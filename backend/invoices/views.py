from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Invoice
from .serializers import InvoiceSerializer

from django.http import HttpResponse
from rest_framework.decorators import action

from utils.pdf_generator import (
    generate_invoice_pdf,
)

from rest_framework.decorators import action
from rest_framework.response import Response

from utils.email_service import send_invoice_email
from utils.pdf_generator import generate_invoice_pdf

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(
            customer__user=self.request.user
        )
    
    @action(
        detail=True,
        methods=["get"],
    )   
    def pdf(self, request, pk=None):

        invoice = self.get_object()

        pdf = generate_invoice_pdf(
            invoice
        )

        response = HttpResponse(
            pdf,
            content_type="application/pdf"
        )

        response[
            "Content-Disposition"
        ] = (
            f'attachment; '
            f'filename="{invoice.invoice_number}.pdf"'
        )

        return response

    @action(
    detail=True,
    methods=["post"],
    )
    def send_email(self, request, pk=None):

        invoice = self.get_object()

        pdf = generate_invoice_pdf(invoice)

        send_invoice_email(
            invoice.customer.email,
            invoice.invoice_number,
            pdf,
        )

        invoice.status = InvoiceStatus.SENT
        invoice.save()

        return Response(
            {
                "message": "Invoice sent successfully."
            }
        )