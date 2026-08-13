import pandas as pd


def portfolio_summary():

    assets = [

        ["Rabat", 15_000_000],

        ["Casablanca", 20_000_000],

        ["Tanger", 12_000_000],

        ["Marrakech", 16_000_000]
    ]

    df = pd.DataFrame(
        assets,
        columns=[
            "Asset",
            "Value"
        ]
    )

    return df
