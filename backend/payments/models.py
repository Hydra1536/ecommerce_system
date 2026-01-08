from django.db import models
from orders.models import Order


class Payment(models.Model):
    PROVIDER_CHOICES = (
        ("stripe", "Stripe"),
        ("bkash", "bKash"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)

    session_id = models.CharField(max_length=255, unique=True)
    payment_intent_id = models.CharField(
        max_length=255, null=True, blank=True
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )

    raw_response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} - {self.session_id}"
