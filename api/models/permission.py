from api.models import db, TimestampMixin


class Permission(db.Model,TimestampMixin):
    __tablename__ = "permissions"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    description = db.Column(db.String(255),nullable=True)

    user_permissions = db.relationship("UserPermission",back_populates="permission",cascade="all, delete-orphan")    