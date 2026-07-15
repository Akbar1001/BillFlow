from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors


def generate_invoice_pdf(invoice):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
    )

    styles = getSampleStyleSheet()

    elements = []

    # Company Name
    elements.append(
        Paragraph(
            "BillFlow",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Invoice Management Platform",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # Invoice Information
    elements.append(
        Paragraph(
           f"Invoice Number: {invoice.invoice_number}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Issue Date: {invoice.issue_date}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Due Date: {invoice.due_date}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Status: {invoice.status}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # Customer Details
    elements.append(
        Paragraph(
            f"Company: {invoice.customer.company_name}",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Contact Person: {invoice.customer.name}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Email: {invoice.customer.email}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Phone: {invoice.customer.phone_number}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"GST Number: {invoice.customer.gst_number}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Address: {invoice.customer.address}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # Invoice Items Table
    data = [
        ["Description", "Quantity", "Unit Price", "Line Total"]
    ]

    for item in invoice.items.all():
        data.append([
            item.description,
            str(item.quantity),
            f"₹{item.unit_price}",
            f"₹{item.line_total}",
        ])

    table = Table(data)

    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('PADDING', (0, 0), (-1, -1), 10),
        ])
    )

    elements.append(table)

    elements.append(Spacer(1, 20))

    # Amount Summary
    elements.append(
        Paragraph(
            f"Subtotal: ₹{invoice.subtotal}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Tax: ₹{invoice.tax}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Discount: ₹{invoice.discount}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Total Amount: ₹{invoice.total_amount}",
            styles["Title"]
        )
    )

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf