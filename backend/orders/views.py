from django.db import transaction
from django.shortcuts import render
from payments.models import Payment
from products.models import Product
from products.permissions import IsAdmin
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

# Create your views here.
from rest_framework.views import APIView

from .models import Order, OrderItem
from .serializers import OrderSerializer
from .utils import calculate_order_total


class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        items = request.data.get("items", [])

        if not items:
            return Response({"error": "No items provided"}, status=400)

        order = Order.objects.create(user=request.user)
        order_items_data = []

        for item in items:
            try:
                product = Product.objects.get(id=item["product_id"])
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Product {item['product_id']} not found"}, status=400
                )
            price = product.price
            quantity = item["quantity"]
            subtotal = price * quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
                subtotal=subtotal,
            )

            order_items_data.append({"price": price, "quantity": quantity})

        order.total_amount = calculate_order_total(order_items_data)
        order.save()

        return Response(OrderSerializer(order).data, status=201)


class UserOrdersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return Response(OrderSerializer(orders, many=True).data)


class AdminOrdersView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all().select_related("user")

    def get(self, request):
        orders = Order.objects.all()
        return Response(OrderSerializer(orders, many=True).data)


class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        total_products = Product.objects.count()
        total_orders = Order.objects.count()
        total_payments = Payment.objects.count()
        pending_orders = Order.objects.filter(status="pending").count()

        return Response(
            {
                "total_products": total_products,
                "total_orders": total_orders,
                "total_payments": total_payments,
                "pending_orders": pending_orders,
            }
        )
