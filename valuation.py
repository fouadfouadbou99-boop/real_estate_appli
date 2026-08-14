import numpy_financial as npf


class Valuation:

    @staticmethod
    def exit_value(
            final_noi,
            growth,
            exit_cap,
            selling_cost_pct
    ):

        noi_n1 = final_noi * (1 + growth)

        gross_exit_value = (
            noi_n1 /
            exit_cap
        )

        net_exit_value = (
            gross_exit_value *
            (1 - selling_cost_pct)
        )

        return (
            gross_exit_value,
            net_exit_value
        )

    @staticmethod
    def net_sale_proceeds(
            net_exit_value,
            remaining_debt
    ):

        return (
            net_exit_value -
            remaining_debt
        )

    @staticmethod
    def equity_irr(
            initial_equity,
            cashflows,
            sale_proceeds
    ):

        flows = [-initial_equity]

        flows.extend(cashflows)

        flows[-1] += sale_proceeds

        return npf.irr(flows)

    @staticmethod
    def project_irr(
            project_cost,
            noi_series,
            net_exit_value
    ):

        flows = [-project_cost]

        flows.extend(noi_series)

        flows[-1] += net_exit_value

        return npf.irr(flows)

    @staticmethod
    def npv(
            discount_rate,
            initial_equity,
            cashflows,
            sale_proceeds
    ):

        flows = cashflows.copy()

        flows[-1] += sale_proceeds

        return (
            npf.npv(
                discount_rate,
                flows
            ) - initial_equity
        )

    @staticmethod
    def moic(
            initial_equity,
            cashflows,
            sale_proceeds
    ):

        return (
            (
                sum(cashflows)
                + sale_proceeds
            )
            / initial_equity
        )
