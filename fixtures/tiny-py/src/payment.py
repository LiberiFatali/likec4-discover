class PaymentService:
    def charge(self, amount: int) -> str:
        return f"charged:{amount}"
