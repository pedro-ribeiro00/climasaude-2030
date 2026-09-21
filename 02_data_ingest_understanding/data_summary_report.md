# Data Summary Report - ClimaSaúde 2030

## 1. Objetivo do documento

Este documento apresenta o primeiro levantamento das fontes de dados previstas para o projeto ClimaSaúde 2030, registrando sua origem, formato, principais campos e finalidade dentro da solução.

Como este é um artefato inicial do TDSP, o Data Summary Report será atualizado ao longo dos próximos TPs conforme novas fontes forem incorporadas e os dados forem explorados com maior profundidade.

## 2. Fonte principal - Open-Meteo Weather API

### Descrição

A Open-Meteo Weather API é a fonte de dados meteorológicos utilizada no protótipo do TP1. A aplicação realiza uma requisição HTTP para obter a previsão diária associada às coordenadas de São Paulo.

### Tipo de fonte

API pública.

### Formato dos dados

JSON.

### Dados utilizados no TP1

| Campo utilizado | Finalidade |
|---|---|
| `time` | Identificar a data da previsão |
| `temperature_2m_max` | Exibir a temperatura máxima diária |
| `apparent_temperature_max` | Exibir a sensação térmica máxima diária |
| `uv_index_max` | Exibir o índice UV máximo diário |
| `precipitation_sum` | Exibir a precipitação prevista |

Também são utilizados os parâmetros de latitude, longitude e fuso horário para definir a localidade consultada.

### Objetivo de uso

Fornecer os dados meteorológicos que alimentam a aplicação Streamlit e permitem apresentar ao usuário uma visão resumida das condições climáticas relacionadas à exposição ao calor.

### Situação no TP1

**Integrada ao protótipo.** Os dados são consultados em tempo de execução, convertidos de JSON para estruturas Python e organizados em um DataFrame Pandas antes de serem exibidos no Streamlit.

## 3. Fonte planejada - IBGE

### Descrição

Dados públicos do Instituto Brasileiro de Geografia e Estatística poderão ser incorporados nas próximas etapas para complementar as informações meteorológicas com contexto territorial e demográfico.

### Tipo de fonte

APIs e bases públicas.

### Dados de interesse

- município;
- unidade federativa;
- região;
- população;
- outros indicadores demográficos que se mostrem relevantes durante a evolução do projeto.

### Objetivo de uso

Permitir análises mais contextualizadas das localidades monitoradas e, futuramente, relacionar condições climáticas com características populacionais e territoriais.

### Situação no TP1

**Planejada, ainda não integrada.**

## 4. Fontes textuais planejadas

### Descrição

Nas próximas etapas, o projeto poderá coletar conteúdo de páginas públicas relacionadas a calor extremo, clima, saúde e sustentabilidade.

Os conteúdos poderão incluir notícias, alertas e orientações publicadas na Web.

### Tipo de fonte

Páginas públicas na Web.

### Formato previsto

Dados textuais não estruturados ou semiestruturados, posteriormente organizados em arquivos CSV e/ou TXT.

### Objetivo de uso

Complementar os indicadores numéricos com conteúdo contextual e criar uma base textual que possa ser utilizada posteriormente em técnicas de Processamento de Linguagem Natural e modelos de linguagem.

### Situação no TP1

**Planejada.** A coleta por web scraping será desenvolvida em etapas posteriores.

## 5. Tipos de dados do projeto

| Categoria | Exemplos | Estrutura |
|---|---|---|
| Meteorológicos | temperatura, sensação térmica, UV, precipitação | Estruturados |
| Geográficos | latitude, longitude, município, UF | Estruturados |
| Demográficos | população e indicadores territoriais | Estruturados |
| Conteúdo Web | notícias, alertas e orientações | Não estruturados / semiestruturados |

## 6. Fluxo inicial dos dados

O fluxo implementado no TP1 é:

`Open-Meteo API → requisição HTTP com Requests → resposta JSON → transformação com Python/Pandas → DataFrame → visualização no Streamlit`

Nas próximas etapas, novas fontes poderão ser adicionadas ao fluxo, incluindo dados demográficos e conteúdo obtido por web scraping.

## 7. Qualidade e limitações iniciais

- A disponibilidade da aplicação depende do funcionamento da fonte externa no momento da consulta.
- Os dados apresentados no TP1 são previsões meteorológicas e podem ser atualizados pela fonte ao longo do tempo.
- Indicadores meteorológicos não devem ser interpretados isoladamente como diagnóstico de risco à saúde.
- Fontes futuras podem ter diferentes níveis de atualização, granularidade e cobertura geográfica.
- Dados textuais coletados da Web poderão exigir processos adicionais de limpeza e padronização.
- A integração entre dados climáticos, territoriais e demográficos será realizada progressivamente.

## 8. Situação das fontes

| Fonte | Status no TP1 | Finalidade |
|---|---|---|
| Open-Meteo Weather API | Integrada | Dados meteorológicos |
| IBGE | Planejada | Dados territoriais e demográficos |
| Páginas públicas sobre clima e saúde | Planejada | Conteúdo textual para scraping e análise futura |

## 9. Atualizacao de fontes e processamento - TP2

### Ministerio da Saude - Ondas de Calor

- **Tipo:** pagina publica na Web.
- **Coleta:** Beautiful Soup executado separadamente em `scripts/scrape_heat_content.py`.
- **Conteudo:** titulos, paragrafos e itens de lista relacionados a calor extremo, impactos na saude e orientacoes.
- **Destino:** `data/raw/conteudo_calor_saude.csv` e `data/raw/conteudo_calor_saude.txt`.
- **Objetivo:** complementar os indicadores numericos com contexto textual sobre calor e saude.

### World Health Organization - Heat and Health

- **Tipo:** pagina publica na Web.
- **Coleta:** Beautiful Soup no mesmo script de scraping.
- **Conteudo:** blocos textuais sobre exposicao ao calor, impactos na saude e medidas preventivas.
- **Destino:** integrado aos mesmos arquivos CSV/TXT.
- **Objetivo:** ampliar a base textual e permitir comparacao de conteudo entre fontes.

### Estrutura do CSV de scraping

| Campo | Descricao |
|---|---|
| `fonte` | Nome da instituicao de origem |
| `titulo_pagina` | Titulo HTML da pagina |
| `url` | Endereco da pagina coletada |
| `tipo_elemento` | Tag HTML de origem (`h1`, `h2`, `h3`, `p`, `li`) |
| `texto` | Conteudo textual extraido |
| `coletado_em_utc` | Momento da coleta em UTC |

### Upload de CSV

O TP2 tambem permite que o usuario envie um arquivo CSV pela interface. O arquivo e mantido em `st.session_state` durante a sessao. Quando o CSV possui uma coluna chamada `texto`, seu conteudo e incorporado as estatisticas e a nuvem de palavras, complementando os dados obtidos por scraping.

## 10. Fluxo de dados atualizado - TP2

### Dados climaticos

`Open-Meteo -> Requests -> JSON -> Pandas -> cache -> Streamlit`

### Conteudo Web

`Paginas publicas -> Requests -> Beautiful Soup -> limpeza/deduplicacao -> Pandas -> CSV/TXT em data/raw -> Streamlit -> estatisticas/nuvem de palavras`

### Dados enviados pelo usuario

`Upload CSV -> Pandas -> st.session_state -> visualizacao/estatisticas -> download CSV`

## 11. Qualidade dos dados no TP2

- o scraper remove scripts, estilos, navegacao e rodapes antes da extracao;
- fragmentos muito pequenos e duplicados sao descartados;
- cada registro preserva a fonte e a URL de origem;
- falhas em uma fonte nao impedem o salvamento dos dados coletados de outras fontes;
- conteudos de paginas Web podem mudar ao longo do tempo, portanto o scraping deve ser reexecutado quando necessario;
- os textos sao informativos e nao substituem orientacao medica ou alertas oficiais em tempo real.

## 12. Situacao das fontes no TP2

| Fonte | Status no TP2 | Finalidade |
|---|---|---|
| Open-Meteo | Integrada | Dados meteorologicos |
| Ministerio da Saude | Integrada via scraping | Conteudo sobre calor e saude |
| WHO | Integrada via scraping | Conteudo complementar sobre calor e saude |
| Upload CSV | Integrado | Entrada adicional de dados pelo usuario |
| IBGE | Planejada | Contexto territorial e demografico futuro |
