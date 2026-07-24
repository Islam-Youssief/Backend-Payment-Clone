from sqlalchemy.orm import relationship
from api.models import db, TimestampMixin


class PaymentHistory(db.Model, TimestampMixin):
    
    __tablename__ = "payment_history"
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id= db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    checkout_payment_id= db.Column(db.String(255), nullable=False, unique=True)
    amount= db.Column(db.Float, nullable=False)
    currency= db.Column(db.String(10), nullable=False)
    status= db.Column(db.String(50), nullable=False)
    failure_reason= db.Column(db.String(255), nullable=True)

    customer= relationship("Customer", back_populates="payment_histories")