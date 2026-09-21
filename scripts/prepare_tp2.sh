#!/bin/bash
set -e

if [ -z "${VIRTUAL_ENV:-}" ]; then
  echo "ERRO: ative primeiro o ambiente virtual: source .venv/bin/activate"
  exit 1
fi

echo "1/3 - Instalando/atualizando dependencias..."
python -m pip install -r requirements.txt

echo "2/3 - Executando web scraping com Beautiful Soup..."
python scripts/scrape_heat_content.py

echo "3/3 - Validando arquivos essenciais..."
python scripts/validate_tp2.py

echo
necho="TP2 preparado. Execute agora: streamlit run app.py"
echo "$necho"
