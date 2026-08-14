import pandas as pd


def build_sensitivity_table(
    valuation_function
):

    growth_rates = [
        0.01,
        0.02,
        0.03,
        0.04
    ]

    exit_caps = [
        0.065,
        0.070,
        0.075,
        0.080
    ]

    sensitivity = pd.DataFrame(
        index=[
            "1%",
            "2%",
            "3%",
            "4%"
        ],
        columns=[
            "6.5%",
            "7.0%",
            "7.5%",
            "8.0%"
        ]
    )

    for g in growth_rates:

        for cap in exit_caps:

            irr = valuation_function(
                growth=g,
                exit_cap=cap
            )

            sensitivity.loc[
                f"{int(g*100)}%",
                f"{cap*100:.1f}%"
            ] = round(
                irr * 100,
                2
            )

    return sensitivity
