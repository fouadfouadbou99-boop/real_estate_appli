# =====================================================
# MODULE DETTE
# Tableau d'amortissement d'un prêt amortissable
# =====================================================

import pandas as pd


def calculate_annuity(
    loan_amount: float,
    interest_rate: float,
    term: int
) -> float:
    """
    Calcule l'annuité constante d'un emprunt.

    Parameters
    ----------
    loan_amount : float
        Montant de l'emprunt.

    interest_rate : float
        Taux d'intérêt annuel (ex: 0.05 pour 5%).

    term : int
        Durée du prêt en années.

    Returns
    -------
    float
        Annuité annuelle.
    """

    annuity = loan_amount * (
        interest_rate /
        (1 - (1 + interest_rate) ** (-term))
    )

    return annuity


def debt_schedule(
    loan_amount: float,
    interest_rate: float,
    term: int
) -> pd.DataFrame:
    """
    Génère le tableau complet d'amortissement.

    Parameters
    ----------
    loan_amount : float
        Montant emprunté.

    interest_rate : float
        Taux annuel.

    term : int
        Durée de l'emprunt.

    Returns
    -------
    pd.DataFrame
    """

    annuity = calculate_annuity(
        loan_amount,
        interest_rate,
        term
    )

    rows = []

    opening_balance = loan_amount

    for year in range(1, term + 1):

        interest = opening_balance * interest_rate

        principal = annuity - interest

        closing_balance = (
            opening_balance - principal
        )

        rows.append({

            "Year": year,

            "Opening Balance": round(
                opening_balance, 2
            ),

            "Annuity": round(
                annuity, 2
            ),

            "Interest": round(
                interest, 2
            ),

            "Principal": round(
                principal, 2
            ),

            "Closing Balance
