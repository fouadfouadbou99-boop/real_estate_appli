# =====================================================
# REAL ESTATE INVESTMENT PLATFORM
# app.py
# =====================================================

import streamlit as st
import plotly.express as px
import pandas as pd

from config import DEFAULTS

from modules.debt import (
    debt_schedule
)

from modules.underwriting import (
    build_cashflows
)

from modules.valuation import (
    add_exit_to_cashflows,
    valuation_summary
)

from modules.metrics import (
    kpi_summary
)

from modules.risk import (
    risk_score,
    risk_category
)

from modules.portfolio import (
    portfolio_summary
)

from modules.montecarlo import (
    run_monte_carlo,
    monte_carlo_summary
)

# =====================================================
# CONFIG STREAMLIT
# =====================================================

st.set_page_config(
    page_title="Real Estate Investment Platform",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Real Estate Investment Platform")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⚙️ Hypothèses")

scenario = st.sidebar.selectbox(
    "Scénario",
    [
        "Stress",
        "Base",
        "Optimiste"
    ]
)

purchase_price = st.sidebar.number_input(
    "Prix acquisition",
    value=float(DEFAULTS["purchase_price"])
)

acquisition_fee_rate = (
    st.sidebar.number_input(
        "Frais acquisition (%)",
        value=float(DEFAULTS["acquisition_fee_rate"] * 100)
    ) / 100
)

capex = st.sidebar.number_input(
    "Travaux",
    value=float(DEFAULTS["capex"])
)

gross_rent_y1 = st.sidebar.number_input(
    "Loyer brut année 1",
    value=float(DEFAULTS["gross_rent_y1"])
)

rent_growth = (
    st.sidebar.number_input(
        "Croissance loyers (%)",
        value=float(DEFAULTS["rent_growth"] * 100)
    ) / 100
)

vacancy_rate = (
    st.sidebar.number_input(
        "Vacance (%)",
        value=float(DEFAULTS["vacancy_rate"] * 100)
    ) / 100
)

expense_rate = (
    st.sidebar.number_input(
        "Charges variables (%)",
        value=float(DEFAULTS["expense_rate"] * 100)
    ) / 100
)

# =====================================================
# PARAMETRES SCENARIOS
# =====================================================

if scenario == "Stress":

    rent_growth = 0.01
    vacancy_rate = 0.10
    exit_cap_rate = 0.08

elif scenario == "Optimiste":

    rent_growth = 0.04
    vacancy_rate = 0.03
    exit_cap_rate = 0.06

else:

    exit_cap_rate = DEFAULTS["exit_cap_rate"]

# =====================================================
# FINANCEMENT
# =====================================================

st.sidebar.subheader("Dette")

ltv = (
    st.sidebar.number_input(
        "Dette (%)",
        value=float(DEFAULTS["ltv"] * 100)
    ) / 100
)

debt_rate = (
    st.sidebar.number_input(
        "Taux dette (%)",
        value=float(DEFAULTS["debt_rate"] * 100)
    ) / 100
)

debt_term = st.sidebar.number_input(
    "Durée dette",
    value=int(DEFAULTS["debt_term"])
)

# =====================================================
# SORTIE
# =====================================================

st.sidebar.subheader("Cession")

holding_period = st.sidebar.number_input(
    "Horizon investissement",
    value=int(DEFAULTS["holding_period"])
)

sale_cost_rate = (
    st.sidebar.number_input(
        "Frais cession (%)",
        value=float(DEFAULTS["sale_cost_rate"] * 100)
    ) / 100
)

discount_rate = (
    st.sidebar.number_input(
        "Taux actualisation (%)",
        value=float(DEFAULTS["discount_rate"] * 100)
    ) / 100
)

# =====================================================
# CHARGES DETAILLEES
# =====================================================

st.sidebar.subheader("Charges détaillées")

taxe_fonciere = st.sidebar.number_input(
    "Taxe foncière",
    value=float(DEFAULTS["taxe_fonciere"])
)

assurance = st.sidebar.number_input(
    "Assurance",
    value=float(DEFAULTS["assurance"])
)

maintenance = st.sidebar.number_input(
    "Maintenance",
    value=float(DEFAULTS["maintenance"])
)

gestion_locative = st.sidebar.number_input(
    "Gestion locative",
    value=float(DEFAULTS["gestion_locative"])
)

inflation = (
    st.sidebar.number_input(
        "Inflation (%)",
        value=float(DEFAULTS["inflation_rate"] * 100)
    ) / 100
)

# =====================================================
# INVESTISSEMENT
# =====================================================

acquisition_fees = (
    purchase_price *
    acquisition_fee_rate
)

total_investment = (
    purchase_price +
    acquisition_fees +
    capex
)

loan_amount = (
    total_investment * ltv
)

equity_investment = (
    total_investment - loan_amount
)

# =====================================================
# DETTE
# =====================================================

debt_df = debt_schedule(
    loan_amount,
    debt_rate,
    int(debt_term)
)

annual_debt_service = (
    debt_df.iloc[0]["Annuity"]
)

# =====================================================
# CASH FLOWS
# =====================================================

cashflows_df = build_cashflows(

    rent_y1=gross_rent_y1,

    growth=rent_growth,

    vacancy=vacancy_rate,

    expense_rate=expense_rate,

    debt_service=annual_debt_service,

    holding_period=int(holding_period),

    taxe_fonciere=taxe_fonciere,

    assurance=assurance,

    maintenance=maintenance,

    gestion_locative=gestion_locative,

    inflation=inflation
)

cashflows_df = add_exit_to_cashflows(

    cashflows_df,

    debt_df,

    exit_cap_rate,

    sale_cost_rate
)

# =====================================================
# KPI
# =====================================================

kpis = kpi_summary(

    equity_investment=equity_investment,

    loan_amount=loan_amount,

    total_investment=total_investment,

    discount_rate=discount_rate,

    cashflows_df=cashflows_df
)

# =====================================================
# RISQUE
# =====================================================

risk = risk_score(
    vacancy_rate,
    ltv,
    debt_rate
)

# =====================================================
# DASHBOARD KPI
# =====================================================

st.subheader("📊 KPI")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "IRR",
    f"{kpis['IRR']} %"
)

col2.metric(
    "NPV",
    f"{kpis['NPV']:,.0f}"
)

col3.metric(
    "DSCR",
    f"{kpis['DSCR']}"
)

col4.metric(
    "Equity Multiple",
    f"{kpis['Equity Multiple']}x"
)

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Cap Rate",
    f"{kpis['Cap Rate']} %"
)

col6.metric(
    "Loan Yield",
    f"{kpis['Loan Yield']} %"
)

col7.metric(
    "Cash on Cash",
    f"{kpis['Cash on Cash']} %"
)

col8.metric(
    "Risk",
    risk_category(risk)
)

# =====================================================
# ONGLETS
# =====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Cash Flows",
        "Dette",
        "Valorisation",
        "Monte Carlo",
        "Portefeuille"
    ]
)

# =====================================================
# CASH FLOWS
# =====================================================

with tab1:

    st.dataframe(
        cashflows_df,
        use_container_width=True
    )

    fig_cf = px.bar(
        cashflows_df,
        x="Year",
        y="CF Equity",
        title="Cash Flow Equity"
    )

    st.plotly_chart(
        fig_cf,
        use_container_width=True
    )

# =====================================================
# DETTE
# =====================================================

with tab2:

    st.dataframe(
        debt_df,
        use_container_width=True
    )

    fig_debt = px.line(
        debt_df,
        x="Year",
        y="Closing Balance",
        title="Capital restant dû"
    )

    st.plotly_chart(
        fig_debt,
        use_container_width=True
    )

# =====================================================
# VALORISATION
# =====================================================

with tab3:

    terminal_noi = (
        cashflows_df.iloc[-1]["NOI"]
    )

    remaining_debt = (
        debt_df.iloc[-1]["Closing Balance"]
    )

    val = valuation_summary(

        terminal_noi,

        exit_cap_rate,

        sale_cost_rate,

        remaining_debt
    )

    st.json(val)

# =====================================================
# MONTE CARLO
# =====================================================

with tab4:

    st.subheader(
        "Simulation Monte Carlo"
    )

    simulations = st.slider(
        "Nombre simulations",
        100,
        10000,
        3000
    )

    mc_df = run_monte_carlo(

        simulations=simulations,

        equity_investment=equity_investment,

        debt_df=debt_df,

        base_rent=gross_rent_y1,

        growth_mean=rent_growth,

        growth_std=0.01,

        vacancy_mean=vacancy_rate,

        vacancy_std=0.02,

        expense_rate=expense_rate,

        debt_service=annual_debt_service,

        holding_period=int(holding_period),

        taxe_fonciere=taxe_fonciere,

        assurance=assurance,

        maintenance=maintenance,

        gestion_locative=gestion_locative,

        inflation=inflation,

        exit_cap_rate=exit_cap_rate,

        sale_cost_rate=sale_cost_rate
    )

    summary = monte_carlo_summary(
        mc_df
    )

    st.json(summary)

    fig_mc = px.histogram(
        mc_df,
        x="IRR",
        nbins=40,
        title="Distribution des TRI"
    )

    st.plotly_chart(
        fig_mc,
        use_container_width=True
    )

# =====================================================
# PORTEFEUILLE
# =====================================================

with tab5:

    portfolio_df = portfolio_summary()

    st.dataframe(
        portfolio_df,
        use_container_width=True
    )

    fig_portfolio = px.pie(
        portfolio_df,
        names="Asset",
        values="Value",
        title="Répartition du portefeuille"
    )

    st.plotly_chart(
        fig_portfolio,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")
st.caption(
    "Real Estate Investment Platform | Version Institutionnelle"
)
