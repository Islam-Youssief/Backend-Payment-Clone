from api.services.transaction import TransactionService
from api.core.serializers.transaction_serializer import TransactionSerializer
from flask import request

class TransactionController:

    @staticmethod
    def get_by_customer_id(customer_id):
        limit = request.args.get("limit", 50, type=int)
        cursor = request.args.get("cursor", type=int)

        limit = min(max(limit, 1), 100)

        transactions, next_cursor, has_more = (
            TransactionService.get_by_customer_id(
                customer_id,
                limit=limit,
                cursor_id=cursor,
            )
        )

        return {
            "items": [
                TransactionSerializer.serialize(transaction)
                for transaction in transactions
            ],
            "pagination": {
                "next_cursor": next_cursor,
                "has_more": has_more,
            },
        }
    @staticmethod
    def get_spending_by_category(customer_id):
        return {
            "items": TransactionService.get_spending_by_category(customer_id)
        }