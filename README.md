# ClimaSaude 2030

Projeto desenvolvido para a disciplina **Projeto de Bloco: Inteligencia Artificial Aplicada**.

## Problema de negocio

Dados meteorologicos e orientacoes sobre calor extremo existem em fontes diferentes e nem sempre sao apresentados de forma integrada e simples. O ClimaSaude 2030 reune previsoes climaticas e conteudo publico sobre calor e saude em uma interface acessivel.

A aplicacao tem finalidade educativa. Ela nao substitui alertas oficiais ou orientacao medica.

## Funcionalidades do TP3

- aplicacao Streamlit com menu lateral e cinco paginas;
- consulta de previsao climatica para cinco cidades;
- visualizacao e download dos dados climaticos;
- exibicao e analise de conteudo coletado da Web;
- upload, visualizacao e download de CSV;
- FastAPI integrada ao Streamlit;
- web scraping com Beautiful Soup;
- preparacao conceitual para uso futuro de LLM.

## Paginas da aplicacao

1. **Inicio:** apresenta o objetivo e o funcionamento do projeto.
2. **Previsao climatica:** consulta a previsao de sete dias.
3. **Conteudo Web:** exibe e analisa os textos coletados.
4. **Upload e download:** permite explorar um arquivo CSV.
5. **Sobre o projeto:** resume o problema, os ODS e os proximos passos.

## FastAPI

A API possui as seguintes rotas:

| Metodo | Rota | Funcao |
|---|---|---|
| GET | `/health` | Verifica se a API esta funcionando |
| GET | `/cidades` | Lista as cidades disponiveis |
| GET | `/previsao/{cidade_id}` | Consulta a previsao de sete dias |
| POST | `/analises/texto` | Calcula estatisticas dos textos enviados |

O Streamlit consome a rota GET de previsao e a rota POST de analise textual. A documentacao automatica fica disponivel em `http://127.0.0.1:8000/docs` quando a API esta em execucao.

## Fontes de dados

1. **Open-Meteo:** previsao de temperatura maxima, sensacao termica, indice UV e precipitacao.
2. **Ministerio da Saude:** orientacoes publicas sobre ondas de calor.
3. **World Health Organization:** informacoes complementares sobre calor e saude.
4. **CSV do usuario:** dados adicionais enviados durante a sessao.

## Web scraping e Selenium

O script `scripts/scrape_heat_content.py` usa Requests e Beautiful Soup para coletar titulos, paragrafos e itens de lista. O resultado e salvo em CSV e TXT dentro de `data/raw/`.

As paginas utilizadas disponibilizam o conteudo necessario diretamente no HTML, portanto nao foi necessario utilizar Selenium. Beautiful Soup foi suficiente para esta etapa.

## Preparacao para LLM

Nas proximas etapas, os textos coletados poderao ser utilizados por um LLM para gerar resumos e responder perguntas simples sobre calor extremo e saude. A FastAPI podera servir como camada de integracao entre o modelo e a interface Streamlit. O plano esta em `03_modeling/llm_plan.md`.

## Como executar

Requer Python 3.9 ou superior.

### 1. Preparar o ambiente

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Atualizar os dados de scraping

```bash
python scripts/scrape_heat_content.py
```

### 3. Iniciar a FastAPI

No primeiro terminal:

```bash
source .venv/bin/activate
uvicorn api.main:app --reload
```

### 4. Iniciar o Streamlit

No segundo terminal:

```bash
source .venv/bin/activate
streamlit run app.py
```

Para testar o upload, pode ser usado o arquivo `data/sample_upload.csv`.

## Estrutura principal

```text
climasaude-2030/
├── app.py
├── requirements.txt
├── README.md
├── api/
│   └── main.py
├── climasaude/
│   ├── analysis.py
│   ├── api_client.py
│   ├── config.py
│   ├── ui.py
│   └── weather.py
├── scripts/
│   └── scrape_heat_content.py
├── data/
│   ├── raw/
│   └── sample_upload.csv
├── 01_business_understanding/
├── 02_data_ingest_understanding/
├── 03_modeling/
└── 04_deployment/
```

## ODS e metodologia

O projeto se relaciona principalmente ao **ODS 13 - Acao Contra a Mudanca Global do Clima**, com conexoes ao **ODS 3 - Saude e Bem-Estar** e ao **ODS 11 - Cidades e Comunidades Sustentaveis**.

O repositorio segue a organizacao do TDSP, com CRISP-DM como referencia complementar.

## Repositorio

https://github.com/pedro-ribeiro00/climasaude-2030
