# =====================================================
# MODULE UNDERWRITING
# Modélisation des cash-flows immobiliers
# =====================================================

import pandas as pd


def build_cashflows(
    rent_y1: float,
    growth: float,
    vacancy: float,
    expense_rate: float,
    debt_service: float,
    holding_period: int,
    taxe_fonciere: float = 0,
    assurance: float = 0,
    maintenance: float = 0,
    gestion_locative: float = 0,
    inflation: float = 0
) -> pd.DataFrame:
    """
    Génère les cash-flows annuels du projet immobilier.
    """

    rows = []

    for year in range(1, holding_period + 1):

        # Evolution des loyers

        gross_rent = rent_y1 * (
            (1 + growth) ** (year - 1)
        )

        # Vacance

        vacancy_loss = (
            gross_rent * vacancy
        )

        effective_rent = (
            gross_rent - vacancy_loss
        )

        # Charges fixes indexées inflation

        indexed_taxe = (
            taxe_fonciere *
            ((1 + inflation) ** (year - 1))
        )

        indexed_assurance = (
            assurance *
            ((1 + inflation) ** (year - 1))
        )

        indexed_maintenance = (
            maintenance *
            ((1 + inflation) ** (year - 1))
        )

        indexed_gestion = (
            gestion_locative *
            ((1 + inflation) ** (year - 1))
        )

        # Charges variables

        variable_expenses = (
            effective_rent *
            expense_rate
        )

        total_expenses = (
            variable_expenses
            + indexed_taxe
            + indexed_assurance
            + indexed_maintenance
            + indexed_gestion
        )

        # NOI

        noi = (
            effective_rent -
            total_expenses
        )

        # Cash-flow après dette

        cf_equity = (
            noi -
            
