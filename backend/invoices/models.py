from django.db import models
from customers.models import Customer
from django.utils import timezone

class InvoiceStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    SENT = "SENT", "Sent"
    PAID = "PAID", "Paid"
    OVERDUE = "OVERDUE", "Overdue"

class Invoice(models.Model):

    customer = models.ForeignKey(
    Customer,
    on_delete=models.CASCADE,
    related_name="invoices",
    )

    invoice_number = models.CharField(
    max_length=30,
    unique=True,
    blank=True,
    )

    issue_date = models.DateField()

    due_date = models.DateField()

    status = models.CharField(
    max_length=20,
    choices=InvoiceStatus.choices,
    default=InvoiceStatus.DRAFT,
    )

    notes = models.TextField(
    blank=True,
    )

    subtotal = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    )

    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def save(self, *args, **kwargs):

        if not self.invoice_number:

            year = timezone.now().year

            last_invoice = Invoice.objects.filter(
                invoice_number__startswith=f"INV-{year}"
            ).order_by("-id").first()

            if last_invoice:
                last_number = int(
                    last_invoice.invoice_number.split("-")[-1]
                ) + 1
            else:
                last_number = 1

            self.invoice_number = (
                f"INV-{year}-{last_number:04d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number
    
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
    Invoice,
    on_delete=models.CASCADE,
    related_name="items",
    )

    description = models.CharField(
    max_length=255,
    )
    
    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    )

    line_total = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    )

    def __str__(self):
        return self.description