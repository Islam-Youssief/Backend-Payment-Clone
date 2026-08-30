class TransactionSerializer:

    @staticmethod
    def serialize(transaction):
        return {
            "id": transaction.id,
            "customer_id": transaction.customer_id,
            "amount": float(transaction.amount),
            "currency": transaction.currency,
            "direction": transaction.direction,
            "transaction_type": transaction.transaction_type,
            "title": transaction.title,
            "description": transaction.description,
            "name": transaction.name,
            "category": transaction.category,
            "created_at": transaction.created_at.isoformat(),
        }