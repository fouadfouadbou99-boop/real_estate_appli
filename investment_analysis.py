import pandas as pd

from metrics import *
from sensitivity import *


def run_analysis(df):

    final_noi = df["NOI"].iloc[-1]

    debt_balance = (
        df["Solde Dette"].iloc[-1]
    )

    gross_exit_value, net_exit_value = (
        compute_exit_value(
            final_noi=final_noi,
            growth_rate=0.02,
            exit_cap_rate=0.07,
            selling_cost_pct=0.03
        )
    )

    net_sale_proceeds = (
        compute_net_sale_proceeds(
            net_exit_value,
            debt_balance
        )
    )

    equity_initial = 348000

    irr_equity = (
        compute_equity_irr(
            equity_initial,
            df["Cash Flow Equity"].tolist(),
            net_sale_proceeds
        )
    )

    irr_project = (
        compute_project_irr(
            project_cost=1180000,
            noi_series=df["NOI"].tolist(),
            net_exit_value=net_exit_value
        )
    )

    npv = compute_npv(
        0.08,
        equity_initial,
        df["Cash Flow Equity"].tolist(),
        net_sale_proceeds
    )

    moic = compute_moic(
        equity_initial,
        df["Cash Flow Equity"].tolist(),
        net_sale_proceeds
    )

    avg_dscr = (
        df["DSCR"].mean()
    )

    avg_ltv = (
        df["LTV"].mean()
    )

    return {
        "IRR Equity": irr_equity,
        "IRR Projet": irr_project,
        "NPV": npv,
        "MOIC": moic,
        "DSCR Moyen": avg_dscr,
        "LTV Moyen": avg_ltv,
        "Valeur Sortie Brute": gross_exit_value,
        "Valeur Sortie Nette": net_exit_value,
        "Produit Net Vente": net_sale_proceeds
    }
