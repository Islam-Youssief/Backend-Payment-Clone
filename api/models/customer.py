from api.models import db,TimestampMixin

class Customer(db.Model,TimestampMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String,nullable=False,unique=True)

    payments = db.relationship('Payment',back_populates='customer')










