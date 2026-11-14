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

As instrucoes completas e atualizadas de instalacao, download do modelo e execucao estao no README da raiz. O projeto usa dois processos locais: FastAPI e Streamlit. O scraper e executado separadamente para atualizar `data/raw/`.

## Execucao do TP3

O TP3 possui dois processos. A API deve ser iniciada antes da interface:

```bash
# Terminal 1
source .venv/bin/activate
uvicorn api.main:app --reload
```

```bash
# Terminal 2
source .venv/bin/activate
streamlit run app.py
```

A URL padrao da API e `http://127.0.0.1:8000`. A documentacao das rotas pode ser consultada em `http://127.0.0.1:8000/docs`.

## Execucao do TP4

Apos baixar o modelo uma vez, o resumo e gerado localmente por meio da rota `/processar_texto`, sem conexao com servico externo. Para os comandos atualizados e detalhes de hardware, consulte o README e `03_modeling/llm_plan.md`.
