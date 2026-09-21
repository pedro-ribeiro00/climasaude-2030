from pathlib import Path
import sys


CHECKS = {
    "app.py": 1000,
    "README.md": 1000,
    "01_business_understanding/project_charter.md": 1000,
    "02_data_ingest_understanding/data_summary_report.md": 1000,
    "scripts/scrape_heat_content.py": 500,
    "data/raw/conteudo_calor_saude.csv": 100,
    "data/raw/conteudo_calor_saude.txt": 100,
    "requirements.txt": 20,
}

falhas = []
print("Validacao rapida do TP2\n")

for caminho, minimo in CHECKS.items():
    arquivo = Path(caminho)
    if not arquivo.exists():
        falhas.append(f"FALTANDO: {caminho}")
        print(f"[ERRO] {caminho} - arquivo nao encontrado")
    else:
        tamanho = arquivo.stat().st_size
        if tamanho < minimo:
            falhas.append(f"PEQUENO/VAZIO: {caminho} ({tamanho} bytes)")
            print(f"[ERRO] {caminho} - apenas {tamanho} bytes")
        else:
            print(f"[OK]   {caminho} - {tamanho} bytes")

if falhas:
    print("\nTP2 ainda possui pendencias:")
    for falha in falhas:
        print(f"- {falha}")
    sys.exit(1)

print("\nArquivos essenciais presentes e nao vazios.")
print("Agora teste a interface com: streamlit run app.py")
