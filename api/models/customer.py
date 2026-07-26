import uuid
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from api.models import db, TimestampMixin


class Customer(db.Model, TimestampMixin):
    __tablename__ = 'customers'

    __table_args__ = (
        CheckConstraint("email LIKE '%@%.%'", name='check_valid_email_format'),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

    payment_attempts = db.relationship('PaymentAttempt', backref='customer', lazy=True)
