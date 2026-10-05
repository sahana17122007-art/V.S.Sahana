"""PDF creation with ReportLab."""
from datetime import date
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from validators import safe

NAVY = colors.HexColor("#17365D")
DISCLAIMER = ("<b>Educational prototype disclaimer:</b> This text is for academic "
              "demonstration only and is not legal advice. A qualified legal "
              "professional should review any document before real-world use.")


def build_pdf(title, clauses, data):
    styles = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=styles["BodyText"], leading=15)
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
                            topMargin=18*mm, bottomMargin=18*mm, title=title)
    story = [
        Paragraph("LegalEase", ParagraphStyle("brand", parent=styles["Title"],
                  alignment=TA_CENTER, fontSize=22, textColor=NAVY)),
        Paragraph(safe(title), ParagraphStyle("doc", parent=styles["Heading1"],
                  alignment=TA_CENTER, fontSize=15)),
        Spacer(1, 12),
    ]
    for i, (heading, text) in enumerate(clauses, 1):
        story += [Paragraph(f"<b>{i}. {safe(heading)}</b>", styles["Heading3"]),
                  Paragraph(safe(text), body), Spacer(1, 6)]
    sign = Table([["______________________", "______________________"],
                  [safe(data["name"]), safe(data["other_party"])],
                  ["Signature / Date", "Signature / Date"],
                  ["Witness 1: ____________", "Witness 2: ____________"]],
                 colWidths=[85*mm, 85*mm])
    sign.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 8),
                              ("FONTSIZE", (0, 0), (-1, -1), 10)]))
    story += [Spacer(1, 24), sign, Spacer(1, 18),
              Paragraph(f"Generated on: {date.today():%d-%m-%Y}", body),
              Spacer(1, 8), Paragraph(DISCLAIMER, body)]
    doc.build(story)
    buf.seek(0)
    return buf
