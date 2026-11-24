# ClimaSaúde 2030

Projeto da disciplina **Projeto de Bloco - Inteligência Artificial Aplicada**.

## Sobre o projeto

O ClimaSaúde 2030 reúne previsões do tempo e informações públicas sobre calor e saúde. O objetivo é facilitar a consulta desses conteúdos, que normalmente estão em fontes diferentes. A aplicação é educativa: não substitui alertas oficiais nem orientação médica.

## Funcionalidades

- Previsão de sete dias para São Paulo, Rio de Janeiro, Belo Horizonte, Brasília e Porto Alegre.
- Indicadores e gráficos de temperatura, sensação térmica, índice UV e precipitação.
- Textos do Ministério da Saúde e da Organização Mundial da Saúde (OMS), coletados por scraping.
- Frequência de palavras, nuvem de palavras e upload/download de CSV.
- Resumo livre de um texto informado pelo usuário (TP4).
- **Painel final (TP5)** com seleção automática de trechos das fontes, considerando a previsão da cidade.

O painel final utiliza uma **síntese extrativa**: apresenta as palavras e o idioma dos textos originais. A previsão vem da Open-Meteo e não é criada pelo modelo.

## Como executar

Requer Python 3.10 ou superior. Na pasta do projeto, crie um ambiente virtual e instale as dependências:

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

No Windows, ative o ambiente com .venv\Scripts\activate.

Baixe o Qwen uma vez:

    python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='Qwen/Qwen2.5-0.5B-Instruct', allow_patterns=['*.json', '*.safetensors', '*.txt', '*.model', '*.tiktoken'])"

Inicie a API e o Streamlit em dois terminais diferentes:

    uvicorn api.main:app --reload

    streamlit run app.py

A documentação das rotas está em http://127.0.0.1:8000/docs. A inferência do modelo funciona com os arquivos locais depois do download; a previsão e o scraping precisam de internet.

Para atualizar os textos coletados:

    python scripts/scrape_heat_content.py

O scraper não é executado quando o painel abre. O arquivo data/sample_upload.csv é apenas um exemplo para a página de upload.

## Código e fontes

| Arquivo | Função |
|---|---|
| app.py e climasaude/ui.py | Interface Streamlit |
| api/main.py | API do projeto |
| climasaude/weather.py | Dados da Open-Meteo |
| scripts/scrape_heat_content.py | Coleta das páginas públicas |
| climasaude/llm.py e climasaude/tp5.py | Modelo e síntese |
| data/raw/ | Textos coletados |

A FastAPI oferece GET /health, GET /cidades, GET /previsao/{cidade_id}, POST /analises/texto, POST /processar_texto e POST /sintese.

Fontes: https://open-meteo.com/ ; https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/o/ondas-de-calor ; https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health

Modelo: https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct

## Documentação e testes

Os documentos TDSP estão nas pastas 01_business_understanding a 05_acceptance. Os resultados de testes estão em 05_acceptance/validacao_tp5.md e 05_acceptance/evidencias/. Para repetir os testes funcionais, use scripts/validar_tp5.py e scripts/validar_interface_tp5.py após preparar o ambiente.

A validação com dados externos e modelo real ocorreu em 23/11/2026. A inspeção visual no navegador e os testes de upload/download pela interface ainda estão pendentes.

O projeto se relaciona ao ODS 13, com conexões aos ODS 3 e 11. O ChatGPT foi usado como apoio no planejamento, desenvolvimento e revisão; as informações apresentadas pela aplicação devem ser verificadas nas fontes.
