from api.models import db, TimestampMixin


class Image(db.Model, TimestampMixin):
    __tablename__ = "images"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True,)
    path = db.Column( db.String(500),nullable=False,)