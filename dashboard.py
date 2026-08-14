import matplotlib.pyplot as plt


def create_dashboard(
    df,
    output_folder
):

    years = df["Année"]

    plt.figure(figsize=(10,5))
    plt.plot(
        years,
        df["Revenus Bruts"]
    )
    plt.title(
        "Evolution des loyers"
    )
    plt.grid(True)
    plt.savefig(
        f"{output_folder}/loyers.png"
    )
    plt.close()

    plt.figure(figsize=(10,5))
    plt.plot(
        years,
        df["NOI"]
    )
    plt.title(
        "Evolution du NOI"
    )
    plt.grid(True)
    plt.savefig(
        f"{output_folder}/noi.png"
    )
    plt.close()

    plt.figure(figsize=(10,5))
    plt.bar(
        years,
        df["Cash Flow Equity"]
    )
    plt.title(
        "Cash Flow Equity"
    )
    plt.savefig(
        f"{output_folder}/equity_cf.png"
    )
    plt.close()

    plt.figure(figsize=(10,5))
    plt.plot(
        years,
        df["DSCR"]
    )
    plt.axhline(
        y=1.2,
        color='red',
        linestyle='--'
    )
    plt.title(
        "DSCR"
    )
    plt.savefig(
        f"{output_folder}/dscr.png"
    )
    plt.close()

    plt.figure(figsize=(10,5))
    plt.plot(
        years,
        df["LTV"]
    )
    plt.title(
        "LTV"
    )
    plt.savefig(
        f"{output_folder}/ltv.png"
    )
    plt.close()
