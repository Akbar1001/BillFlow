from rest_framework import serializers
from .models import Invoice, InvoiceItem
from django.db import transaction
from decimal import Decimal

class InvoiceItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceItem
        fields = [
            "description",
            "quantity",
            "unit_price",
        ]

class InvoiceSerializer(serializers.ModelSerializer):

    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            "customer",
            "issue_date",
            "due_date",
            "notes",
            "items",
        ]
    @transaction.atomic
    def create(self, validated_data):

        items_data = validated_data.pop("items")

        invoice = Invoice.objects.create(
            **validated_data
        )

        subtotal = Decimal("0.00")

        for item_data in items_data:

            line_total = (
                item_data["quantity"]
                * item_data["unit_price"]
            )

            subtotal += line_total

            InvoiceItem.objects.create(
                invoice=invoice,
                description=item_data["description"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                line_total=line_total,
            )

        invoice.subtotal = subtotal
        invoice.total_amount = (
            subtotal
            + invoice.tax
            - invoice.discount
        )

        invoice.save()

        return invoice
    
    def validate_customer(self, customer):

        request = self.context["request"]

        if customer.user != request.user:
            raise serializers.ValidationError(
            "You cannot create invoices for another user's customer."
            )

        return customer