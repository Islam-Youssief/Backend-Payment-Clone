import uuid
from sqlalchemy.dialects.postgresql import UUID
from api.models import db, TimestampMixin


class Customer(db.Model, TimestampMixin):
    __tablename__ = 'customers'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    payment_attempts = db.relationship('PaymentAttempt', backref='customer', lazy=True)
