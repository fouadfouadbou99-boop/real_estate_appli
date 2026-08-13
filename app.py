import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from numpy_financial import irr, npv
from io import BytesIO

# ============================================================================
# CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Real Estate Investment Platform",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Real Estate Investment Platform")
st.markdown("### Modélisation et analyse d'investissements immobiliers")

# ============================================================================
# SIDEBAR
# ============================================================================

st.sidebar.header("Hypothèses")

purchase_price = st.sidebar.number_input(
    "Prix d'acquisition",
    value=1_000_000.0,
    step=10000.0
)

acquisition_fee_rate = st.sidebar.slider(
    "Frais d'acquisition (%)",
    0.0,
    20.0,
    8.0
) / 100

capex = st.sidebar.number_input(
    "Travaux",
    value=100_000.0,
    step=5000.0
)

gross_rent_y1 = st.sidebar.number_input(
    "Loyer brut Année 1",
    value=120_000.0
)

rent_growth = st.sidebar.slider(
    "Croissance des loyers (%)",
    0.0,
    10.0,
    2.0
) / 100

vacancy_rate = st.sidebar.slider(
    "Vacance (%)",
    0.0,
    20.0,
    5.0
) / 100

expense_rate = st.sidebar.slider(
    "Charges (%)",
    0.0,
    50.0,
    20.0
) / 100

ltv = st.sidebar.slider(
    "LTV (%)",
    0.0,
    90.0,
    70.0
) / 100

interest_rate = st.sidebar.slider(
    "Taux de dette (%)",
    0.0,
    15.0,
    5.0
) / 100

loan_term = st.sidebar.number_input(
    "Durée de la dette",
    min_value=1,
    max_value=40,
    value=20
)

holding_period = st.sidebar.number_input(
    "Horizon de détention",
    min_value=1,
    max_value=40,
    value=20
)

exit_cap_rate = st.sidebar.slider(
    "Exit Cap Rate (%)",
    1.0,
    15.0,
    7.0
) / 100

sale_cost_rate = st.sidebar.slider(
    "Frais de cession (%)",
    0.0,
    10.0,
    3.0
) / 100

discount_rate = st.sidebar.slider(
    "Taux d'actualisation (%)",
    1.0,
    20.0,
    8.0
) / 100

# ============================================================================
# INVESTISSEMENT
# ============================================================================

acquisition_fees = purchase_price * acquisition_fee_rate

total_investment = (
    purchase_price
    + acquisition_fees
    + capex
)

debt = total_investment * ltv
equity = total_investment - debt

# ============================================================================
# DETTE
# ============================================================================

annuity = debt * (
    interest_rate /
    (1 - (1 + interest_rate) ** (-loan_term))
)

debt_rows = []

opening_balance = debt

for year in range(1, loan_term + 1):

    interest = opening_balance * interest_rate
    principal = annuity - interest
    closing_balance = max(0, opening_balance - principal)

    debt_rows.append({
        "Année": year,
        "Capital Initial": opening_balance,
        "Intérê
