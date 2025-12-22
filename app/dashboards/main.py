import streamlit as st
from app.dashboards.sidebar import render_sidebar
from app.dashboards.finance.finance_page import finance_page

st.set_page_config(
    page_title="Segundo Cérebro - Admin",
    layout="wide"
)

st.title("🧠 Segundo Cérebro — Painel Admin")

page = render_sidebar()

if page == "Financeiro":
    finance_page()
