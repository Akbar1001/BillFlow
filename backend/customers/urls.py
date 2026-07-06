from django.urls import path
from .views import CustomerListCreateAPIView

urlpatterns = [
    path("", CustomerListCreateAPIView.as_view(), name="customer-list-create"),
]