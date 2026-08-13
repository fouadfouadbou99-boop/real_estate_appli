# =====================================================
# MODULE METRICS
# Calcul des KPI financiers
# =====================================================

import numpy as np
import numpy_financial as npf
import pandas as pd


def calculate_irr(
    equity_investment: float,
    cashflows_df: pd.DataFrame
) -> float:
    """
    TRI (IRR) de l'investissement.
    """

    cashflows = [-equity_investment]

    cashflows.extend(
        cashflows_df["CF Equity"].tolist()
    )

    try:
        return float(
            npf.irr(cashflows)
        )

    except Exception:
        return 0.0


def calculate_npv(
    equity_investment: float,
    cashflows_df: pd.DataFrame,
    discount_rate: float
) -> float:
    """
    VAN (NPV)
    """

    cashflows = (
        cashflows_df["CF Equity"]
        .tolist()
    )

    npv = npf.npv(
        discount_rate,
        cashflows
    )

    npv = npv - equity_investment

    return float(npv)


def calculate_equity_multiple(
    equity_investment: float,
    cashflows_df: pd.DataFrame
) -> float:
    """
    Equity Multiple
    """

    total_distributions = (
        cashflows_df["CF Equity"]
        .sum()
    )

    if equity
