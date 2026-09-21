# 🌡️ ClimaSaúde 2030

Projeto desenvolvido para a disciplina **Projeto de Bloco: Inteligência Artificial Aplicada**.

## Problema de negócio

Eventos de calor extremo podem representar riscos à saúde e ao bem-estar da população, especialmente em áreas urbanas. Apesar da disponibilidade de dados meteorológicos públicos, informações como temperatura, sensação térmica e índice UV nem sempre são apresentadas de forma integrada e simples para cidadãos e gestores.

O ClimaSaúde 2030 busca reduzir essa dificuldade de interpretação, transformando dados climáticos públicos em informações organizadas e acessíveis sobre condições associadas à exposição ao calor.

## Solução proposta

A solução é uma aplicação data-driven desenvolvida em Python e Streamlit. Nesta primeira versão, ela consulta a Open-Meteo Weather API, processa os dados com Pandas e apresenta temperatura máxima, sensação térmica máxima, índice UV e precipitação em uma tabela de fácil leitura.

O projeto foi estruturado para evoluir ao longo dos próximos TPs, incorporando novas fontes de dados, web scraping, FastAPI e recursos de Inteligência Artificial.

## Objetivo

Desenvolver uma aplicação capaz de coletar, processar e apresentar dados climáticos de maneira acessível, facilitando a compreensão de condições associadas à exposição ao calor extremo.

## Público-alvo

O público-alvo principal é formado por **cidadãos interessados em compreender de forma simples as condições climáticas de sua localidade**.

Como públicos secundários, a aplicação poderá atender gestores públicos, organizações sociais, profissionais de sustentabilidade e pesquisadores interessados em clima, cidades e saúde.

## Metas e indicadores de sucesso

| Meta | Indicador de sucesso |
|---|---|
| Integrar uma fonte pública de dados climáticos | Consulta bem-sucedida à Open-Meteo Weather API |
| Exibir indicadores climáticos no protótipo | Temperatura, sensação térmica, UV e precipitação disponíveis |
| Disponibilizar uma interface funcional | Aplicação Streamlit executa localmente sem erros |
| Garantir reprodutibilidade | Dependências documentadas em `requirements.txt` |
| Manter o projeto preparado para evolução | Estrutura de diretórios organizada segundo o TDSP |

## ESG e Agenda 2030

O projeto se relaciona principalmente aos pilares **Ambiental** e **Social** do ESG.

### ODS principal: ODS 13 - Ação Contra a Mudança Global do Clima

O ODS 13 foi escolhido como principal porque o projeto utiliza dados climáticos para facilitar a identificação e a comunicação de condições associadas ao calor extremo, apoiando a conscientização e a adaptação a impactos climáticos.

O projeto também se relaciona com:

- **ODS 3 - Saúde e Bem-Estar**, devido à relação entre exposição ao calor, saúde e bem-estar da população.
- **ODS 11 - Cidades e Comunidades Sustentáveis**, pela importância de cidades mais preparadas para eventos climáticos extremos.

## Fonte de dados do TP1

A primeira versão utiliza a **Open-Meteo Weather API** para obter dados meteorológicos em formato JSON. Esses dados são convertidos para um DataFrame Pandas e exibidos no dashboard.

Fontes adicionais, como dados do IBGE e conteúdos públicos da Web, estão planejadas para as próximas etapas.

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- Requests
- Open-Meteo Weather API
- Git / GitHub

## Metodologia

O projeto utiliza o **TDSP (Team Data Science Process)** como metodologia principal de organização e desenvolvimento.

O **CRISP-DM** é utilizado como referência complementar para o ciclo de Ciência de Dados, sem duplicar a estrutura do projeto.

## Estrutura do projeto

```text
climasaude-2030/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   └── processed/
│
├── 01_business_understanding/
│   └── project_charter.md
│
├── 02_data_ingest_understanding/
│   └── data_summary_report.md
│
├── 03_modeling/
├── 04_deployment/
└── 05_acceptance/
```

## Executando o projeto

### 1. Criar o ambiente virtual

```bash
python3 -m venv .venv
```

### 2. Ativar o ambiente virtual

No macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação

```bash
streamlit run app.py
```

## Artefatos TDSP

- `01_business_understanding/project_charter.md`: problema de negócio, objetivos, metas, indicadores, público-alvo, stakeholders, ESG/ODS e escopo.
- `02_data_ingest_understanding/data_summary_report.md`: fontes de dados, tipos, campos, finalidades, fluxo de dados e limitações iniciais.

## Repositório

GitHub: https://github.com/pedro-ribeiro00/climasaude-2030

## Status

**TP1 concluído.** A base do projeto está preparada para evolução nos próximos Testes de Performance.
