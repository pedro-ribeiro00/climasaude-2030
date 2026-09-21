import streamlit as st
import pandas as pd
import requests


st.title("🌡️ ClimaSaúde 2030")

st.subheader("Monitoramento de condições associadas ao calor extremo")

st.write("""
O ClimaSaúde 2030 é uma aplicação em desenvolvimento que busca facilitar
a interpretação de dados climáticos relacionados à exposição ao calor.

A solução utiliza dados públicos para apresentar informações como
temperatura, sensação térmica e índice UV, contribuindo para a compreensão
de condições climáticas que podem afetar a saúde e o bem-estar da população.
""")


st.subheader("Objetivos")

st.write("""
- Coletar dados climáticos através de APIs públicas.
- Apresentar indicadores climáticos de maneira simples e acessível.
- Auxiliar na identificação de condições associadas ao calor extremo.
- Evoluir futuramente para uma solução capaz de gerar análises utilizando IA.
""")


# Coordenadas de São Paulo
latitude = -23.5505
longitude = -46.6333

# Endpoint da Open-Meteo Weather API
url = "https://api.open-meteo.com/v1/forecast"

# Parâmetros enviados para a API
parametros = {
    "latitude": latitude,
    "longitude": longitude,
    "daily": "temperature_2m_max,apparent_temperature_max,uv_index_max,precipitation_sum",
    "timezone": "America/Sao_Paulo"
}

# Realiza a consulta à API
resposta = requests.get(
    url,
    params=parametros,
    timeout=10
)

# Interrompe a execução caso a API retorne um erro HTTP
resposta.raise_for_status()

# Converte a resposta JSON para um dicionário Python
dados = resposta.json()

# Organiza os dados em um DataFrame
df_clima = pd.DataFrame({
    "Data": dados["daily"]["time"],
    "Temperatura Máxima (°C)": dados["daily"]["temperature_2m_max"],
    "Sensação Térmica Máxima (°C)": dados["daily"]["apparent_temperature_max"],
    "Índice UV Máximo": dados["daily"]["uv_index_max"],
    "Precipitação (mm)": dados["daily"]["precipitation_sum"]
})


st.subheader("Amostra dos dados climáticos")

st.write("""
Dados meteorológicos previstos para São Paulo obtidos através da
Open-Meteo Weather API.
""")

st.dataframe(
    df_clima,
    hide_index=True
)


st.subheader("Links úteis")

st.markdown("""
- [Objetivos de Desenvolvimento Sustentável - ONU](https://sdgs.un.org/goals)
- [Open-Meteo Weather API](https://open-meteo.com/)
- [IBGE](https://www.ibge.gov.br/)
- [Conecta Brasil](https://conectabrasil.org/home)
- [Observatório do Terceiro Setor](https://observatorio3setor.org.br/)
""")