import pandas as pd
from datetime import datetime


def generate_investment_report(
    df,
    kpis,
    assumptions
):
    """
    Génère un reporting synthétique
    """

    report = {}

    report["Date Analyse"] = datetime.today().strftime("%Y-%m-%d")

    report["Prix Acquisition"] = assumptions["purchase_price"]

    report["Loyer Initial"] = assumptions["gross_rent"]

    report["TRI Projet"] = round(
        kpis["IRR Projet"] * 100,
        2
    )

    report["TRI Equity"] = round(
        kpis["IRR Equity"] * 100,
        2
    )

    report["VAN"] = round(
        kpis["NPV"],
        0
    )

    report["MOIC"] = round(
        kpis["MOIC"],
        2
    )

    report["DSCR Moyen"] = round(
        df["DSCR"].mean(),
        2
    )

    report["DSCR Minimum"] = round(
        df["DSCR"].min(),
        2
    )

    report["LTV Moyen"] = round(
        df["LTV"].mean()*100,
        2
    )

    report["LTV Maximum"] = round(
        df["LTV"].max()*100,
        2
    )

    report["NOI Année 1"] = round(
        df["NOI"].iloc[0],
        0
    )

    report["NOI Final"] = round(
        df["NOI"].iloc[-1],
        0
    )

    report["Valeur Actif Initiale"] = round(
        df["Asset Value"].iloc[0],
        0
    )

    report["Valeur Actif Finale"] = round(
        df["Asset Value"].iloc[-1],
        0
    )

    report["Dette Initiale"] = round(
        df["Solde Dette"].iloc[0],
        0
    )

    report["Dette Finale"] = round(
        df["Solde Dette"].iloc[-1],
        0
    )

    return pd.DataFrame(
        report.items(),
        columns=[
            "Indicateur",
            "Valeur"
        ]
    )
