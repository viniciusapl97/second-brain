import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.header("📊 Módulos")
        page = st.radio(
            "Selecione:",
            ["Financeiro", "Memória (em breve)", "Relatórios (em breve)"]
        )
    return page
