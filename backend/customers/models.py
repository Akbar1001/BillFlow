from django.db import models
from django.conf import settings


class Customer(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customers",
    )

    company_name = models.CharField(
        max_length=200,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=15
    )

    gst_number = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.company_name or self.name