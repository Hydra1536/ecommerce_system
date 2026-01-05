from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from payments.factory import get_payment_strategy


class InitiatePaymentView(APIView):
    def post(self, request, order_id):
        provider = request.data.get("provider")
        order = Order.objects.get(id=order_id)

        strategy = get_payment_strategy(provider)
        result = strategy.initiate_payment(order)

        if provider == "bkash":
            strategy.verify_payment(result["paymentID"])

        return Response(result)


import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from payments.strategies.stripe import StripePayment


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = stripe.Event.construct_from(stripe.util.json.loads(payload), stripe.api_key)

    if event["type"] == "payment_intent.succeeded":
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
