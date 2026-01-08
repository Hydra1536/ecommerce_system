# payments/strategies/stripe.py

import stripe
from django.conf import settings

from payments.models import Payment
from payments.services import finalize_order
from payments.strategies.base import PaymentStrategy

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripePayment(PaymentStrategy):

    def initiate_payment(self, order):
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Order #{order.id}",
                    },
                    "unit_amount": int(order.total_amount * 100),
                },
                "quantity": 1,
            }],
            success_url="https://winded-morphotic-otis.ngrok-free.dev/orders/",
            cancel_url="https://winded-morphotic-otis.ngrok-free.dev/checkout/",
            metadata={"order_id": str(order.id)},
        )

        Payment.objects.create(
            order=order,
            provider="stripe",
            session_id=session.id,
            status="pending",
            raw_response=session.to_dict(),
        )

        return session.url

    def verify_payment(self, event):
        session = event["data"]["object"]
        # print("THIS IS RESPONSE", session)

        session_id = session["id"]
        payment_status = session["payment_status"]
        payment_intent = session.get("payment_intent")

        try:
            payment = Payment.objects.get(
                session_id=session_id,
                provider="stripe"
            )
            # print("PAYMENT FOUND", payment)
        except Payment.DoesNotExist:
            return

        # if payment.status == "success":
        #     return  # idempotency

        if payment_status == "paid":
            payment.status = "success"
            payment.payment_intent_id = payment_intent
            payment.order.status = "paid"

            finalize_order(payment)
        # print("EVENT DATA", event)
        payment.raw_response = event
        payment.order.save()
        payment.save()
