from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_pdf(path, data):

    doc = SimpleDocTemplate(path)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Investment Memorandum",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            f"IRR : {data['irr']:.2%}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"NPV : {data['npv']:,.0f}",
            styles["Normal"]
        )
    )

    doc.build(content)
