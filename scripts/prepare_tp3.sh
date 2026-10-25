#!/bin/bash
set -euo pipefail

if [ -z "${VIRTUAL_ENV:-}" ]; then
  echo "ERRO: ative primeiro o ambiente virtual: source .venv/bin/activate"
  exit 1
fi

echo "1/4 - Instalando ou atualizando dependencias..."
python -m pip install -r requirements.txt

echo "2/4 - Atualizando os dados com Beautiful Soup..."
python scripts/scrape_heat_content.py

echo "3/4 - Validando a estrutura e a rubrica..."
python scripts/validate_tp3.py

echo "4/4 - Executando testes automatizados..."
python -m pytest -q

echo
echo "TP3 preparado e testado."
echo "Terminal 1: uvicorn api.main:app --reload"
echo "Terminal 2: streamlit run app.py"
