"""Testa interações do Streamlit com AppTest e API real; não testa pixels."""

import json
import os
from pathlib import Path
import subprocess
import sys
import time

import pandas as pd
import requests
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def main():
    os.chdir(ROOT)
    pasta = ROOT / "05_acceptance/evidencias"
    pasta.mkdir(exist_ok=True)
    resultados = []

    def registrar(nome, app):
        registro = {
            "case": nome,
            "exceptions": [str(x.value) for x in app.exception],
            "errors": [str(x.value) for x in app.error],
            "metrics": [{x.label: x.value} for x in app.metric],
            "captions": [x.value for x in app.caption],
        }
        resultados.append(registro)
        print(nome, flush=True)
        assert not app.exception
        assert not app.error
        return registro

    with (pasta / "interface_api_execucao.log").open("w") as log:
        servidor = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "api.main:app", "--port", "8000"],
            stdout=log, stderr=subprocess.STDOUT,
            env={**os.environ, "HF_HUB_OFFLINE": "1"},
        )
        try:
            for _ in range(100):
                if servidor.poll() is not None:
                    raise RuntimeError("Não foi possível iniciar a API de teste")
                try:
                    if requests.get("http://127.0.0.1:8000/health", timeout=1).ok:
                        break
                except requests.RequestException:
                    pass
                time.sleep(0.1)
            else:
                raise RuntimeError("A API não ficou disponível")

            app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=300).run()
            registrar("Inicio", app)
            for funcao in ["render_clima", "render_conteudo", "render_arquivos", "render_projeto", "render_dashboard"]:
                app = AppTest.from_string(
                    f"from climasaude.ui import {funcao}\n{funcao}()", default_timeout=300,
                ).run()
                registrar(funcao, app)
                if funcao == "render_clima":
                    for cidade in ["Rio de Janeiro - RJ", "Belo Horizonte - MG", "Brasilia - DF", "Porto Alegre - RS"]:
                        app.selectbox[0].select(cidade).run()
                        registrar("clima " + cidade, app)
                elif funcao == "render_arquivos":
                    # Verifica o processamento após carregar; não simula o seletor de arquivos do navegador.
                    app.session_state["dados_upload"] = pd.read_csv(ROOT / "data/sample_upload.csv")
                    app.run()
                    registrar("CSV na sessão", app)
                    assert len(app.dataframe) == 2
                    app.button[0].click().run()
                    registrar("Limpar CSV", app)
                elif funcao == "render_conteudo":
                    app.button[0].click().run()
                    assert len(app.warning) == 1
                    registrar("Resumo vazio", app)
                    app.multiselect[0].set_value([]).run()
                    assert len(app.info) > 0
                    registrar("Nenhuma fonte em Conteudo Web", app)
                elif funcao == "render_dashboard":
                    for cidade, fonte in [
                        ("Sao Paulo - SP", "Ministerio da Saude"),
                        ("Rio de Janeiro - RJ", "World Health Organization"),
                    ]:
                        app.selectbox[0].select(cidade)
                        app.multiselect[0].set_value([fonte])
                        app.run()
                        inicio = time.perf_counter()
                        app.button[0].click().run()
                        registro = registrar("Gerar síntese " + cidade + " / " + fonte, app)
                        registro["seconds"] = round(time.perf_counter() - inicio, 3)
                        registro["markdown"] = [x.value for x in app.markdown]
                        app.run()
                        registrar("Síntese preservada após rerun " + cidade, app)
                        assert any("Síntese extrativa — trechos selecionados" in x.value for x in app.markdown)
                    app.multiselect[0].set_value([]).run()
                    registrar("Nenhuma fonte no Painel final", app)
        finally:
            (pasta / "streamlit_interacoes.json").write_text(json.dumps(resultados, ensure_ascii=False, indent=2))
            servidor.terminate()
            servidor.wait(timeout=15)


if __name__ == "__main__":
    main()
