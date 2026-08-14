# app.py

import pandas as pd
import numpy as np
import numpy_financial as npf
import streamlit as st
import plotly.express as px

# ==========================================================
# CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Modèle Financier Immobilier",
    layout="wide"
)

st.title("🏢 Modèle Financier Immobilier")
st.write("Projection financière et analyse d'investissement immobilier")

# ==========================================================
# CHARGEMENT DU FICHIER
# ==========================================================

uploaded_file = st.file_uploader(
    "Charger le fichier Excel contenant les hypothèses",
    type=["xlsx", "xlsm"]
)

if uploaded_file is None:
    st.info("Veuillez charger votre fichier Excel.")
    st.stop()

# ==========================================================
# LECTURE DES HYPOTHESES
# ==========================================================

try:

    hypotheses_df = pd.read_excel(
        uploaded_file,
        sheet_name="Hypothèses"
    )

    hypotheses_df.columns = ["Parameter", "Value"]
    hypotheses_df = hypotheses_df.drop(0)
    hypotheses_df = hypotheses_df.set_index("Parameter")

    hypotheses_df["Value"] = pd.to_numeric(
        hypotheses_df["Value"],
        errors="coerce"
    )

except Exception as e:
    st.error(f"Erreur lors du chargement des hypothèses : {e}")
    st.stop()

# ==========================================================
# EXTRACTION DES VARIABLES
# ==========================================================

prix_acquisition = hypotheses_df.loc["Prix acquisition", "Value"]
frais_acquisition_percent = hypotheses_df.loc["Frais acquisition %", "Value"]

travaux = hypotheses_df.loc["Travaux", "Value"]

loyer_brut_an1 = hypotheses_df.loc["Loyer brut An1", "Value"]

croissance_loyers_percent = hypotheses_df.loc[
    "Croissance loyers %",
    "Value"
]

vacance_percent = hypotheses_df.loc[
    "Vacance %",
    "Value"
]

charges_percent = hypotheses_df.loc[
    "Charges %",
    "Value"
]

dette_percent = hypotheses_df.loc[
    "Dette %",
    "Value"
]

interest_rate_annual = hypotheses_df.loc[
    "Taux dette %",
    "Value"
]

loan_duration_years = int(
    hypotheses_df.loc["Duree dette", "Value"]
)

horizon_years = int(
    hypotheses_df.loc["Horizon", "Value"]
)

exit_cap_rate = hypotheses_df.loc[
    "Exit Cap Rate %",
    "Value"
]

frais_cession_percent = hypotheses_df.loc[
    "Frais cession %",
    "Value"
]

taux_actualisation = hypotheses_df.loc[
    "Taux actualisation %",
    "Value"
]

# ==========================================================
# BUDGET ACQUISITION
# ==========================================================

budget_acquisition = (
    prix_acquisition
    * (1 + frais_acquisition_percent)
    + travaux
)

montant_dette = budget_acquisition * dette_percent
montant_equity = budget_acquisition - montant_dette

# ==========================================================
# AMORTISSEMENT DETTE
# ==========================================================

interest_rate_monthly = interest_rate_annual / 12
num_payments_months = loan_duration_years * 12

if interest_rate_monthly > 0:

    monthly_payment = (
        montant_dette
        * (
            interest_rate_monthly
            * (1 + interest_rate_monthly) ** num_payments_months
        )
        / (
            (1 + interest_rate_monthly) ** num_payments_months
            - 1
        )
    )

else:
    monthly_payment = montant_dette / num_payments_months

amortization_schedule = []

remaining_balance = montant_dette

for year in range(1, loan_duration_years + 1):

    annual_interest = 0
    annual_principal = 0

    opening_balance = remaining_balance

    for month in range(12):

        if remaining_balance <= 0:
            break

        interest_month = (
            remaining_balance * interest_rate_monthly
        )

        principal_month = (
            monthly_payment - interest_month
        )

        if principal_month > remaining_balance:
            principal_month = remaining_balance

        annual_interest += interest_month
        annual_principal += principal_month

        remaining_balance -= principal_month

    amortization_schedule.append(
        [
            year,
            opening_balance,
            annual_interest,
            annual_principal,
            annual_interest + annual_principal,
            remaining_balance
        ]
    )

amortization_df = pd.DataFrame(
    amortization_schedule,
    columns=[
        "Année",
        "Solde début période",
        "Intérêts annuels",
        "Amortissement annuel",
        "Annuité annuelle",
        "Solde fin période"
    ]
)

# ==========================================================
# PROJECTION
# ==========================================================

projection = []

current_rent = loyer_brut_an1

for year in range(1, horizon_years + 1):

    revenus_bruts = current_rent

    vacance = revenus_bruts * vacance_percent

    revenus_nets = revenus_bruts - vacance

    charges = revenus_nets * charges_percent

    noi = revenus_nets - charges

    interets = 0
    principal = 0

    if year <= loan_duration_years:

        interets = amortization_df.loc[
            year - 1,
            "Intérêts annuels"
        ]

        principal = amortization_df.loc[
            year - 1,
            "Amortissement annuel"
        ]

    cashflow_after_debt = noi - interets - principal

    projection.append(
        [
            year,
            revenus_bruts,
            vacance,
            revenus_nets,
            charges,
            noi,
            interets,
            principal,
            cashflow_after_debt
        ]
    )

    current_rent = (
        current_rent
        * (1 + croissance_loyers_percent)
    )

projection_df = pd.DataFrame(
    projection,
    columns=[
        "Année",
        "Revenus Bruts",
        "Vacance",
        "Revenus Nets",
        "Charges",
        "NOI",
        "Intérêts",
        "Amortissement",
        "Cash Flow Equity"
    ]
)

# ==========================================================
# VALEUR DE SORTIE
# ==========================================================

noi_sortie = projection_df.iloc[-1]["NOI"]

valeur_terminale = noi_sortie / exit_cap_rate

produit_net_cession = (
    valeur_terminale
    * (1 - frais_cession_percent)
)

# ==========================================================
# KPI
# ==========================================================

project_cf = [-budget_acquisition]

project_cf.extend(
    projection_df["NOI"].tolist()
)

project_cf[-1] += produit_net_cession

equity_cf = [-montant_equity]

equity_cf.extend(
    projection_df["Cash Flow Equity"].tolist()
)

equity_cf[-1] += produit_net_cession

tri_projet = npf.irr(project_cf)

tri_equity = npf.irr(equity_cf)

van = (
    npf.npv(
        taux_actualisation,
        project_cf[1:]
    )
    + project_cf[0]
)

moic = (
    sum(
        x for x in equity_cf
        if x > 0
    )
    / abs(equity_cf[0])
)

# ==========================================================
# DSCR
# ==========================================================

projection_df["Debt Service"] = (
    projection_df["Intérêts"]
    + projection_df["Amortissement"]
)

projection_df["DSCR"] = projection_df.apply(
    lambda row:
    row["NOI"] / row["Debt Service"]
    if row["Debt Service"] > 0
    else np.nan,
    axis=1
)

# ==========================================================
# LTV
# ==========================================================

projection_df["Asset Value"] = (
    projection_df["NOI"] / exit_cap_rate
)

projection_df["Solde Dette"] = (
    projection_df["Année"].map(
        amortization_df.set_index(
            "Année"
        )["Solde fin période"]
    )
)

projection_df["Solde Dette"] = (
    projection_df["Solde Dette"]
    .fillna(0)
)

projection_df["LTV"] = (
    projection_df["Solde Dette"]
    / projection_df["Asset Value"]
)

# ==========================================================
# KPI DASHBOARD
# ==========================================================

st.header("📊 KPIs")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "TRI Projet",
    f"{tri_projet:.2%}"
)

c2.metric(
    "TRI Equity",
    f"{tri_equity:.2%}"
)

c3.metric(
    "VAN",
    f"{van:,.0f}"
)

c4.metric(
    "MOIC",
    f"{moic:.2f}x"
)

st.divider()

# ==========================================================
# TABLEAU
# ==========================================================

st.header("Projection Annuelle")

st.dataframe(
    projection_df,
    use_container_width=True
)

# ==========================================================
# GRAPHIQUE NOI / CASH FLOW
# ==========================================================

st.header("NOI et Cash Flows")

fig1 = px.line(
    projection_df,
    x="Année",
    y=[
        "NOI",
        "Cash Flow Equity"
    ],
    markers=True
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==========================================================
# GRAPHIQUE DSCR
# ==========================================================

st.header("DSCR")

fig2 = px.line(
    projection_df,
    x="Année",
    y="DSCR",
    markers=True
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================================
# GRAPHIQUE LTV
# ==========================================================

st.header("LTV")

fig3 = px.line(
    projection_df,
    x="Année",
    y="LTV",
    markers=True
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================================
# EXPORT EXCEL
# ==========================================================

excel_output = "projection_resultats.xlsx"

projection_df.to_excel(
    excel_output,
    index=False
)

with open(excel_output, "rb") as f:

    st.download_button(
        label="📥 Télécharger les résultats Excel",
        data=f,
        file_name=excel_output,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
