# =====================================================
# MODULE VALORISATION
# Calcul de la valeur de sortie
# =====================================================

import pandas as pd


def gross_exit_value(
    terminal_noi: float,
    exit_cap_rate: float
) -> float:
    """
    Valeur brute à la sortie.

    Valeur = NOI Terminal / Exit Cap Rate
    """

    if exit_cap_rate <= 0:
        return 0

    return terminal_noi / exit_cap_rate


def net_exit_value(
    terminal_noi: float,
    exit_cap_rate: float,
    sale_cost_rate: float
) -> float:
    """
    Valeur nette après frais de cession.
    """

    gross_value = gross_exit_value(
        terminal_noi,
        exit_cap_rate
    )

    return gross_value * (
        1 - sale_cost_rate
    )


def equity_proceeds(
    terminal_noi: float,
    exit_cap_rate: float,
    sale_cost_rate: float,
    remaining_debt: float
) -> float:
    """
    Produit net revenant à l'actionnaire.
    """

    net_value = net_exit_value(
        terminal_noi,
        exit_cap_rate,
        sale_cost_rate
    )

    proceeds = net_value - remaining_debt

    return proceeds


def add_exit_to_cashflows(
    cashflows_df: pd.DataFrame,
    debt_df: pd.DataFrame,
    exit_cap_rate: float,
    sale_cost_rate: float
) -> pd.DataFrame:
    """
    Ajoute le produit de cession
    au dernier cash-flow actionnaire.
    """

    result_df = cashflows_df.copy()

    terminal_noi = float(
        result_df.iloc[-1]["NOI"]
    )

    remaining_debt = float(
        debt_df.iloc[-1]["Closing Balance"]
    )

    proceeds = equity_proceeds(
        terminal_noi,
        exit_cap_rate,
        sale_cost_rate,
        remaining_debt
    )

    result_df.loc[
        result_df.index[-1],
        "CF Equity"
    ] += proceeds

    result_df["Exit Proceeds"] = 0.0

    result_df.loc[
        result_df.index[-1],
        "Exit Proceeds"
    ] = round(proceeds, 2)

    return result_df


def valuation_summary(
    terminal_noi: float,
    exit_cap_rate: float,
    sale_cost_rate: float,
    remaining_debt: float
) -> dict:
    """
    Résumé de la valorisation.
    """

    gross_value = gross_exit_value(
        terminal_noi,
        exit_cap_rate
    )

    net_value = net_exit_value(
        terminal_noi,
        exit_cap_rate,
        sale_cost_rate
    )

    proceeds = (
        net_value -
        remaining_debt
    )

    return {

        "terminal_noi":
            round(
                terminal_noi,
                2
            ),

        "gross_exit_value":
            round(
                gross_value,
                2
            ),

        "net_exit_value":
            round(
                net_value,
                2
            ),

        "remaining_debt":
            round(
                remaining_debt,
                2
            ),

        "equity_proceeds":
            round(
                proceeds,
                2
            )
    }
