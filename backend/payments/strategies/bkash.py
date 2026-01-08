# payments/strategies/bkash.py

import uuid
import requests
from django.conf import settings
from payments.models import Payment
from payments.services import finalize_order
from payments.strategies.base import PaymentStrategy


class BkashPayment(PaymentStrategy):

    def __init__(self):
        self.base_url = settings.BKASH_BASE_URL
        self.app_key = settings.BKASH_APP_KEY
        self.app_secret = settings.BKASH_APP_SECRET
        self.username = settings.BKASH_USERNAME
        self.password = settings.BKASH_PASSWORD
        self.token = None
        self.is_demo = True  # Force demo mode for testing

    def grant_token(self):
        url = f"{self.base_url}/tokenized/checkout/token/grant"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "username": self.username,
            "password": self.password,
        }
        data = {
            "app_key": self.app_key,
            "app_secret": self.app_secret,
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            self.token = response.json().get("id_token")
            return self.token
        else:
            raise Exception(f"Failed to grant token: {response.text}")

    def create_payment(self, amount, order_id):
        if self.is_demo:
            # Return mock data for demo
            return {
                "paymentID": f"DEMO-{uuid.uuid4().hex[:10]}",
                "createTime": "2024-01-08T15:52:00.000Z",
                "orgLogo": "",
                "orgName": "Demo Merchant",
                "transactionStatus": "Initiated",
                "amount": str(amount),
                "currency": "BDT",
                "intent": "sale",
                "merchantInvoiceNumber": f"INV-{order_id}"
            }

        if not self.token:
            self.grant_token()
        url = f"{self.base_url}/tokenized/checkout/create"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": self.token,
            "X-APP-Key": self.app_key,
        }
        data = {
            "mode": "0011",
            "payerReference": str(order_id),
            "amount": str(amount),
            "currency": "BDT",
            "intent": "sale",
            "merchantInvoiceNumber": f"INV-{order_id}",
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to create payment: {response.text}")

    def execute_payment(self, payment_id):
        if self.is_demo:
            # Return mock success for demo
            return {
                "paymentID": payment_id,
                "createTime": "2024-01-08T15:52:00.000Z",
                "updateTime": "2024-01-08T15:52:30.000Z",
                "trxID": f"DEMO-TRX-{uuid.uuid4().hex[:8]}",
                "transactionStatus": "Completed",
                "amount": "100.00",
                "currency": "BDT",
                "intent": "sale",
                "merchantInvoiceNumber": "DEMO-INV-123"
            }

        if not self.token:
            self.grant_token()
        url = f"{self.base_url}/tokenized/checkout/execute"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": self.token,
            "X-APP-Key": self.app_key,
        }
        data = {"paymentID": payment_id}
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to execute payment: {response.text}")

    def initiate_payment(self, order):
        # For bKash, initiate might not create payment yet, but prepare data for frontend
        # Frontend will call create via JS
        payment_id = f"BKASH-{uuid.uuid4().hex[:10]}"

        response = {
            "paymentID": payment_id,
            "amount": str(order.total_amount),
            "status": "pending"
        }

        Payment.objects.create(
            order=order,
            provider="bkash",
            session_id=payment_id,
            status="pending",
            raw_response=response,
        )

        return response

    def verify_payment(self, payment_id):
        print(f"verify_payment called with payment_id: {payment_id}")
        try:
            payment = Payment.objects.get(
                session_id=payment_id,
                provider="bkash"
            )
            print(f"Found payment: {payment.id}, current status: {payment.status}")
        except Payment.DoesNotExist:
            print(f"Payment not found for payment_id: {payment_id}")
            return

        payment.status = "success"
        payment.order.status = "paid"
        print(f"Updated payment status to: {payment.status}, order status to: {payment.order.status}")

        finalize_order(payment)

        payment.raw_response = {
            "paymentID": payment_id,
            "status": "success"
        }

        payment.order.save()
        payment.save()
        print("Payment and order saved successfully")
