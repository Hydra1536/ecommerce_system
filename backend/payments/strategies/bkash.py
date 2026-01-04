import uuid

import requests
from payments.models import Payment
from payments.services import finalize_order
from payments.strategies.base import PaymentStrategy
from products.utils import reduce_stock_for_order


class BkashPayment(PaymentStrategy):

    def initiate_payment(self, order):
        unique_id = f"BKASH-{uuid.uuid4().hex[:8].upper()}"

        response = {"paymentID": unique_id, "status": "pending"}

        Payment.objects.create(
            order=order,
            provider="bkash",
            transaction_id=response["paymentID"],
            status="pending",
            raw_response=response,
        )

        return response

    def verify_payment(self, payment_id):
        # Simulate bKash execute/query success
        payment = Payment.objects.get(transaction_id=payment_id)

        payment.status = "success"
        payment.order.status = "paid"
        # reduce_stock_for_order(payment.order)
        finalize_order(payment)

        payment.raw_response = {"paymentID": payment_id, "status": "success"}

        payment.order.save()
        payment.save()
