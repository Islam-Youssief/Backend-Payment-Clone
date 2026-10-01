from api.models import Transaction
from sqlalchemy import func

class TransactionService:

    @staticmethod
    def get_by_customer_id(customer_id, limit=10, cursor_id=None):
        query = (Transaction.query.filter(Transaction.customer_id == customer_id))

        if cursor_id is not None:
            query = query.filter(Transaction.id < cursor_id)

        transactions = (query.order_by(Transaction.id.desc()).limit(limit + 1).all())

        has_more = len(transactions) > limit

        if has_more:
            transactions = transactions[:limit]

        next_cursor = transactions[-1].id if has_more else None

        return transactions, next_cursor, has_more

    @staticmethod
    def get_spending_by_category(customer_id):
        results = (
            Transaction.query
            .with_entities(
                Transaction.category,
                func.sum(Transaction.amount).label("amount")
            )
            .filter(
                Transaction.customer_id == customer_id,
                Transaction.direction == "debit",
                Transaction.category.isnot(None),
            )
            .group_by(Transaction.category).order_by(func.sum(Transaction.amount).desc()).all()
        )

        return [
            {
                "category": category,
                "amount": float(amount),
            }
            for category, amount in results
        ]
    