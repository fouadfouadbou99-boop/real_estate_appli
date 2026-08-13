def terminal_value(
        terminal_noi,
        exit_cap,
        sale_cost_rate):

    gross_value = (
        terminal_noi /
        exit_cap
    )

    net_value = (
        gross_value *
        (1 - sale_cost_rate)
    )

    return gross_value, net_value
