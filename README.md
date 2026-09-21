# ClimaSaude 2030

Projeto desenvolvido para a disciplina **Projeto de Bloco: Inteligencia Artificial Aplicada**.

## Problema de negocio

Eventos de calor extremo podem representar riscos a saude e ao bem-estar da populacao, especialmente em areas urbanas. Apesar da disponibilidade de dados meteorologicos e informacoes publicas sobre os impactos do calor, essas informacoes nem sempre sao apresentadas de forma integrada e simples para cidadaos e gestores.

O ClimaSaude 2030 busca reduzir essa dificuldade de interpretacao, combinando dados climaticos estruturados com conteudo publico sobre calor e saude em uma interface interativa.

## Solucao - TP2

A aplicacao Streamlit evoluiu para incluir:

- selecao interativa de cidades;
- consulta de previsao de 7 dias via Open-Meteo;
- cache para reduzir consultas repetidas;
- estado de sessao para preservar historico de cidades e CSV enviado pelo usuario;
- web scraping separado com Beautiful Soup;
- armazenamento do scraping em CSV e TXT em `data/raw/`;
- tabela, estatisticas de texto e nuvem de palavras;
- upload de arquivos CSV;
- download de dados climaticos, conteudo coletado e CSV enviado;
- documentacao TDSP atualizada.

## Publico-alvo

O publico-alvo principal e formado por **cidadaos interessados em compreender de forma simples as condicoes climaticas de sua localidade**. Como publicos secundarios, a aplicacao pode atender gestores publicos, organizacoes sociais, profissionais de sustentabilidade e pesquisadores interessados em clima, cidades e saude.

## Metas e indicadores

| Meta | Indicador de sucesso |
|---|---|
| Consumir dados climaticos | Consulta bem-sucedida a Open-Meteo |
| Tornar a interface interativa | Usuario seleciona diferentes cidades |
| Coletar conteudo Web | Beautiful Soup gera CSV/TXT em `data/raw/` |
| Exibir informacoes extraidas | Tabela, estatisticas e nuvem de palavras disponiveis |
| Melhorar performance | Uso de `st.cache_data` |
| Preservar dados de interacao | Uso de `st.session_state` |
| Permitir entrada e saida de dados | Upload e download de CSV funcionais |
| Garantir reprodutibilidade | Dependencias documentadas em `requirements.txt` |

## ESG e Agenda 2030

O projeto se relaciona principalmente aos pilares **Ambiental** e **Social** do ESG.

O **ODS 13 - Acao Contra a Mudanca Global do Clima** e o ODS principal porque a solucao utiliza dados climaticos para facilitar a compreensao e a comunicacao de condicoes associadas ao calor extremo, contribuindo para conscientizacao e adaptacao a impactos climaticos.

Tambem se relaciona ao **ODS 3 - Saude e Bem-Estar** e ao **ODS 11 - Cidades e Comunidades Sustentaveis**.

## Fontes de dados

1. **Open-Meteo Weather API** - previsao diaria de temperatura, sensacao termica, UV e precipitacao.
2. **Ministerio da Saude - Ondas de Calor** - conteudo publico sobre impactos e cuidados relacionados ao calor.
3. **World Health Organization - Heat and Health** - conteudo publico sobre calor e saude.
4. **CSV enviado pelo usuario** - dados adicionais para exploracao; quando existe uma coluna `texto`, seu conteudo complementa as estatisticas e a nuvem de palavras.

## Metodologia

O projeto utiliza o **TDSP (Team Data Science Process)** como metodologia principal. O CRISP-DM e utilizado como referencia complementar para o ciclo de Ciencia de Dados.

## Estrutura

```text
climasaude-2030/
├── app.py
├── README.md
├── requirements.txt
├── scripts/
│   ├── scrape_heat_content.py
│   ├── validate_tp2.py
│   └── prepare_tp2.sh
├── data/
│   ├── raw/
│   └── processed/
├── 01_business_understanding/
│   └── project_charter.md
├── 02_data_ingest_understanding/
│   └── data_summary_report.md
├── 03_modeling/
├── 04_deployment/
│   └── deployment_notes.md
└── 05_acceptance/
```

## Execucao rapida

### 1. Ativar o ambiente virtual

```bash
source .venv/bin/activate
```

### 2. Preparar o TP2

O script abaixo instala as dependencias, executa o scraping e valida os arquivos:

```bash
bash scripts/prepare_tp2.sh
```

### 3. Executar a aplicacao

```bash
streamlit run app.py
```

Para testar rapidamente o upload de CSV, use o arquivo `data/sample_upload.csv`.

## Execucao manual

```bash
pip install -r requirements.txt
python scripts/scrape_heat_content.py
python scripts/validate_tp2.py
streamlit run app.py
```

## Controle de versao e deploy

O projeto usa Git/GitHub para controle de versao. As notas de preparacao para deploy estao em `04_deployment/deployment_notes.md`.

## Repositorio

https://github.com/pedro-ribeiro00/climasaude-2030

## Status

**TP2 - interface interativa, web scraping, cache, session state, upload/download e documentacao implementados.**
