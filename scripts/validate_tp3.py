"""Valida arquivos, estrutura, dados e rotas obrigatorias do TP3."""

import ast
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api.main import app


ARQUIVOS = {
    "app.py": 300,
    "api/main.py": 1000,
    "climasaude/ui.py": 3000,
    "README.md": 2000,
    "01_business_understanding/project_charter.md": 2000,
    "02_data_ingest_understanding/data_summary_report.md": 2000,
    "03_modeling/llm_integration_plan.md": 1500,
    "05_acceptance/tp3_checklist.md": 1000,
    "scripts/scrape_heat_content.py": 1000,
    "data/raw/conteudo_calor_saude.csv": 100,
    "data/raw/conteudo_calor_saude.txt": 100,
    "requirements.txt": 100,
}

MARCADORES = {
    "app.py": ["st.navigation", "st.Page"],
    "README.md": ["FastAPI", "Streamlit", "Selenium", "LLM"],
    "01_business_understanding/project_charter.md": ["TP3", "FastAPI", "LLM"],
    "02_data_ingest_understanding/data_summary_report.md": ["TP3", "Beautiful Soup", "Selenium"],
}


def validar() -> list[str]:
    falhas: list[str] = []
    print("Validacao automatica do TP3\n")

    for caminho, minimo in ARQUIVOS.items():
        arquivo = Path(caminho)
        if not arquivo.exists():
            falhas.append(f"Arquivo ausente: {caminho}")
        elif arquivo.stat().st_size < minimo:
            falhas.append(f"Arquivo pequeno ou vazio: {caminho}")
        else:
            print(f"[OK] arquivo: {caminho}")

    for caminho, termos in MARCADORES.items():
        arquivo = Path(caminho)
        if not arquivo.exists():
            continue
        conteudo = arquivo.read_text(encoding="utf-8")
        for termo in termos:
            if termo not in conteudo:
                falhas.append(f"{caminho} nao menciona: {termo}")

    for arquivo in Path(".").rglob("*.py"):
        if ".venv" in arquivo.parts:
            continue
        try:
            ast.parse(arquivo.read_text(encoding="utf-8"), filename=str(arquivo))
        except SyntaxError as exc:
            falhas.append(f"Erro de sintaxe em {arquivo}: {exc}")
    print("[OK] sintaxe dos arquivos Python")

    metodos_por_rota = {
        rota.path: rota.methods
        for rota in app.routes
        if hasattr(rota, "methods")
    }
    if "GET" not in metodos_por_rota.get("/previsao/{cidade_id}", set()):
        falhas.append("Rota GET /previsao/{cidade_id} ausente")
    if "POST" not in metodos_por_rota.get("/analises/texto", set()):
        falhas.append("Rota POST /analises/texto ausente")
    print("[OK] rotas GET e POST da FastAPI")

    csv = Path("data/raw/conteudo_calor_saude.csv")
    if csv.exists():
        colunas = set(pd.read_csv(csv, nrows=1).columns)
        obrigatorias = {"fonte", "url", "texto", "coletado_em_utc"}
        if not obrigatorias.issubset(colunas):
            falhas.append(f"CSV sem colunas obrigatorias: {sorted(obrigatorias - colunas)}")
        else:
            print("[OK] esquema rastreavel do scraping")

    return falhas


if __name__ == "__main__":
    problemas = validar()
    if problemas:
        print("\nPendencias encontradas:")
        for problema in problemas:
            print(f"- {problema}")
        sys.exit(1)
    print("\nTP3 validado: estrutura e criterios obrigatorios presentes.")
