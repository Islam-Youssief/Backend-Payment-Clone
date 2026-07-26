import uuid

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from api.models import db, TimestampMixin


class Customer(db.Model, TimestampMixin):

    __tablename__ = "customers"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7, nullable=False)
    name= db.Column(db.String(255), nullable=False)
    email= db.Column(db.String(255), nullable=False, unique=True)

    payment_histories = relationship("PaymentHistory", back_populates="customer")