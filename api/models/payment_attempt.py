from api.models import db, TimestampMixin

class PaymentAttempt(db.Model, TimestampMixin):
    __tablename__ = 'payment_attempts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='SET NULL'), nullable=True)
    
    # Denormalized fields to survive customer deletion
    customer_name = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False)
    
    provider = db.Column(db.String(50), nullable=False) # e.g., 'FAWRY', 'STRIPE'
    provider_reference = db.Column(db.String(255), nullable=True)
    
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False, default='EGP')
    
    status = db.Column(db.String(50), nullable=False, default='PENDING') # PENDING, SUCCESS, FAILED, DECLINED
    failure_reason = db.Column(db.Text, nullable=True)

