import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from numpy_financial import irr, npv
from io import BytesIO

# =============================================================================
# CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Real Estate Investment Platform",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Real Estate Investment Platform")
st.markdown("Modélisation et analyse d'investissements immobiliers")

# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.header("Hypothèses")

purchase_price = st.sidebar.number_input(
    "Prix d'acquisition",
    min_value=0.0,
    value=1_000_000.0,
    step=10000.0
)

acquisition_fee_rate = (
    st.sidebar.slider(
        "Frais d'acquisition (%)",
        0.0,
        20.0,
        8.0
    ) / 100
)

capex = st.sidebar.number_input(
    "Travaux",
    min_value=0.0,
    value=100_000.0,
    step=5000.0
)

gross_rent_y1 = st.sidebar.number_input(
    "Loyer brut Année 1",
    min_value=0.0,
    value=120_000.0,
    step=1000.0
)

rent_growth = (
    st.sidebar.slider(
        "Croissance des loyers (%)",
        0.0,
        10.0,
        2.0
    ) / 100
)

vacancy_rate = (
    st.sidebar.slider(
        "Vacance (%)",
        0.0,
        30.0,
        5.0
    ) / 100
)

expense_rate = (
    st.sidebar.slider(
        "Charges (%)",
        0.0,
        50.0,
        20.0
    ) / 100
)

ltv = (
    st.sidebar.slider(
        "LTV (%)",
        0.0,
        90.0,
        70.0
    ) / 100
)

interest_rate = (
    st.sidebar.slider(
        "Taux de dette (%)",
        0.0,
        15.0,
        5.0
    ) / 100
)

loan_term = st.sidebar.number_input(
    "Durée de la dette (années)",
    min_value=1,
    max_value=40,
    value=20
)

holding_period = st.sidebar.number_input(
    "Durée de détention (années)",
    min_value=1,
    max_value=40,
    value=20
)

exit_cap_rate = (
    st.sidebar.slider(
        "Exit Cap Rate (%)",
        1.0,
        15.0,
        7.0
    ) / 100
)

sale_cost_rate = (
    st.sidebar.slider(
        "Frais de cession (%)",
        0.0,
        10.0,
        3.0
    ) / 100
)

discount_rate = (
    st.sidebar.slider(
        "Taux d'actualisation (%)",
        1.0,
        20.0,
        8.0
    ) / 100
)

# =============================================================================
# INVESTISSEMENT INITIAL
# =============================================================================

acquisition_fees = purchase_price * acquisition_fee_rate

total_investment = (
    purchase_price
    + acquisition_fees
    + capex
)

debt_amount = total_investment * ltv
equity_amount = total_investment - debt_amount

# =============================================================================
# ANNUITE
# =============================================================================

if interest_rate == 0:
    annuity = debt_amount / loan_term
else:
    annuity = debt_amount * (
        interest_rate /
        (1 - (1 + interest_rate) ** (-loan_term))
    )

# =============================================================================
# TABLEAU D'AMORTISSEMENT
# =============================================================================

debt_rows = []

opening_balance = debt_amount

for year in range(1, loan_term + 1):

    interest = opening_balance * interest_rate

    principal = annuity - interest

    closing_balance = max(
        0,
        opening_balance - principal
    )

    debt_rows.append({
        "Année": year,
        "Capital initial": opening_balance,
        "Intérêts": interest,
        "Principal": principal,
        "Annuité": annuity,
        "Capital final": closing_balance
    })

    opening_balance = closing_balance

debt_df = pd.DataFrame(debt_rows)

# =============================================================================
# CASH FLOWS
# =============================================================================

cf_rows = []

for year in range(1, holding_period + 1):

    gross_rent = (
        gross_rent_y1 *
        ((1 + rent_growth) ** (year - 1))
    )

    effective_rent = (
        gross_rent *
        (1 - vacancy_rate)
    )

    noi = (
        effective_rent *
        (1 - expense_rate)
    )

    debt_service = annuity if year <= loan_term else 0

    equity_cf = noi - debt_service

    cf_rows.append({
        "Année": year,
        "Loyer brut": gross_rent,
        "Loyer net": effective_rent,
        "NOI": noi,
        "Service dette": debt_service,
        "Cash Flow Equity": equity_cf
    })

cashflow_df = pd.DataFrame(cf_rows)

# =============================================================================
# DETTE RESIDUELLE A LA SORTIE
# =============================================================================

if holding_period <= loan_term:
    remaining_debt = debt_df.loc[
        debt_df["Année"] == holding_period,
        "Capital final"
    ].iloc[0]
else:
    remaining_debt = 0

# =============================================================================
# VALEUR DE SORTIE
# =============================================================================

terminal_noi = cashflow_df.iloc[-1]["NOI"]

gross_exit_value = terminal_noi / exit_cap_rate

sale_costs = gross_exit_value * sale_cost_rate

net_exit_value = gross_exit_value - sale_costs

net_sale_proceeds = (
    net_exit_value
    - remaining_debt
)

cashflow_df.loc[
    cashflow_df.index[-1],
    "Cash Flow Equity"
] += net_sale_proceeds

# =============================================================================
# KPI
# =============================================================================

equity_cashflows = [-equity_amount]
equity_cashflows.extend(
    cashflow_df["Cash Flow Equity"].tolist()
)

try:
    irr_result = irr(equity_cashflows)
except:
    irr_result = np.nan

try:
    npv_result = (
        npv(
            discount_rate,
            equity_cashflows[1:]
        )
        - equity_cashflows[0]
    )
except:
    npv_result = np.nan

equity_multiple = (
    sum(equity_cashflows[1:])
    / equity_amount
    if equity_amount > 0
    else 0
)

entry_noi = cashflow_df.iloc[0]["NOI"]

entry_cap_rate = (
    entry_noi / total_investment
    if total_investment > 0
    else 0
)

dscr = (
    entry_noi / annuity
    if annuity > 0
    else 0
)

# =============================================================================
# DASHBOARD KPI
# =============================================================================

st.subheader("Indicateurs Clés")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "TRI",
    f"{irr_result:.2%}" if not np.isnan(irr_result) else "N/A"
)

c2.metric(
    "VAN",
    f"{npv_result:,.0f}"
)

c3.metric(
    "DSCR",
    f"{dscr:.2f}"
)

c4.metric(
    "Equity Multiple",
    f"{equity_multiple:.2f}x"
)

# =============================================================================
# STRUCTURE DE FINANCEMENT
# =============================================================================

st.subheader("Structure de financement")

a, b, c = st.columns(3)

a.metric(
    "Investissement Total",
    f"{total_investment:,.0f}"
)

b.metric(
    "Dette",
    f"{debt_amount:,.0f}"
)

c.metric(
    "Fonds Propres",
    f"{equity_amount:,.0f}"
)

# =============================================================================
# GRAPHIQUE
# =============================================================================

st.subheader("Cash Flows Equity")

fig = px.line(
    cashflow_df,
    x="Année",
    y="Cash Flow Equity",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =============================================================================
# ANALYSE DE SENSIBILITÉ
# =============================================================================

st.subheader("Sensibilité Exit Cap Rate")

sensitivity = []

for cap in np.arange(0.05, 0.091, 0.005):

    value = terminal_noi / cap

    sensitivity.append({
        "Exit Cap Rate (%)": round(cap * 100, 2),
        "Valeur de sortie": round(value, 0)
    })

sensitivity_df = pd.DataFrame(sensitivity)

st.dataframe(
    sensitivity_df,
    use_container_width=True
)

# =============================================================================
# TABLEAUX DETAILLES
# =============================================================================

tab1, tab2 = st.tabs(
    ["Cash Flows", "Dette"]
)

with tab1:
    st.dataframe(
        cashflow_df,
        use_container_width=True
    )

with tab2:
    st.dataframe(
        debt_df,
        use_container_width=True
    )

# =============================================================================
# EXPORT EXCEL
# =============================================================================

buffer = BytesIO()

with pd.ExcelWriter(
    buffer,
    engine="openpyxl"
) as writer:

    cashflow_df.to_excel(
        writer,
        sheet_name="CashFlows",
        index=False
    )

    debt_df.to_excel(
        writer,
        sheet_name="Dette",
        index=False
    )

    pd.DataFrame({
        "Indicateur": [
            "TRI",
            "VAN",
            "DSCR",
            "Equity Multiple",
            "Cap Rate Entrée",
            "Valeur de sortie nette"
        ],
        "Valeur": [
            irr_result,
            npv_result,
            dscr,
            equity_multiple,
            entry_cap_rate,
            net_exit_value
        ]
    }).to_excel(
        writer,
        sheet_name="KPI",
        index=False
    )

st.download_button(
    "📥 Télécharger Excel",
    data=buffer.getvalue(),
    file_name="real_estate_model.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
