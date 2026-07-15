from django.db import models
from invoices.models import Invoice
from django.db.models import Sum
from invoices.models import InvoiceStatus

class PaymentMethod(models.TextChoices):
    CASH = "CASH", "Cash"
    UPI = "UPI", "UPI"
    BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"
    CARD = "CARD", "Card"


class Payment(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True,
    )

    payment_date = models.DateField()

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

        total_paid = self.invoice.payments.aggregate(
            total=Sum("amount")
        )["total"] or 0

        if total_paid >= self.invoice.total_amount:
            self.invoice.status = InvoiceStatus.PAID
        else:
            self.invoice.status = InvoiceStatus.SENT

        self.invoice.save()

    def __str__(self):
        return self.transaction_id