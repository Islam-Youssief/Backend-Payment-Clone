import uuid

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from api.models import db, TimestampMixin


class PaymentHistory(db.Model, TimestampMixin):
    
    __tablename__ = "payment_history"
    id= db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7, nullable=False)
    customer_id= db.Column(UUID(as_uuid=True), db.ForeignKey("customers.id"), nullable=False)
    idempotency_key= db.Column(UUID(as_uuid=True), nullable=False, unique=True)
    checkout_payment_id= db.Column(UUID(as_uuid=True), nullable=False, unique=True)
    amount= db.Column(db.Float, nullable=False)
    currency= db.Column(db.String(10), nullable=False)
    status= db.Column(db.String(50), nullable=False)
    failure_reason= db.Column(db.String(255), nullable=True)

    customer= relationship("Customer", back_populates="payment_histories")