import numpy as np
import numpy_financial as npf


def compute_exit_value(
    final_noi,
    growth_rate,
    exit_cap_rate,
    selling_cost_pct
):
    """
    NOI N+1 / Exit Cap
    """

    noi_n1 = final_noi * (1 + growth_rate)

    gross_exit_value = (
        noi_n1 /
        exit_cap_rate
    )

    net_exit_value = (
        gross_exit_value *
        (1 - selling_cost_pct)
    )

    return gross_exit_value, net_exit_value


def compute_net_sale_proceeds(
    net_exit_value,
    remaining_debt
):

    return (
        net_exit_value
        - remaining_debt
    )


def compute_equity_irr(
    equity_initial,
    cash_flows_equity,
    net_sale_proceeds
):

    flows = [-equity_initial]

    flows.extend(cash_flows_equity)

    flows[-1] = (
        flows[-1]
        + net_sale_proceeds
    )

    return npf.irr(flows)


def compute_project_irr(
    project_cost,
    noi_series,
    net_exit_value
):

    flows = [-project_cost]

    flows.extend(noi_series)

    flows[-1] += net_exit_value

    return npf.irr(flows)


def compute_npv(
    discount_rate,
    equity_initial,
    cash_flows_equity,
    net_sale_proceeds
):

    flows = cash_flows_equity.copy()

    flows[-1] += net_sale_proceeds

    return (
        npf.npv(
            discount_rate,
            flows
        )
        - equity_initial
    )


def compute_moic(
    equity_initial,
    cash_flows_equity,
    net_sale_proceeds
):

    total_received = (
        sum(cash_flows_equity)
        + net_sale_proceeds
    )

    return (
        total_received /
        equity_initial
    )
