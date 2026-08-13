import streamlit as st
import pandas as pd
import plotly.express as px

from config import DEFAULTS
from debt import debt_schedule
from underwriting import build_cashflows
from portfolio import portfolio_summary
from risk import (
    risk_score,
    risk_category
)

st.set_page_config(
    page_title="Real Estate Platform",
    layout="wide"
)

st.title(
    "🏢 Real Estate Investment Platform"
)

purchase_price = st.sidebar.number_input(
    "Prix acquisition",
    value=DEFAULTS["purchase_price"]
)

ltv = st.sidebar.slider(
    "LTV",
    0.0,
    1.0,
    DEFAULTS["ltv"]
)

loan_amount = purchase_price * ltv

debt_df = debt_schedule(
    loan_amount,
    DEFAULTS["debt_rate"],
    DEFAULTS["debt_term"]
)

annuity = debt_df.iloc[0]["Annuity"]

cashflow_df = build_cashflows(
    DEFAULTS["gross_rent_y1"],
    DEFAULTS["rent_growth"],
    DEFAULTS["vacancy_rate"],
    DEFAULTS["expense_rate"],
    annuity,
    DEFAULTS["holding_period"]
)

score = risk_score(
    DEFAULTS["vacancy_rate"],
    ltv,
    DEFAULTS["debt_rate"]
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Risk Score",
    score
)

col2.metric(
    "Risk Category",
    risk_category(score)
)

col3.metric(
    "Loan Amount",
    f"{loan_amount:,.0f}"
)

st.subheader(
    "Cash Flows"
)

fig = px.bar(
    cashflow_df,
    x="Year",
    y="CF Equity"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader(
    "Debt Schedule"
)

st.dataframe(
    debt_df,
    use_container_width=True
)

st.subheader(
    "Portfolio"
)

st.dataframe(
    portfolio_summary(),
    use_container_width=True
)
