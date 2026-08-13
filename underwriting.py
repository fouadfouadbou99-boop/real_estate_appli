import pandas as pd


def build_cashflows(
        rent_y1,
        growth,
        vacancy,
        expenses,
        debt_service,
        years):

    rows = []

    for year in range(1, years + 1):

        gross_rent = (
            rent_y1 *
            ((1 + growth) ** (year - 1))
        )

        effective_rent = (
            gross_rent *
            (1 - vacancy)
        )

        noi = (
            effective_rent *
            (1 - expenses)
        )

        cf_equity = (
            noi -
            debt_service
        )

        rows.append({

            "Year": year,

            "Gross Rent": gross_rent,

            "Effective Rent": effective_rent,

            "NOI": noi,

            "CF Equity": cf_equity
        })

    return pd.DataFrame(rows)
