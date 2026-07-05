from django.urls import path
from .views import UserListAPIView

urlpatterns = [
    path("", UserListAPIView.as_view(), name="user-list"),
    path("register/", RegisterAPIView.as_view(), name="register"),
]