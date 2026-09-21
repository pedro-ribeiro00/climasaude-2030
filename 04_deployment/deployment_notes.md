# Deployment Notes - ClimaSaude 2030

## Controle de versao

O projeto utiliza Git para controle de versao e GitHub como repositorio remoto:

https://github.com/pedro-ribeiro00/climasaude-2030

O fluxo utilizado e:

1. desenvolver e testar localmente;
2. revisar alteracoes com `git status` e `git diff`;
3. versionar com `git add` e `git commit`;
4. sincronizar com `git push origin main`.

## Preparacao para deploy

A aplicacao possui `requirements.txt` na raiz e `app.py` como ponto de entrada,
permitindo reproduzir o ambiente localmente e preparando o projeto para servicos
compativeis com Streamlit.

Execucao local:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/scrape_heat_content.py
streamlit run app.py
```

O scraping e executado separadamente da interface e grava os dados em `data/raw/`,
conforme a organizacao do projeto.
