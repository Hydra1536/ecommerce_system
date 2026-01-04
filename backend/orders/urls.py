from django.urls import path

from .views import AdminOrdersView, CreateOrderView, UserOrdersView

urlpatterns = [
    path("create/", CreateOrderView.as_view()),
    path("my-orders/", UserOrdersView.as_view()),
    path("admin-orders/", AdminOrdersView.as_view()),
]
