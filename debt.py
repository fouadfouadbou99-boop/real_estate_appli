import pandas as pd


def debt_schedule(
        loan_amount,
        interest_rate,
        term):

    annuity = loan_amount * (
        interest_rate /
        (1 - (1 + interest_rate) ** (-term))
    )

    rows = []

    opening_balance = loan_amount

    for year in range(1, term + 1):

        interest = (
                opening_balance *
                interest_rate
        )

        principal = (
                annuity -
                interest
        )

        closing_balance = (
                opening_balance -
                principal
        )

        rows.append({

            "Year": year,

            "Opening Balance": opening_balance,

            "Annuity": annuity,

            "Interest": interest,

            "Principal": principal,

            "Closing Balance": closing_balance
        })

        opening_balance = closing_balance

    return pd.DataFrame(rows)
