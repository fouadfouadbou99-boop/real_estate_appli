import pandas as pd


def create_sensitivity(
        valuation_callback
):

    growths = [
        0.01,
        0.02,
        0.03,
        0.04
    ]

    caps = [
        0.065,
        0.07,
        0.075,
        0.08
    ]

    matrix = pd.DataFrame(
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

    for g in growths:

        for cap in caps:

            irr = valuation_callback(
                growth=g,
                exit_cap=cap
            )

            matrix.loc[
                f"{g*100:.0f}%",
                f"{cap*100:.1f}%"
            ] = round(
                irr*100,
                2
            )

    return matrix
