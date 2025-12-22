import streamlit as st

def render_metrics(df):
    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()
    balance = income - expense

    col1, col2, col3 = st.columns(3)

    col1.metric("Receitas", f"R$ {income:,.2f}")
    col2.metric("Despesas", f"R$ {expense:,.2f}")
    col3.metric("Saldo", f"R$ {balance:,.2f}")
