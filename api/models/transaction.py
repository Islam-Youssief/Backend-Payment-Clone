from api.models import db, TimestampMixin


class Transaction(db.Model, TimestampMixin):
    __tablename__ = "transactions"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True,)
    customer_id = db.Column(db.Integer,db.ForeignKey("customers.id",ondelete="CASCADE",),nullable=False,index=True,)
    amount = db.Column(db.Numeric(14, 2),nullable=False,)
    currency = db.Column(db.String(10), nullable=False,default="USD",)
    direction = db.Column(db.String(10),nullable=False,)
    transaction_type = db.Column(db.String(30),nullable=False,)
    title = db.Column(db.String(255), nullable=False,)
    description = db.Column(db.Text,nullable=True,)
    name = db.Column(db.String(255),nullable=True,)
    category = db.Column(db.String(100),nullable=True,)

    customer = db.relationship("Customer",back_populates="transactions",)