from api.models import db,TimestampMixin



class customer(db.Model, TimestampMixin):
    __tablename__ = "customers"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False,unique=True)
    
    payments = db.relationship("payemntsHistory",back_populates="customer")