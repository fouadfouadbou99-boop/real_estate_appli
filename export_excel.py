from io import BytesIO


def export_excel(
        projection,
        sensitivity,
        kpis
):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        projection.to_excel(
            writer,
            sheet_name="Projection"
        )

        sensitivity.to_excel(
            writer,
            sheet_name="Sensibilite"
        )

        kpis.to_excel(
            writer,
            sheet_name="KPIs"
        )

    return output.getvalue()
