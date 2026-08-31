from api.models import db, TimestampMixin

class UserPermission(db.Model, TimestampMixin):
    __tablename__ = "user_permissions"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id",ondelete="CASCADE",),nullable=False)
    permission_id = db.Column(db.Integer,db.ForeignKey("permissions.id",ondelete="CASCADE",),nullable=False)

    user = db.relationship("User",back_populates="user_permissions")
    permission = db.relationship("Permission",back_populates="user_permissions")