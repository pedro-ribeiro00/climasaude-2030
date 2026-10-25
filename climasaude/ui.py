"""Paginas da interface Streamlit."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud

from climasaude.analysis import STOPWORDS
from climasaude.api_client import (
    APIIndisponivel,
    analisar_textos_api,
    obter_previsao_api,
)
from climasaude.config import CIDADES


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTEUDO_CSV = PROJECT_ROOT / "data" / "raw" / "conteudo_calor_saude.csv"


def _iniciar_sessao() -> None:
    if "dados_upload" not in st.session_state:
        st.session_state.dados_upload = None
    if "historico_cidades" not in st.session_state:
        st.session_state.historico_cidades = []


def _csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


@st.cache_data(ttl=1800, show_spinner=False)
def _previsao_em_cache(cidade_id: str) -> dict:
    return obter_previsao_api(cidade_id)


@st.cache_data(ttl=300, show_spinner=False)
def _carregar_conteudo(caminho: str) -> pd.DataFrame:
    arquivo = Path(caminho)
    return pd.read_csv(arquivo) if arquivo.exists() else pd.DataFrame()


def _titulo(subtitulo: str) -> None:
    st.title("🌡️ ClimaSaude 2030")
    st.caption(subtitulo)


def render_inicio() -> None:
    _iniciar_sessao()
    _titulo("Dados climaticos e informacao publica para compreender o calor extremo")
    st.write(
        "A aplicacao integra previsoes meteorologicas, conteudo de fontes publicas "
        "e analises textuais em uma experiencia multipagina. Use o menu lateral "
        "para navegar pelas funcionalidades."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Cidades cadastradas", len(CIDADES))
    col2.metric("Fontes Web", 2)
    col3.metric("Horizonte da previsao", "7 dias")

    st.subheader("Como a solucao funciona")
    st.markdown(
        """
1. A **FastAPI** centraliza a consulta climatica e a analise de textos.
2. O **Streamlit** consome essa API e apresenta os resultados em paginas independentes.
3. O **Beautiful Soup** coleta conteudo publico e preserva fonte, URL e data da coleta.
4. Os arquivos tratados ficam prontos para exploracao e futura integracao com LLM.
"""
    )
    st.info(
        "Conteudo educativo: os indicadores e textos nao substituem alertas oficiais "
        "nem orientacao de profissionais de saude."
    )


def render_clima() -> None:
    _iniciar_sessao()
    _titulo("Previsao climatica fornecida pela FastAPI do projeto")

    nomes = {cidade.nome: cidade_id for cidade_id, cidade in CIDADES.items()}
    nome = st.selectbox("Escolha uma cidade", list(nomes))
    cidade_id = nomes[nome]

    if not st.session_state.historico_cidades or st.session_state.historico_cidades[-1] != nome:
        st.session_state.historico_cidades.append(nome)
        st.session_state.historico_cidades = st.session_state.historico_cidades[-5:]

    try:
        with st.spinner("Consultando a API do ClimaSaude..."):
            resposta = _previsao_em_cache(cidade_id)
    except APIIndisponivel as exc:
        st.error(str(exc))
        return

    df = pd.DataFrame(resposta["previsao"]).rename(
        columns={
            "data": "Data",
            "temperatura_max_c": "Temperatura Maxima (°C)",
            "sensacao_max_c": "Sensacao Termica Maxima (°C)",
            "uv_max": "Indice UV Maximo",
            "precipitacao_mm": "Precipitacao (mm)",
        }
    )
    df["Data"] = pd.to_datetime(df["Data"])
    hoje = df.iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temp. maxima", f"{hoje['Temperatura Maxima (°C)']:.1f} °C")
    c2.metric("Sensacao maxima", f"{hoje['Sensacao Termica Maxima (°C)']:.1f} °C")
    c3.metric("UV maximo", f"{hoje['Indice UV Maximo']:.1f}")
    c4.metric("Precipitacao", f"{hoje['Precipitacao (mm)']:.1f} mm")

    st.dataframe(df, hide_index=True, width="stretch")
    st.line_chart(
        df.set_index("Data")[[
            "Temperatura Maxima (°C)",
            "Sensacao Termica Maxima (°C)",
        ]]
    )
    st.download_button(
        "Baixar previsao em CSV",
        data=_csv_bytes(df),
        file_name=f"previsao_{cidade_id}.csv",
        mime="text/csv",
    )

    with st.expander("Historico desta sessao"):
        for item in reversed(st.session_state.historico_cidades):
            st.write(f"- {item}")


def render_conteudo() -> None:
    _iniciar_sessao()
    _titulo("Conteudo coletado com Beautiful Soup e analisado pela FastAPI")
    df = _carregar_conteudo(str(CONTEUDO_CSV))
    if df.empty:
        st.warning("Execute `python scripts/scrape_heat_content.py` para gerar os dados.")
        return

    fontes = sorted(df["fonte"].dropna().unique())
    selecionadas = st.multiselect("Filtrar fontes", fontes, default=fontes)
    filtrado = df[df["fonte"].isin(selecionadas)].copy()

    if filtrado.empty:
        st.info("Selecione ao menos uma fonte para gerar a analise.")
        return

    textos = filtrado["texto"].dropna().astype(str).tolist()
    upload = st.session_state.dados_upload
    if isinstance(upload, pd.DataFrame) and "texto" in upload.columns:
        textos.extend(upload["texto"].dropna().astype(str).tolist())

    if not textos:
        st.info("Nao ha textos validos para analisar com os filtros atuais.")
        return

    try:
        analise = analisar_textos_api(textos)
    except APIIndisponivel as exc:
        st.error(str(exc))
        return

    m1, m2, m3 = st.columns(3)
    m1.metric("Blocos coletados", len(filtrado))
    m2.metric("Fontes", filtrado["fonte"].nunique())
    m3.metric("Palavras analisadas", analise["total_palavras"])

    st.subheader("Amostra rastreavel")
    st.dataframe(
        filtrado[["fonte", "tipo_elemento", "texto", "url"]].head(25),
        hide_index=True,
        width="stretch",
    )

    frequencias = pd.DataFrame(analise["palavras_frequentes"])
    if not frequencias.empty:
        st.subheader("Palavras mais frequentes")
        st.bar_chart(frequencias.set_index("palavra"))

    if textos:
        st.subheader("Nuvem de palavras")
        nuvem = WordCloud(
            width=1200,
            height=500,
            background_color="white",
            stopwords=STOPWORDS,
            collocations=False,
        ).generate(" ".join(textos))
        figura, eixo = plt.subplots(figsize=(12, 5))
        eixo.imshow(nuvem, interpolation="bilinear")
        eixo.axis("off")
        st.pyplot(figura, width="stretch")
        plt.close(figura)

    st.download_button(
        "Baixar conteudo filtrado",
        data=_csv_bytes(filtrado),
        file_name="conteudo_calor_saude.csv",
        mime="text/csv",
    )


def render_arquivos() -> None:
    _iniciar_sessao()
    _titulo("Envio, exploracao e download de arquivos CSV")
    st.write(
        "O arquivo permanece apenas na sessao atual. Se houver uma coluna `texto`, "
        "ela complementa a analise da pagina Conteudo Web."
    )
    arquivo = st.file_uploader("Selecione um CSV", type=["csv"])
    if arquivo is not None:
        try:
            st.session_state.dados_upload = pd.read_csv(arquivo)
            st.success("Arquivo carregado com sucesso.")
        except (pd.errors.ParserError, UnicodeDecodeError, ValueError) as exc:
            st.error(f"Nao foi possivel ler o CSV: {exc}")

    df = st.session_state.dados_upload
    if not isinstance(df, pd.DataFrame):
        return

    st.dataframe(df.head(100), hide_index=True, width="stretch")
    resumo = pd.DataFrame(
        {
            "coluna": df.columns,
            "tipo": [str(tipo) for tipo in df.dtypes],
            "nulos": df.isna().sum().values,
            "unicos": [df[coluna].nunique(dropna=True) for coluna in df.columns],
        }
    )
    st.subheader("Resumo das colunas")
    st.dataframe(resumo, hide_index=True, width="stretch")
    st.download_button(
        "Baixar copia do CSV",
        data=_csv_bytes(df),
        file_name="dados_upload.csv",
        mime="text/csv",
    )
    if st.button("Limpar arquivo da sessao"):
        st.session_state.dados_upload = None
        st.rerun()


def render_projeto() -> None:
    _titulo("Escopo, arquitetura e proximos passos")
    st.subheader("Problema de negocio")
    st.write(
        "Dados climaticos e orientacoes sobre calor existem em fontes separadas. "
        "O projeto os organiza em uma interface acessivel, com rastreabilidade e "
        "separacao entre apresentacao, API e fontes externas."
    )
    st.subheader("Arquitetura do TP3")
    st.code(
        "Open-Meteo → FastAPI → Streamlit\n"
        "Paginas publicas → Beautiful Soup → CSV/TXT → FastAPI → Streamlit",
        language="text",
    )
    st.subheader("Preparacao para LLM")
    st.write(
        "A base textual preserva fonte e URL para futura recuperacao com citacoes. "
        "O plano de integracao preve RAG, validacao de respostas, privacidade e "
        "avisos contra interpretacao medica indevida."
    )
    st.markdown(
        """
- [Open-Meteo](https://open-meteo.com/)
- [Ministerio da Saude - Ondas de Calor](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/o/ondas-de-calor)
- [WHO - Heat and Health](https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health)
- [Repositorio GitHub](https://github.com/pedro-ribeiro00/climasaude-2030)
"""
    )
