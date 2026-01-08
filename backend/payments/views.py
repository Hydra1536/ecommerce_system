from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from payments.factory import get_payment_strategy
from payments.strategies.bkash import BkashPayment
import logging
logger = logging.getLogger(__name__)


class InitiatePaymentView(APIView):

    def post(self, request, order_id):
        provider = request.data.get("provider")
        order = Order.objects.get(id=order_id)

        strategy = get_payment_strategy(provider)
        result = strategy.initiate_payment(order)

        return Response(result, status=200)


import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from payments.strategies.stripe import StripePayment


# payments/views.py

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    print ("PAYLOAD", payload)
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except Exception as e:
        logger.error(f"Stripe webhook error: {e}")
        return JsonResponse({"error": str(e)}, status=400)

    logger.info(f"Stripe event: {event['type']}")

    if event["type"] == "checkout.session.completed":
        print("EVENT DATA", event)
        StripePayment().verify_payment(event)

    return JsonResponse({"status": "ok"})




from rest_framework.permissions import IsAdminUser

from payments.models import Payment
from payments.serializer import PaymentSerializer


class AllPaymentsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        payments = Payment.objects.select_related("order")
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)


class BkashCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        amount = request.data.get("amount")

        try:
            order = Order.objects.get(id=order_id, user=request.user)
            bkash = BkashPayment()
            result = bkash.create_payment(amount, order_id)

            # Update the payment record with the correct paymentID
            if result.get("paymentID"):
                try:
                    payment = Payment.objects.get(
                        order=order,
                        provider="bkash",
                        status="pending"
                    )
                    payment.session_id = result["paymentID"]
                    payment.save()
                    print(f"Updated payment session_id to: {result['paymentID']}")
                except Payment.DoesNotExist:
                    print("No pending payment found to update")

            return Response(result, status=200)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
        except Exception as e:
            logger.error(f"bKash create error: {e}")
            return Response({"error": str(e)}, status=400)


class BkashExecuteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get("paymentID")

        try:
            bkash = BkashPayment()
            result = bkash.execute_payment(payment_id)

            # If successful, verify the payment
            if result.get("transactionStatus") == "Completed":
                strategy = get_payment_strategy("bkash")
                strategy.verify_payment(payment_id)
            return Response(result, status=200)
        except Exception as e:
            logger.error(f"bKash execute error: {e}")
            return Response({"error": str(e)}, status=400)
