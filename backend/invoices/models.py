from django.db import models
from customers.models import Customer

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