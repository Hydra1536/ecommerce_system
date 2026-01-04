from orders.services import reduce_stock_after_payment


def finalize_order(payment):
    order = payment.order

    if payment.status != "success":
        return

    reduce_stock_after_payment(order)
    order.status = "paid"
    order.save()
