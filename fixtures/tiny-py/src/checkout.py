from .payment import PaymentService


def checkout(amount: int) -> str:
    return PaymentService().charge(amount)
