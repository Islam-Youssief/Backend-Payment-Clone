from api.models import db,TimestampMixin


class PaymentsHistory(db.Model,TimestampMixin):
    __tablename__ = "payments_history"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    transaction_id = db.Column(db.String(255),nullable=False,unique=True)
    customer_id = db.Column(db.Integer,db.ForeignKey("customers.id"),nullable=False)
    amount = db.Column(db.Numeric(10,2),nullable=False)
    currency = db.Column(db.String(50),nullable=False)
    provider = db.Column(db.String(50),nullable=False)
    status = db.Column(db.String(20),nullable=False)
    failure_reason = db.Column(db.Text,nullable=True)
    payment_type = db.Column(db.String(60))

    customer = db.relationship("Customer",back_populates="payments")