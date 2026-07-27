

class PaymentHistorySerializer:

    def __init__(self,payment):
        self._payment = payment

    def serialize(self):
        return{
            "id": self._payment.id,
            "transaction_id": self._payment.transaction_id,
            "customer_id": self._payment.customer_id,
            "customer_name": self._payment.customer.name,
            "customer_email": self._payment.customer.email,
            "amount": float(self._payment.amount),
            "currency": self._payment.currency,
            "provider": self._payment.provider,
            "status": self._payment.status,
            "failure_reason": self._payment.failure_reason,
            "payment_type": self._payment.payment_type,
            "created_at": self._payment.created_at.isoformat(),
            "updated_at": self._payment.updated_at.isoformat(), 
        }