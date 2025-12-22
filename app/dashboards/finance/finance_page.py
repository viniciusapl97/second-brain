import streamlit as st
import pandas as pd
from datetime import date
from app.modules.finance.repository import FinanceRepository
from app.dashboards.finance.finance_metrics import render_metrics

def finance_page():
    st.subheader("💰 Financeiro")

    repo = FinanceRepository()

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Data inicial", date.today().replace(day=1))
    with col2:
        end_date = st.date_input("Data final", date.today())

    transactions = repo.list_by_period(start_date, end_date)

    if not transactions:
        st.warning("Nenhuma transação encontrada.")
        return

    df = pd.DataFrame(transactions)

    render_metrics(df)

    st.dataframe(
        df.sort_values("date", ascending=False),
        use_container_width=True
    )
