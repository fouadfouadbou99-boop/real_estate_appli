import pandas as pd
from io import BytesIO


def export_full_report(
        projection_df,
        report_df,
        sensitivity_df,
        kpis
):
    """
    Génère un fichier Excel complet.
    """

    output = BytesIO()

    with pd.ExcelWriter(
            output,
            engine="xlsxwriter"
    ) as writer:

        workbook = writer.book

        #################################################
        # FORMATS
        #################################################

        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'bg_color': '#1F4E78',
            'font_color': 'white'
        })

        kpi_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'bg_color': '#D9EAD3'
        })

        percent_format = workbook.add_format({
            'num_format': '0.00%'
        })

        money_format = workbook.add_format({
            'num_format': '#,##0'
        })

        #################################################
        # SHEET PROJECTION
        #################################################

        projection_df.to_excel(
            writer,
            sheet_name="Projection",
            index=False
        )

        ws_projection = writer.sheets["Projection"]

        ws_projection.set_column(
            'A:Z',
            18
        )

        #################################################
        # SHEET KPI
        #################################################

        kpi_df = pd.DataFrame([
            ["TRI Projet", kpis["irr_project"]],
            ["TRI Equity", kpis["irr_equity"]],
            ["VAN", kpis["npv"]],
            ["MOIC", kpis["moic"]],
            ["DSCR Moyen", kpis["avg_dscr"]],
            ["LTV Moyen", kpis["avg_ltv"]],
            ["Valeur Sortie", kpis["exit_value"]],
            ["Produit Net Vente", kpis["sale_proceeds"]],
        ],
            columns=[
                "Indicateur",
                "Valeur"
            ]
        )

        kpi_df.to_excel(
            writer,
            sheet_name="KPIs",
            index=False
        )

        ws_kpi = writer.sheets["KPIs"]

        ws_kpi.set_column(
            "A:B",
            30
        )

        #################################################
        # SHEET REPORTING
        #################################################

        report_df.to_excel(
            writer,
            sheet_name="Reporting",
            index=False
        )

        ws_report = writer.sheets["Reporting"]

        ws_report.set_column(
            "A:B",
            40
        )

        #################################################
        # SHEET SENSIBILITES
        #################################################

        sensitivity_df.to_excel(
            writer,
            sheet_name="Sensibilites"
        )

        ws_sens = writer.sheets["Sensibilites"]

        ws_sens.set_column(
            "A:F",
            18
        )

        #################################################
        # SHEET CONTROLES
        #################################################

        checks_df = pd.DataFrame({
            "Contrôle": [
                "DSCR > 1.20",
                "LTV < 80%",
                "Dette remboursée"
            ],
            "Résultat": [
                "OK" if kpis["avg_dscr"] > 1.20 else "ALERTE",
                "OK" if kpis["avg_ltv"] < 0.80 else "ALERTE",
                "OK"
            ]
        })

        checks_df.to_excel(
            writer,
            sheet_name="Controles",
            index=False
        )

        #################################################
        # DASHBOARD
        #################################################

        dashboard = workbook.add_worksheet(
            "Dashboard"
        )

        dashboard.write(
            "A1",
            "DASHBOARD INVESTISSEMENT",
            title_format
        )

        dashboard.write(
            "A4",
            "TRI Equity"
        )

        dashboard.write(
            "B4",
            kpis["irr_equity"]
        )

        dashboard.write(
            "D4",
            "TRI Projet"
        )

        dashboard.write(
            "E4",
            kpis["irr_project"]
        )

        dashboard.write(
            "G4",
            "MOIC"
        )

        dashboard.write(
            "H4",
            kpis["moic"]
        )

        dashboard.write(
            "J4",
            "VAN"
        )

        dashboard.write(
            "K4",
            kpis["npv"]
        )

        #################################################
        # GRAPH 1 NOI
        #################################################

        chart_noi = workbook.add_chart({
            "type": "line"
        })

        rows = len(projection_df)

        chart_noi.add_series({
            "name": "NOI",
            "categories":
                f"=Projection!$A$2:$A${rows+1}",
            "values":
                f"=Projection!$F$2:$F${rows+1}",
        })

        chart_noi.set_title({
            "name": "Evolution NOI"
        })

        dashboard.insert_chart(
            "A8",
            chart_noi
        )

        #################################################
        # GRAPH 2 LTV
        #################################################

        chart_ltv = workbook.add_chart({
            "type": "line"
        })

        chart_ltv.add_series({
            "name": "LTV",
            "categories":
                f"=Projection!$A$2:$A${rows+1}",
            "values":
                f"=Projection!$N$2:$N${rows+1}",
        })

        chart_ltv.set_title({
            "name": "Evolution LTV"
        })

        dashboard.insert_chart(
            "I8",
            chart_ltv
        )

        #################################################
        # GRAPH 3 DSCR
        #################################################

        chart_dscr = workbook.add_chart({
            "type": "line"
        })

        chart_dscr.add_series({
            "name": "DSCR",
            "categories":
                f"=Projection!$A$2:$A${rows+1}",
            "values":
                f"=Projection!$L$2:$L${rows+1}",
        })

        chart_dscr.set_title({
            "name": "Evolution DSCR"
        })

        dashboard.insert_chart(
            "A25",
            chart_dscr
        )

        #################################################
        # GRAPH 4 CASH FLOW EQUITY
        #################################################

        chart_cf = workbook.add_chart({
            "type": "column"
        })

        chart_cf.add_series({
            "name": "Cash Flow Equity",
            "categories":
                f"=Projection!$A$2:$A${rows+1}",
            "values":
                f"=Projection!$I$2:$I${rows+1}",
        })

        chart_cf.set_title({
            "name": "Cash Flow Equity"
        })

        dashboard.insert_chart(
            "I25",
            chart_cf
        )

        #################################################
        # SYNTHÈSE
        #################################################

        synthesis = workbook.add_worksheet(
            "Synthese"
        )

        synthesis.write(
            "A1",
            "SYNTHESE COMITE INVESTISSEMENT",
            title_format
        )

        synthesis.write(
            "A4",
            f"TRI Equity : {kpis['irr_equity']:.2%}"
        )

        synthesis.write(
            "A5",
            f"TRI Projet : {kpis['irr_project']:.2%}"
        )

        synthesis.write(
            "A6",
            f"VAN : {kpis['npv']:,.0f}"
        )

        synthesis.write(
            "A7",
            f"MOIC : {kpis['moic']:.2f}x"
        )

        synthesis.write(
            "A8",
            f"DSCR Moyen : {kpis['avg_dscr']:.2f}"
        )

        synthesis.write(
            "A9",
            f"LTV Moyen : {kpis['avg_ltv']:.2%}"
        )

    return output.getvalue()
