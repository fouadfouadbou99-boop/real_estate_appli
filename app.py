import streamlit as st

st.set_page_config(
    page_title="Real Estate Investment Platform",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Real Estate Investment Platform")

st.success("Application démarrée avec succès")

st.header("Hypothèses")

purchase_price = st.number_input(
    "Prix acquisition",
    value=1000000.0
)

rent = st.number_input(
    "Loyer annuel",
    value=120000.0
)

vacancy = st.slider(
    "Vacance (%)",
    0,
    20,
    5
)

st.header("Résultats")

effective_rent = rent * (1 - vacancy / 100)

st.metric(
    "Loyer net",
    f"{effective_rent:,.0f} MAD"
)

st.metric(
    "Prix acquisition",
    f"{purchase_price:,.0f} MAD"
)
