# Project Charter - ClimaSaúde 2030

## 1. Nome do projeto

**ClimaSaúde 2030 - Monitoramento de Condições Associadas ao Calor Extremo**

## 2. Problema de negócio

Eventos de calor extremo podem representar riscos à saúde e ao bem-estar da população, especialmente em áreas urbanas. Embora existam dados meteorológicos públicos, informações como temperatura, sensação térmica e índice UV nem sempre são apresentadas de forma integrada e simples para cidadãos e gestores.

O problema de negócio tratado pelo projeto é, portanto, a dificuldade de transformar dados climáticos disponíveis em informações de fácil interpretação, capazes de apoiar a identificação de períodos com maior exposição ao calor e melhorar a comunicação dessas condições para o público.

## 3. Proposta da solução

Desenvolver uma aplicação data-driven em Python e Streamlit que consulte fontes públicas de dados climáticos, processe as informações e apresente indicadores relevantes em uma interface simples e acessível.

Na primeira versão, a aplicação apresenta dados de temperatura máxima, sensação térmica máxima, índice UV e precipitação. Nas etapas seguintes, o projeto poderá incorporar novas fontes de dados, conteúdo textual coletado da Web e recursos de Inteligência Artificial para gerar análises e insights contextualizados.

## 4. Objetivo geral

Desenvolver uma aplicação capaz de coletar, processar e apresentar dados climáticos de maneira acessível, facilitando a compreensão de condições associadas à exposição ao calor extremo.

## 5. Objetivos específicos

- Consumir dados climáticos de fontes públicas por meio de APIs.
- Processar e organizar os dados utilizando Python e Pandas.
- Apresentar os principais indicadores climáticos em uma interface Streamlit.
- Facilitar a interpretação de informações relacionadas à exposição ao calor.
- Manter o projeto estruturado para receber novas fontes de dados e funcionalidades nas próximas etapas.
- Preparar a arquitetura para futura integração com técnicas de Inteligência Artificial e modelos de linguagem.

## 6. Público-alvo

O público-alvo principal é formado por **cidadãos que desejam compreender, de forma simples, as condições climáticas de sua localidade e situações de maior exposição ao calor**.

Como públicos secundários, a solução poderá atender gestores públicos, organizações sociais, profissionais de sustentabilidade e pesquisadores interessados em clima, cidades e saúde.

## 7. Metas do projeto

- Integrar pelo menos uma API pública de dados climáticos no protótipo inicial.
- Exibir temperatura máxima, sensação térmica máxima, índice UV e precipitação.
- Disponibilizar os dados em uma aplicação Streamlit executável localmente.
- Garantir que o ambiente do projeto possa ser reproduzido a partir do arquivo `requirements.txt`.
- Estruturar o projeto segundo as fases do TDSP para permitir sua evolução durante os próximos TPs.

## 8. Indicadores de sucesso

| Indicador | Critério de sucesso |
|---|---|
| Integração com fonte externa | A aplicação realiza consulta bem-sucedida à API climática |
| Indicadores disponíveis | Temperatura, sensação térmica, índice UV e precipitação são exibidos |
| Atualização dos dados | Os dados são obtidos automaticamente a partir da API |
| Funcionamento da aplicação | O dashboard Streamlit executa localmente sem erros |
| Reprodutibilidade | O ambiente pode ser recriado usando `requirements.txt` |
| Usabilidade inicial | Os indicadores são apresentados de maneira organizada e compreensível |

## 9. Alinhamento com ESG

O projeto se relaciona principalmente aos pilares **Ambiental** e **Social** do ESG.

### Ambiental

A solução utiliza dados ambientais e meteorológicos para ampliar a compreensão de condições associadas a eventos de calor extremo e seus impactos nas cidades.

### Social

A apresentação acessível dessas informações aproxima dados climáticos de questões relacionadas à saúde e ao bem-estar da população, contribuindo para conscientização e melhor compreensão de situações de exposição ao calor.

## 10. Objetivos de Desenvolvimento Sustentável (ODS)

### ODS principal: ODS 13 - Ação Contra a Mudança Global do Clima

O ODS 13 foi escolhido como principal porque o projeto utiliza dados climáticos para tornar mais compreensíveis condições associadas ao calor extremo. A proposta está ligada à conscientização e à adaptação aos impactos de eventos climáticos, transformando dados técnicos em informações mais acessíveis ao usuário.

### ODS relacionados

**ODS 3 - Saúde e Bem-Estar:** o calor extremo pode afetar a saúde e o bem-estar da população, tornando relevante a comunicação de condições de maior exposição.

**ODS 11 - Cidades e Comunidades Sustentáveis:** a análise e comunicação de condições climáticas em áreas urbanas contribui para a discussão sobre cidades mais preparadas para eventos climáticos extremos.

## 11. Stakeholders

- **Usuários da aplicação:** cidadãos interessados em consultar e compreender informações climáticas.
- **Gestores públicos e profissionais de sustentabilidade:** potenciais usuários dos dados para acompanhamento e comunicação de condições climáticas.
- **Organizações sociais e pesquisadores:** interessados em análises relacionadas a clima, saúde e cidades.
- **Responsável pelo desenvolvimento:** responsável pela coleta e processamento dos dados, desenvolvimento da aplicação, documentação e evolução da solução.

## 12. Escopo do projeto

### Escopo inicial - TP1

- Estruturação do projeto segundo o TDSP.
- Elaboração do Project Charter e do Data Summary Report.
- Configuração do ambiente de desenvolvimento Python.
- Integração com uma API pública de dados meteorológicos.
- Desenvolvimento de uma aplicação demonstrativa em Streamlit.
- Exibição de uma amostra dos dados utilizados.
- Disponibilização de links úteis relacionados ao projeto.

### Evolução prevista

- Inclusão de novas fontes de dados.
- Coleta de conteúdo textual por web scraping.
- Novas visualizações e recursos interativos.
- Desenvolvimento de API própria com FastAPI.
- Integração de modelos de linguagem e recursos de Inteligência Artificial.
- Geração automatizada de análises e insights relacionados ao contexto climático.

## 13. Metodologia

O projeto utilizará o **TDSP (Team Data Science Process)** como metodologia principal de organização e desenvolvimento.

As fases adotadas são:

1. Business Understanding
2. Data Ingest & Understanding
3. Modeling
4. Deployment
5. Acceptance

O **CRISP-DM** será utilizado como referência complementar para o ciclo de Ciência de Dados, sem duplicar a estrutura do projeto.

| CRISP-DM | TDSP |
|---|---|
| Business Understanding | Business Understanding |
| Data Understanding | Data Ingest & Understanding |
| Data Preparation | Data Ingest & Understanding |
| Modeling | Modeling |
| Evaluation | Modeling / Acceptance |
| Deployment | Deployment |
