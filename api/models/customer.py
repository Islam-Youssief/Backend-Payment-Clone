from sqlalchemy.orm import relationship
from api.models import db, TimestampMixin


class Customer(db.Model, TimestampMixin):

    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String(255), nullable=False)
    email= db.Column(db.String(255), nullable=False, unique=True)

    payment_histories = relationship("PaymentHistory", back_populates="customer", cascade="all, delete-orphan")