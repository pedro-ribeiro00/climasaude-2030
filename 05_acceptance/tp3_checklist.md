# Checklist de aceitação — TP3

Este documento relaciona os itens solicitados à evidência presente no repositório. A validação automática complementar é executada por `python scripts/validate_tp3.py` e pelos testes em `tests/`.

| Item da rubrica | Status | Evidência |
|---|---|---|
| Revisar o Project Charter | Atendido | `01_business_understanding/project_charter.md`, seção TP3 |
| Revisar o Data Summary Report | Atendido | `02_data_ingest_understanding/data_summary_report.md`, fontes, esquema e qualidade |
| Reavaliar problema e metas | Atendido | Charter e README atualizados para a arquitetura FastAPI + Streamlit |
| Documentar fontes de scraping | Atendido | Data Summary Report e `scripts/scrape_heat_content.py` |
| Aplicação Streamlit multipágina | Atendido | `app.py` usa `st.navigation` e cinco páginas funcionais |
| Menu de navegação | Atendido | Menu lateral agrupado em interface, dados e documentação |
| Funcionalidades diferentes por página | Atendido | Previsão, conteúdo Web, análise, upload/download e documentação |
| FastAPI com rota GET | Atendido | `GET /previsao/{cidade_id}`, além de `/health` e `/cidades` |
| FastAPI com rota POST | Atendido | `POST /analises/texto` com validação Pydantic |
| Integração Streamlit ↔ FastAPI | Atendido | `climasaude/api_client.py` consumido nas páginas de clima e conteúdo |
| Web scraping | Atendido | Beautiful Soup, limpeza, deduplicação e persistência CSV/TXT |
| Avaliação de Selenium | Atendido | Não utilizado; justificativa técnica no README e Data Summary Report |
| Preparação para LLM | Atendido | `03_modeling/llm_integration_plan.md` e metadados rastreáveis no corpus |
| Testes e validação | Atendido | Testes unitários/API e `scripts/validate_tp3.py` |
| Reprodutibilidade | Atendido | `requirements.txt`, `scripts/prepare_tp3.sh` e instruções no README |

## Critérios manuais de aceite

- A documentação interativa da API abre em `http://127.0.0.1:8000/docs`.
- O menu lateral permite acessar as cinco páginas sem perder o CSV da sessão.
- A página de previsão mostra sete dias e permite baixar o resultado.
- A página de conteúdo filtra fontes, chama a rota POST e oferece download.
- O upload aceita o arquivo de exemplo e exibe resumo das colunas.
- Mensagens orientam o usuário quando a API local não está em execução.

## Limites declarados

A aplicação depende de fontes externas e não representa um sistema oficial de alerta. Conteúdo sobre saúde é apenas educativo. A futura funcionalidade de LLM deverá conservar essas limitações e citar suas fontes.
