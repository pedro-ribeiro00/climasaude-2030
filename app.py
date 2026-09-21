from collections import Counter
from io import BytesIO
from pathlib import Path
import re

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
from wordcloud import WordCloud


st.set_page_config(
    page_title="ClimaSaude 2030",
    page_icon="🌡️",
    layout="wide",
)

CIDADES = {
    "Sao Paulo - SP": (-23.5505, -46.6333),
    "Rio de Janeiro - RJ": (-22.9068, -43.1729),
    "Belo Horizonte - MG": (-19.9167, -43.9345),
    "Brasilia - DF": (-15.7939, -47.8828),
    "Porto Alegre - RS": (-30.0346, -51.2177),
}

STOPWORDS = {
    "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do", "dos",
    "e", "em", "entre", "é", "essa", "esse", "esta", "este", "foi", "mais",
    "na", "nas", "no", "nos", "o", "os", "ou", "para", "pela", "pelas",
    "pelo", "pelos", "por", "que", "se", "sem", "ser", "sua", "suas", "um",
    "uma", "the", "and", "of", "to", "in", "is", "are", "for", "on", "with",
    "as", "from", "by", "can", "be", "an", "at", "or", "that", "this",
}


@st.cache_data(ttl=1800, show_spinner=False)
def carregar_clima(latitude: float, longitude: float) -> pd.DataFrame:
    """Consulta a Open-Meteo e retorna a previsao diaria em DataFrame."""
    url = "https://api.open-meteo.com/v1/forecast"
    parametros = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": (
            "temperature_2m_max,apparent_temperature_max,"
            "uv_index_max,precipitation_sum"
        ),
        "timezone": "America/Sao_Paulo",
        "forecast_days": 7,
    }

    resposta = requests.get(url, params=parametros, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()["daily"]

    df = pd.DataFrame(
        {
            "Data": pd.to_datetime(dados["time"]),
            "Temperatura Maxima (°C)": dados["temperature_2m_max"],
            "Sensacao Termica Maxima (°C)": dados["apparent_temperature_max"],
            "Indice UV Maximo": dados["uv_index_max"],
            "Precipitacao (mm)": dados["precipitation_sum"],
        }
    )
    return df


@st.cache_data(ttl=300, show_spinner=False)
def carregar_conteudo_web(caminho: str) -> pd.DataFrame:
    arquivo = Path(caminho)
    if not arquivo.exists():
        return pd.DataFrame()
    return pd.read_csv(arquivo)


def dataframe_para_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def palavras_frequentes(textos: pd.Series, limite: int = 12) -> pd.DataFrame:
    texto = " ".join(textos.dropna().astype(str).tolist()).lower()
    palavras = re.findall(r"[a-zA-ZÀ-ÿ]{4,}", texto)
    contagem = Counter(p for p in palavras if p not in STOPWORDS)
    return pd.DataFrame(contagem.most_common(limite), columns=["palavra", "frequencia"])


def criar_wordcloud(textos: pd.Series):
    texto = " ".join(textos.dropna().astype(str).tolist())
    if not texto.strip():
        return None

    return WordCloud(
        width=1200,
        height=500,
        background_color="white",
        stopwords=STOPWORDS,
        collocations=False,
    ).generate(texto)


# Estado de sessao: preserva upload e historico de cidades durante a navegacao.
if "dados_upload" not in st.session_state:
    st.session_state.dados_upload = None

if "historico_cidades" not in st.session_state:
    st.session_state.historico_cidades = []

if "ultima_cidade" not in st.session_state:
    st.session_state.ultima_cidade = None


st.title("🌡️ ClimaSaude 2030")
st.subheader("Monitoramento de condicoes associadas ao calor extremo")

st.write(
    """
O ClimaSaude 2030 transforma dados climaticos e conteudo publico sobre calor e
saude em informacoes mais acessiveis. Nesta etapa, o projeto combina API,
web scraping, visualizacoes, cache, estado de sessao e upload/download de CSV.
"""
)

with st.sidebar:
    st.header("Consulta")
    cidade = st.selectbox("Escolha uma cidade", list(CIDADES.keys()))
    st.caption("A previsao e obtida da Open-Meteo e fica em cache por 30 minutos.")

    if cidade != st.session_state.ultima_cidade:
        st.session_state.historico_cidades.append(cidade)
        st.session_state.historico_cidades = st.session_state.historico_cidades[-5:]
        st.session_state.ultima_cidade = cidade

    if st.session_state.historico_cidades:
        st.write("**Ultimas consultas nesta sessao:**")
        for item in reversed(st.session_state.historico_cidades):
            st.write(f"- {item}")

aba_clima, aba_web, aba_arquivos, aba_projeto = st.tabs(
    ["Clima", "Conteudo Web", "Upload e Download", "Sobre o projeto"]
)


with aba_clima:
    latitude, longitude = CIDADES[cidade]

    try:
        with st.spinner("Consultando dados climaticos..."):
            df_clima = carregar_clima(latitude, longitude)

        st.subheader(f"Previsao de 7 dias - {cidade}")

        primeira_linha = df_clima.iloc[0]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Temp. maxima", f"{primeira_linha['Temperatura Maxima (°C)']:.1f} °C")
        col2.metric(
            "Sensacao maxima",
            f"{primeira_linha['Sensacao Termica Maxima (°C)']:.1f} °C",
        )
        col3.metric("UV maximo", f"{primeira_linha['Indice UV Maximo']:.1f}")
        col4.metric("Precipitacao", f"{primeira_linha['Precipitacao (mm)']:.1f} mm")

        st.dataframe(df_clima, hide_index=True, use_container_width=True)

        st.subheader("Temperatura ao longo da semana")
        grafico_clima = df_clima.set_index("Data")[[
            "Temperatura Maxima (°C)",
            "Sensacao Termica Maxima (°C)",
        ]]
        st.line_chart(grafico_clima)

        st.download_button(
            "Baixar previsao em CSV",
            data=dataframe_para_csv(df_clima),
            file_name=f"previsao_{cidade.split(' - ')[0].lower().replace(' ', '_')}.csv",
            mime="text/csv",
        )

    except requests.RequestException as exc:
        st.error(f"Nao foi possivel consultar a API climatica: {exc}")


with aba_web:
    st.subheader("Conteudo publico sobre calor e saude")
    caminho_web = "data/raw/conteudo_calor_saude.csv"
    df_web = carregar_conteudo_web(caminho_web)

    if df_web.empty:
        st.warning(
            "O arquivo de scraping ainda nao foi encontrado. Execute: "
            "`python scripts/scrape_heat_content.py`"
        )
    else:
        fontes = sorted(df_web["fonte"].dropna().unique().tolist())
        fontes_escolhidas = st.multiselect(
            "Filtrar fontes",
            options=fontes,
            default=fontes,
        )

        df_filtrado = df_web[df_web["fonte"].isin(fontes_escolhidas)].copy()

        # Caso o CSV enviado pelo usuario possua uma coluna texto, ele complementa a analise.
        textos_analise = df_filtrado[["texto"]].copy()
        textos_analise["origem"] = "web scraping"

        if (
            isinstance(st.session_state.dados_upload, pd.DataFrame)
            and "texto" in st.session_state.dados_upload.columns
        ):
            textos_upload = st.session_state.dados_upload[["texto"]].copy()
            textos_upload["origem"] = "upload"
            textos_analise = pd.concat([textos_analise, textos_upload], ignore_index=True)

        total_palavras = int(
            textos_analise["texto"].fillna("").astype(str).str.split().str.len().sum()
        )

        m1, m2, m3 = st.columns(3)
        m1.metric("Blocos coletados", len(df_filtrado))
        m2.metric("Fontes", df_filtrado["fonte"].nunique())
        m3.metric("Palavras analisadas", total_palavras)

        st.subheader("Amostra do conteudo extraido")
        st.dataframe(
            df_filtrado[["fonte", "tipo_elemento", "texto"]].head(20),
            hide_index=True,
            use_container_width=True,
        )

        st.subheader("Palavras mais frequentes")
        df_palavras = palavras_frequentes(textos_analise["texto"])
        if not df_palavras.empty:
            st.bar_chart(df_palavras.set_index("palavra"))
            st.dataframe(df_palavras, hide_index=True, use_container_width=True)

        st.subheader("Nuvem de palavras")
        nuvem = criar_wordcloud(textos_analise["texto"])
        if nuvem is not None:
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.imshow(nuvem, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.download_button(
            "Baixar conteudo extraido em CSV",
            data=dataframe_para_csv(df_filtrado),
            file_name="conteudo_calor_saude.csv",
            mime="text/csv",
        )


with aba_arquivos:
    st.subheader("Adicionar dados por CSV")
    st.write(
        "Envie um CSV para complementar a exploracao. Se o arquivo possuir uma coluna "
        "`texto`, ela tambem sera incorporada às estatisticas e à nuvem de palavras."
    )

    arquivo = st.file_uploader("Selecione um arquivo CSV", type=["csv"])

    if arquivo is not None:
        try:
            df_upload = pd.read_csv(arquivo)
            st.session_state.dados_upload = df_upload
            st.success(f"Arquivo carregado: {len(df_upload)} linhas e {len(df_upload.columns)} colunas.")
        except Exception as exc:
            st.error(f"Nao foi possivel ler o CSV: {exc}")

    if isinstance(st.session_state.dados_upload, pd.DataFrame):
        df_upload = st.session_state.dados_upload
        st.dataframe(df_upload.head(50), hide_index=True, use_container_width=True)

        st.write("**Resumo das colunas:**")
        resumo = pd.DataFrame(
            {
                "coluna": df_upload.columns,
                "tipo": [str(tipo) for tipo in df_upload.dtypes],
                "nulos": df_upload.isna().sum().values,
            }
        )
        st.dataframe(resumo, hide_index=True, use_container_width=True)

        st.download_button(
            "Baixar copia do CSV carregado",
            data=dataframe_para_csv(df_upload),
            file_name="dados_upload.csv",
            mime="text/csv",
        )

        if st.button("Limpar arquivo da sessao"):
            st.session_state.dados_upload = None
            st.rerun()


with aba_projeto:
    st.subheader("Problema de negocio")
    st.write(
        "Dados sobre clima e calor extremo existem, mas nem sempre chegam ao usuario de "
        "forma integrada e facil de interpretar. O projeto organiza informacoes climaticas "
        "e conteudo publico sobre saude para apoiar a compreensao dessas condicoes."
    )

    st.subheader("ODS e ESG")
    st.write(
        "O projeto se relaciona principalmente ao ODS 13 - Acao Contra a Mudanca Global "
        "do Clima, com conexoes aos ODS 3 - Saude e Bem-Estar e ODS 11 - Cidades e "
        "Comunidades Sustentaveis."
    )

    st.subheader("Links uteis")
    st.markdown(
        """
- [Objetivos de Desenvolvimento Sustentavel - ONU](https://sdgs.un.org/goals)
- [Open-Meteo Weather API](https://open-meteo.com/)
- [Ministerio da Saude - Ondas de Calor](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/o/ondas-de-calor)
- [WHO - Heat and Health](https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health)
- [Repositorio do projeto no GitHub](https://github.com/pedro-ribeiro00/climasaude-2030)
"""
    )
