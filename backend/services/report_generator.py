from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import letter

import datetime


def generate_pdf_report(results):

    filename = (
        f"reports/shortlist_"
        f"{datetime.datetime.now().timestamp()}.pdf"
    )

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "HR AI Shortlisting Report",
        styles['Title']
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    rank = 1

    for candidate in results:

        text = f"""
        <b>Rank:</b> {rank}<br/>
        <b>Candidate:</b> {candidate['candidate']}<br/>
        <b>Total Score:</b>
        {candidate['evaluation']['total_score']}<br/>
        <b>Similarity:</b>
        {candidate['similarity_score']}<br/>
        """

        para = Paragraph(
            text,
            styles['BodyText']
        )

        elements.append(para)
        elements.append(Spacer(1, 20))

        rank += 1

    doc.build(elements)

    return filename