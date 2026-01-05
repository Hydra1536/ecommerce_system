from django.db import transaction


@transaction.atomic
def reduce_stock_for_order(order):
    for item in order.items.select_related("product"):
        product = item.product

        if product.stock < item.quantity:
            raise Exception(f"Insufficient stock for {product.name}")

        product.stock -= item.quantity
        product.save()
