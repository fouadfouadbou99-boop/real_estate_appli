import pandas as pd


def sensitivity_grid():

    growths = [
        0.01,
        0.02,
        0.03,
        0.04
    ]

    exits = [
        0.06,
        0.07,
        0.08,
        0.09
    ]

    matrix = []

    for g in growths:

        row = []

        for e in exits:

            score = (
                g * 100 -
                e * 50
            )

            row.append(
                round(score, 2)
            )

        matrix.append(row)

    return pd.DataFrame(
        matrix,
        index=growths,
        columns=exits
    )
