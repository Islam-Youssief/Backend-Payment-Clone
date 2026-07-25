from api.models import db,TimestampMixin


class Payment(db.Model, TimestampMixin):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    idempotency_key = db.Column(db.String(255),
                                unique=True,
                                nullable=False
    )
    customer_id = db.Column(db.Integer,
                            db.ForeignKey('customers.id'),
                            nullable=False
    )
    provider = db.Column(db.String(20), nullable=False)
    provider_reference = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    failure_reason = db.Column(db.String(255), nullable=True)

    customer = db.relationship('Customer',back_populates='payments')