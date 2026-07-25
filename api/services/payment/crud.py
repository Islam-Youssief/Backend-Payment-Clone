from sqlalchemy.exc import SQLAlchemyError

from api.models import Payment, db

class PaymentCrud:

    def create(self, data):
        try:
            payment = Payment(**data)
            db.session.add(payment)
            db.session.commit()
            db.session.refresh(payment)
            return payment
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def get(self, payment_id):
        return Payment.query.filter_by(id=payment_id).first()

    def get_by_idempotency_key(self, key):
        return Payment.query.filter_by(idempotency_key=key).first()

    def list_by_customer(self, customer_id):
        return (
            Payment.query
            .filter_by(customer_id=customer_id)
            .order_by(Payment.created_at.desc())
            .all()
        )
