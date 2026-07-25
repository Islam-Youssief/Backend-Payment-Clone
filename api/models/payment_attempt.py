import uuid
from sqlalchemy.dialects.postgresql import UUID
from api.models import db, TimestampMixin

class PaymentAttempt(db.Model, TimestampMixin):
    __tablename__ = 'payment_attempts'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7)
    customer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('customers.id', ondelete='SET NULL'), nullable=True)
    
    # Denormalized fields to survive customer deletion
    customer_name = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False)
    
    provider = db.Column(db.String(50), nullable=False) # e.g., 'FAWRY', 'STRIPE'
    provider_reference = db.Column(db.String(255), nullable=True)
    idempotency_key = db.Column(UUID(as_uuid=True), unique=True, nullable=True)
    
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False, default='EGP')
    
    status = db.Column(db.String(50), nullable=False, default='PENDING') # PENDING, SUCCESS, FAILED, DECLINED
    failure_reason = db.Column(db.Text, nullable=True)

