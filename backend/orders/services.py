from django.db import transaction
from orders.models import OrderItem
from products.models import Product


@transaction.atomic
def reduce_stock_after_payment(order):
    """
    Reduce product stock safely after successful payment
    """
    items = OrderItem.objects.select_related("product").filter(order=order)

    for item in items:
        product = Product.objects.select_for_update().get(id=item.product.id)

        if product.stock < item.quantity:
            raise Exception("Insufficient stock")

        product.stock -= item.quantity
        product.save()
