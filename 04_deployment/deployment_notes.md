# Execução do ClimaSaúde 2030

Repositório: https://github.com/pedro-ribeiro00/climasaude-2030

A aplicação executa localmente dois processos: **FastAPI** e **Streamlit**. O arquivo `requirements.txt` lista as bibliotecas, e o README apresenta os comandos para instalar as dependências, baixar o Qwen e iniciar os serviços.

A API utiliza, por padrão, http://127.0.0.1:8000. O Streamlit acessa essa API para consultar as previsões, analisar textos e pedir a síntese. O scraping é executado separadamente para atualizar o CSV.

Os testes funcionais de **23/11/2026** usaram dados externos e o Qwen local. Os resultados estão em `05_acceptance/`. A aplicação não foi publicada como serviço Web. A inspeção visual no navegador e o upload/download pela interface ainda precisam ser conferidos em um ambiente com acesso à página.
