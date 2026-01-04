from payments.strategies.bkash import BkashPayment
from payments.strategies.stripe import StripePayment


def get_payment_strategy(provider):
    if provider == "stripe":
        return StripePayment()
    elif provider == "bkash":
        return BkashPayment()
    else:
        raise ValueError("Invalid payment provider")
