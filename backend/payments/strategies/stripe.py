import stripe
from django.conf import settings
from payments.models import Payment
from payments.services import finalize_order
from payments.strategies.base import PaymentStrategy

from .base import PaymentStrategy

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripePayment(PaymentStrategy):

    def initiate_payment(self, order):
        intent = stripe.PaymentIntent.create(
            amount=int(order.total_amount * 100),
            currency="usd",
            metadata={"order_id": order.id},
        )

        Payment.objects.create(
            order=order,
            provider="stripe",
            transaction_id=intent.id,
            status="pending",
            raw_response=intent,
        )

        return intent.client_secret

    def verify_payment(self, event):
        intent = event["data"]["object"]
        payment = Payment.objects.get(transaction_id=intent.id)

        if intent.status == "succeeded":
            payment.status = "success"
            payment.order.status = "paid"
            finalize_order(payment)
        else:
            payment.status = "failed"

        payment.raw_response = event
        payment.payment.order.save()
        payment.save()
