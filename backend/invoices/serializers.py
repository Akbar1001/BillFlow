from rest_framework import serializers
from .models import Invoice, InvoiceItem


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
    def create(self, validated_data):

        items_data = validated_data.pop("items")

        invoice = Invoice.objects.create(**validated_data)

        for item_data in items_data:

            InvoiceItem.objects.create(
                invoice=invoice,
                description=item_data["description"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                line_total=item_data["quantity"] * item_data["unit_price"],
            )

        return invoice