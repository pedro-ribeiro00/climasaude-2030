# 🌡️ ClimaSaúde 2030

Projeto desenvolvido para a disciplina **Projeto de Bloco: Inteligência Artificial Aplicada**.

## Sobre o projeto

O ClimaSaúde 2030 é uma aplicação data-driven que busca facilitar a
interpretação de dados climáticos relacionados à exposição ao calor extremo.

A solução utiliza dados públicos para apresentar informações como temperatura,
sensação térmica, índice UV e precipitação de maneira simples e acessível.

## Objetivo

Desenvolver uma solução capaz de coletar, processar e apresentar dados
climáticos, contribuindo para a compreensão de condições associadas ao calor
extremo.

O projeto está alinhado principalmente ao:

- ODS 13 - Ação Contra a Mudança Global do Clima

Também possui relação com:

- ODS 3 - Saúde e Bem-Estar
- ODS 11 - Cidades e Comunidades Sustentáveis

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- Requests
- Open-Meteo Weather API
- Git

## Metodologia

O projeto utiliza o **TDSP (Team Data Science Process)** como metodologia
principal de organização e desenvolvimento.

O **CRISP-DM** é utilizado como referência complementar para o ciclo de
Ciência de Dados.

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