from django.core.mail import EmailMessage

def send_invoice_email(
    customer_email,
    invoice_number,
    pdf_content
):
    email = EmailMessage(
        subject=f"Invoice {invoice_number}",
        body="Please find your invoice attached.",
        to=[customer_email],
    )

    email.attach(
        f"{invoice_number}.pdf",
        pdf_content,
        "application/pdf"
    )

    email.send()