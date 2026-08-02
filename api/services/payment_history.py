from api.models import PaymentsHistory,db

class PaymentHistoryService:

    @staticmethod
    def get_all():
        return PaymentsHistory.query.all()

    @staticmethod
    def get_by_id(payment_id):
        return PaymentsHistory.query.get(payment_id)

    @staticmethod
    def get_by_customer_id(customer_id):
        return PaymentsHistory.query.filter_by(customer_id=customer_id).all()

    @staticmethod
    def update_status_by_transaction_id(transaction_id,status,failure_reason=None):
        payment = PaymentsHistory.query.filter_by(transaction_id=transaction_id).first()
        if payment:
            payment.status = status
            if failure_reason:
                payment.failure_reason = failure_reason
                db.session.commit()
        return payment
    