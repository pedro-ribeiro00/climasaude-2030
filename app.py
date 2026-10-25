"""Ponto de entrada da aplicacao Streamlit multipagina."""

import streamlit as st

from climasaude.ui import (
    render_arquivos,
    render_clima,
    render_conteudo,
    render_inicio,
    render_projeto,
)


st.set_page_config(
    page_title="ClimaSaude 2030",
    page_icon="🌡️",
    layout="wide",
)

paginas = {
    "ClimaSaude 2030": [
        st.Page(render_inicio, title="Inicio", icon="🏠", default=True),
        st.Page(render_clima, title="Previsao climatica", icon="🌡️"),
    ],
    "Dados e analises": [
        st.Page(render_conteudo, title="Conteudo Web", icon="📰"),
        st.Page(render_arquivos, title="Upload e download", icon="📁"),
    ],
    "Documentacao": [
        st.Page(render_projeto, title="Sobre o projeto", icon="📘"),
    ],
}

navegacao = st.navigation(paginas, position="sidebar")
navegacao.run()
