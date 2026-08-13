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
# SIDEBAR - HYPOTHESES
# =====================================================

st.sidebar.title("⚙️ Hypothèses")

scenario = st.sidebar.selectbox(
    "Scénario",
    [
        "Stress",
        "Base",
        "Optimiste"
    ],
    index=1
)

purchase_price = st.sidebar.number_input(
    "Prix acquisition",
    value=float(DEFAULTS["purchase_price"])
)

acquisition_fee_rate = (
    st.sidebar.number_input(
        "Frais acquisition (%)",
        value=float(
            DEFAULTS["acquisition_fee_rate"] * 100
        )
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
        value=float(
            DEFAULTS["rent_growth"] * 100
        )
    ) / 100
)

vacancy_rate = (
    st.sidebar.number_input(
        "Vacance (%)",
        value=float(
            DEFAULTS["vacancy_rate"] * 100
        )
    ) / 100
)

expense_rate = (
    st.sidebar.number_input(
        "Charges variables (%)",
        value=float(
            DEFAULTS["expense_rate"] * 100
        )
    ) / 100
)

# =====================================================
# SCENARIOS
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
# PARAMETRES DETTE
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

debt_term = int(
    st.sidebar.number_input(
        "Durée dette (années)",
        value=DEFAULTS["debt_term"]
    )
)

# =====================================================
# SORTIE
# =====================================================

st.sidebar.subheader("Sortie")

holding_period = int(
    st.sidebar.number_input(
        "Horizon investissement",
        value=DEFAULTS["holding_period"]
    )
)

sale_cost_rate = (
    st.sidebar.number_input(
        "Frais de cession (%)",
        value=float(
            DEFAULTS["sale_cost_rate"] * 100
        )
    ) / 100
)

discount_rate = (
    st.sidebar.number_input(
        "Taux actualisation (%)",
        value=float(
            DEFAULTS["discount_rate"] * 100
        )
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
        value=float(
            DEFAULTS["inflation_rate"] * 100
        )
    ) / 100
)

# =====================================================
# INVESTISSEMENT INITIAL
# =====================================================

acquisition_fees = (
    purchase_price *
    acquisition_fee_rate
)

total_investment = (
    purchase_price
    + acquisition_fees
    + capex
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
    debt_term
)

annual_debt_service = (
    debt_df.iloc[0]["Annuity"]
)
