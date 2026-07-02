from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    email_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name