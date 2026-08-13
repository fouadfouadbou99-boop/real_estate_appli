# =====================================================
# MODULE MONTE CARLO
# Analyse probabiliste du TRI
# =====================================================

import numpy as np
import pandas as pd

from underwriting import build_cashflows
from valuation import add_exit_to_cashflows
from metrics import calculate_irr


def run_monte_carlo(
    simulations: int,
    equity_investment: float,
    debt_df: pd.DataFrame,
    base_rent: float,
    growth_mean: float,
    growth_std: float,
    vacancy_mean: float,
    vacancy_std: float,
    expense_rate: float,
    debt_service: float,
    holding_period: int,
    taxe_fonciere: float,
    assurance: float,
    maintenance: float,
    gestion_locative: float,
    inflation: float,
    exit_cap_rate: float,
    sale_cost_rate: float
):
    """
    Simule plusieurs scénarios
    de croissance des loyers
    et de vacance.
    """

    irr_results = []

    for _ in range(simulations):

        simulated_growth = max(
            np.random.normal(
                growth_mean,
                growth_std
            ),
            -0.05
        )

        simulated_vacancy = min(
            max(
                np.random.normal(
                    vacancy_mean,
                    vacancy_std
                ),
                0
            ),
            0.50
        )

        cf_df = build_cashflows(

            rent_y1=base_rent,

            growth=simulated_growth,

            vacancy=simulated_vacancy,

            expense_rate=expense_rate,

            debt_service=debt_service,

            holding_period=holding_period,

            taxe_fonciere=taxe_fonciere,

            assurance=assurance,

            maintenance=maintenance,

            gestion_locative=gestion_locative,

            inflation=inflation
        )

        cf_df = add_exit_to_cashflows(
            cf_df,
            debt_df,
            exit_cap_rate,
            sale_cost_rate
        )

        irr_value = calculate_irr(
            equity_investment,
            cf_df
        )

        irr_results.append(
            irr_value * 100
        )

    return pd.DataFrame({
        "IRR": irr_results
    })


def monte_carlo_summary(
    mc_df: pd.DataFrame
):
    """
    Statistiques principales
    de la simulation.
    """

    irr_series = mc_df["IRR"]

    return {

        "Mean IRR":
            round(
                irr_series.mean(),
                2
            ),

        "Median IRR":
            round(
                irr_series.median(),
                2
            ),

        "Min IRR":
            round(
                irr_series.min(),
                2
            ),

        "Max IRR":
            round(
                irr_series.max(),
                2
            ),

        "Std Dev":
            round(
                irr_series.std(),
                2
            ),

        "P10":
            round(
                np.percentile(
                    irr_series,
                    10
   
