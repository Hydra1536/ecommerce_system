from decimal import Decimal


def calculate_order_total(items):
    total = Decimal("0.00")
    for item in items:
        total += item["price"] * item["quantity"]
    return total
