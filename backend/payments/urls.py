from django.urls import path

from .views import AllPaymentsView, InitiatePaymentView, stripe_webhook, BkashCreateView, BkashExecuteView

urlpatterns = [
    path("all/", AllPaymentsView.as_view()),
    path("pay/<int:order_id>/", InitiatePaymentView.as_view()),
    path("stripe/webhook/", stripe_webhook),
    path("bkash/create/", BkashCreateView.as_view()),
    path("bkash/execute/", BkashExecuteView.as_view()),
]
