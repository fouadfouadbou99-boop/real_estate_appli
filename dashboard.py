import plotly.express as px
import streamlit as st


def draw_dashboard(df):

    st.subheader(
        "Dashboard Investissement"
    )

    fig1 = px.line(
        df,
        x="Année",
        y="NOI",
        title="NOI"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.line(
        df,
        x="Année",
        y="DSCR",
        title="DSCR"
    )

    fig2.add_hline(
        y=1.2,
        line_dash="dash",
        line_color="red"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    fig3 = px.line(
        df,
        x="Année",
        y="LTV",
        title="LTV"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    fig4 = px.bar(
        df,
        x="Année",
        y="Cash Flow Equity",
        title="Cash Flow Equity"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    fig5 = px.area(
        df,
        x="Année",
        y="Asset Value",
        title="Valeur de l'actif"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )
