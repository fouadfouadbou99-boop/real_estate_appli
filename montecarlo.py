import numpy as np
import pandas as pd


def run_simulation(
        n=5000,
        mean_growth=0.02,
        std_growth=0.01):

    values = np.random.normal(
        mean_growth,
        std_growth,
        n
    )

    return pd.DataFrame({
        "Rent Growth": 
