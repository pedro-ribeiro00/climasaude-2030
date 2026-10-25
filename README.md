# ClimaSaude 2030

Projeto da disciplina **Projeto de Bloco: Inteligencia Artificial Aplicada**. O TP3 evolui o prototipo para uma aplicacao multipagina com separacao entre interface, API e fontes de dados.

## Problema de negocio

Dados meteorologicos e orientacoes publicas sobre calor extremo existem em fontes separadas e nem sempre chegam ao cidadao de forma integrada e facil de interpretar. O ClimaSaude 2030 organiza previsoes climaticas e conteudo publico sobre calor e saude, preservando a origem dos dados e deixando a arquitetura pronta para analises futuras com LLM.

A aplicacao tem finalidade educativa. Ela nao substitui alertas meteorologicos oficiais, atendimento medico ou orientacao de profissionais de saude.

## Entregas do TP3

- aplicacao Streamlit com cinco paginas e menu lateral;
- paginas de inicio, previsao, conteudo Web, upload/download e documentacao;
- FastAPI propria com documentacao automatica;
- rotas GET para status, cidades e previsao;
- rota POST para analise textual;
- integracao real do Streamlit com a FastAPI;
- scraping aprimorado com Beautiful Soup;
- CSV e TXT com fonte, URL, idioma, hash e momento da coleta;
- testes automatizados e validador da rubrica;
- Project Charter e Data Summary Report revisados;
- plano explicito de integracao futura com LLM e RAG.

## Arquitetura

```text
Open-Meteo ───────────────→ FastAPI ──→ Streamlit multipagina
                                  ↑
Paginas publicas → Beautiful Soup → CSV/TXT → analise textual
CSV do usuario ──────────────────────────────→ sessao Streamlit
```

O Streamlit nao consulta diretamente a Open-Meteo. A pagina de previsao chama `GET /previsao/{cidade_id}`. A pagina de conteudo envia os textos para `POST /analises/texto`. Essa separacao permite testar a regra de negocio, controlar erros de fontes externas e incorporar um provedor de LLM futuramente sem expor credenciais na interface.

## Rotas da FastAPI

| Metodo | Rota | Funcao |
|---|---|---|
| GET | `/` | Identifica o servico |
| GET | `/health` | Verifica status e versao |
| GET | `/cidades` | Lista localidades disponiveis |
| GET | `/previsao/{cidade_id}` | Normaliza a previsao de sete dias |
| POST | `/analises/texto` | Calcula metricas e palavras frequentes |

Exemplo do corpo da rota POST:

```json
{
  "textos": ["Calor extremo exige hidratacao e atencao."],
  "limite": 10
}
```

Com a API em execucao, a documentacao interativa fica em `http://127.0.0.1:8000/docs`.

## Web scraping e decisao sobre Selenium

O script `scripts/scrape_heat_content.py` coleta blocos textuais de paginas publicas do Ministerio da Saude e da World Health Organization. Ele remove navegacao, scripts, estilos e rodapes, descarta fragmentos pequenos, elimina duplicidades e registra metadados de proveniencia.

**Selenium nao foi utilizado porque nao ha necessidade tecnica nas fontes atuais.** O conteudo relevante ja esta presente no HTML devolvido pelo servidor e nao exige login, preenchimento de formulario, rolagem, clique ou execucao de JavaScript. Requests + Beautiful Soup executam a tarefa com menos dependencias, menor consumo de recursos e maior facilidade de teste. Se uma nova fonte carregar o conteudo somente apos interacao dinamica, Selenium podera ser incorporado de forma isolada ao pipeline de coleta.

## Fontes de dados

1. **Open-Meteo Weather API:** previsao diaria de temperatura maxima, sensacao termica maxima, UV e precipitacao.
2. **Ministerio da Saude — Ondas de Calor:** orientacoes publicas em portugues.
3. **WHO — Heat and Health:** conteudo internacional complementar em ingles.
4. **CSV enviado pelo usuario:** exploracao temporaria; uma coluna `texto` complementa a analise sem persistencia automatica.

## Preparacao do ambiente

Requer Python 3.9 ou superior.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Para atualizar o scraping, validar a estrutura e executar todos os testes:

```bash
bash scripts/prepare_tp3.sh
```

## Execucao

A aplicacao usa dois processos. Na raiz do repositorio, abra dois terminais com o ambiente virtual ativo.

Terminal 1 — API:

```bash
uvicorn api.main:app --reload
```

Terminal 2 — interface:

```bash
streamlit run app.py
```

Por padrao, a interface usa `http://127.0.0.1:8000`. Para outro endereco:

```bash
export CLIMASAUDE_API_URL="http://servidor:8000"
streamlit run app.py
```

## Testes e aceite

```bash
python -m pytest -q
python scripts/validate_tp3.py
```

O mapeamento item por item da rubrica esta em `05_acceptance/tp3_checklist.md`.

## Preparacao para LLM

O arquivo `03_modeling/llm_integration_plan.md` define o caso de uso, a arquitetura RAG, o contrato de entrada e saida, cuidados com privacidade, guardrails e avaliacao. Nenhuma chave ou chamada a modelo foi adicionada no TP3. A base textual ja preserva metadados necessarios para segmentacao, recuperacao e citacao de fontes.

## Estrutura principal

```text
climasaude-2030/
├── api/
│   └── main.py
├── climasaude/
│   ├── analysis.py
│   ├── api_client.py
│   ├── config.py
│   ├── ui.py
│   └── weather.py
├── scripts/
│   ├── prepare_tp3.sh
│   ├── scrape_heat_content.py
│   └── validate_tp3.py
├── tests/
├── data/raw/
├── 01_business_understanding/
├── 02_data_ingest_understanding/
├── 03_modeling/
├── 04_deployment/
├── 05_acceptance/
├── app.py
└── requirements.txt
```

## Metodologia e alinhamento

O projeto segue o TDSP, com CRISP-DM como referencia complementar. Relaciona-se principalmente ao **ODS 13 — Acao Contra a Mudanca Global do Clima**, com conexoes ao **ODS 3 — Saude e Bem-Estar** e ao **ODS 11 — Cidades e Comunidades Sustentaveis**.

## Repositorio

https://github.com/pedro-ribeiro00/climasaude-2030

## Status

**TP3 implementado: Streamlit multipagina, FastAPI integrada, scraping rastreavel, documentacao revisada, preparacao para LLM e validacao automatizada.**
