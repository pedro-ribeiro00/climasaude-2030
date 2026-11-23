"""Testa a API com fontes e Qwen reais. Execute na raiz, com a porta 8000 livre."""

import json
import os
from pathlib import Path
import subprocess
import sys
import time

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "http://127.0.0.1:8000"


def main():
    os.chdir(ROOT)
    pasta = ROOT / "05_acceptance/evidencias"
    pasta.mkdir(exist_ok=True)
    resultados = []
    with (pasta / "api_execucao.log").open("w") as log:
        servidor = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "api.main:app", "--port", "8000"],
            stdout=log, stderr=subprocess.STDOUT,
            env={**os.environ, "HF_HUB_OFFLINE": "1"},
        )
        try:
            for _ in range(100):
                if servidor.poll() is not None:
                    raise RuntimeError("A API não iniciou; confira api_execucao.log")
                try:
                    if requests.get(f"{BASE_URL}/health", timeout=1).ok:
                        break
                except requests.RequestException:
                    pass
                time.sleep(0.1)
            else:
                raise RuntimeError("A API não ficou disponível")

            def verificar(metodo, rota, corpo=None, esperado=200):
                inicio = time.perf_counter()
                resposta = requests.request(metodo, BASE_URL + rota, json=corpo, timeout=300)
                registro = {
                    "method": metodo, "path": rota, "status": resposta.status_code,
                    "expected": esperado, "seconds": round(time.perf_counter() - inicio, 3),
                    "response": resposta.json(),
                }
                resultados.append(registro)
                print(metodo, rota, resposta.status_code, registro["seconds"], flush=True)
                assert resposta.status_code == esperado, registro
                return registro

            verificar("GET", "/health")
            verificar("GET", "/cidades")
            verificar("GET", "/previsao/inexistente", esperado=404)
            verificar("POST", "/analises/texto", {"textos": ["Calor e saúde. Calor nas cidades."]})
            verificar("POST", "/analises/texto", {"textos": []}, 422)
            verificar("POST", "/analises/texto", {"textos": ["a"], "limite": 51}, 422)
            for corpo in [{"texto": ""}, {"texto": "  "}, {"texto": "a" * 6001}]:
                verificar("POST", "/processar_texto", corpo, 422)
            for corpo in [
                {"textos": [], "contexto": "a"},
                {"textos": [" "], "contexto": "a"},
                {"textos": ["texto"], "contexto": " "},
                {"textos": ["a" * 40001], "contexto": "a"},
            ]:
                verificar("POST", "/sintese", corpo, 422)

            df = pd.read_csv(ROOT / "data/raw/conteudo_calor_saude.csv")
            verificar("POST", "/processar_texto", {"texto": df.iloc[0].texto})
            for cidade, fonte in [
                ("sao-paulo", "Ministerio da Saude"),
                ("rio-de-janeiro", "World Health Organization"),
                ("sao-paulo", None),
            ]:
                previsao = verificar("GET", "/previsao/" + cidade)["response"]
                linhas = df if fonte is None else df[df.fonte == fonte]
                contexto = "Cidade: " + previsao["cidade"] + ". " + " | ".join(
                    f"{d['data']}: temperatura máxima {d['temperatura_max_c']} °C, "
                    f"sensação térmica {d['sensacao_max_c']} °C, UV {d['uv_max']}"
                    for d in previsao["previsao"]
                )
                textos = [f"Fonte: {r.fonte}. {r.texto}" for r in linhas.itertuples()]
                registro = verificar("POST", "/sintese", {"textos": textos, "contexto": contexto})
                registro["configuration"] = {"city": cidade, "source": fonte or "Ambas"}
                resultado = registro["response"]["resultado"]
                assert contexto in resultado
                evidencias = resultado.split("**Síntese extrativa — trechos selecionados pelo Qwen**")[1]
                assert all(t.startswith("- ") and t[2:] in textos for t in evidencias.strip().split("\n\n"))
                registro["trechos_conferidos_com_csv"] = True
        finally:
            (pasta / "api_real.json").write_text(json.dumps(resultados, ensure_ascii=False, indent=2))
            servidor.terminate()
            servidor.wait(timeout=15)


if __name__ == "__main__":
    main()
