from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.models import Customer
from invoices.models import Invoice, InvoiceStatus


class DashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        customers = Customer.objects.filter(
            user=request.user
        )

        invoices = Invoice.objects.filter(
            customer__user=request.user
        )

        total_revenue = invoices.filter(
            status=InvoiceStatus.PAID
        ).aggregate(
            revenue=Sum("total_amount")
        )["revenue"] or 0

        data = {
            "total_customers": customers.count(),
            "total_invoices": invoices.count(),
            "paid_invoices": invoices.filter(
                status=InvoiceStatus.PAID
            ).count(),
            "pending_invoices": invoices.exclude(
                status=InvoiceStatus.PAID
            ).count(),
            "overdue_invoices": invoices.filter(
                status=InvoiceStatus.OVERDUE
            ).count(),
            "total_revenue": total_revenue,
        }

        return Response(data)