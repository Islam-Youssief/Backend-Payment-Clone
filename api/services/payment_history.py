from api.models import PaymentsHistory

class PaymentHistoryService:

    @staticmethod
    def get_all():
        return PaymentsHistory.query.all()

    @staticmethod
    def get_by_id(payment_id):
        return PaymentsHistory.query.get(payment_id)