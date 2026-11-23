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


## Execução TP5

O **Painel final** é uma nova página do Streamlit. Ela utiliza a previsão via FastAPI e os arquivos CSV produzidos pelo scraper. A nova rota `POST /sintese` executa o modelo local, mantendo os comandos de inicialização do TP4.

Para conferir a aplicação: iniciar FastAPI e Streamlit, selecionar cidade e fontes, gerar a síntese, conferir o retorno e confrontá-lo com as URLs originais. A execução integral depende dos pesos do Qwen instalados no computador.

## Validação final — 23/11/2026

Foram instaladas as dependências em Python 3.12 e os pesos reais do Qwen. Os serviços iniciaram e a API foi exercitada por HTTP junto com a aplicação Streamlit por AppTest. Os scripts `scripts/validar_tp5.py` e `scripts/validar_interface_tp5.py` permitem repetir os testes. O relatório de aceite distingue testes reais aprovados da inspeção visual pendente.

As correções foram registradas primeiro na branch `validacao-tp5-real`; a entrega final incorpora código, evidências, documentos e PDF à `main`, pelo PR #1. O acesso do navegador do Work às portas locais não funcionou e houve bloqueio pela política de segurança do navegador. Não houve publicação de um dashboard acessível externamente nem captura de imagens da aplicação funcionando.
