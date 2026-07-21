from api.models import db, TimestampMixin


class Customer(db.Model, TimestampMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    payment_attempts = db.relationship('PaymentAttempt', backref='customer', lazy=True)
