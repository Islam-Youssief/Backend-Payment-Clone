from api.models import db, TimestampMixin

class Task(db.Model, TimestampMixin):
    __tablename__ = "tasks"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    name = db.Column(db.String(255),nullable=False)
    description = db.Column(db.Text,nullable=True)
    status = db.Column(db.String(30),nullable=False,default="todo")
    started_at = db.Column(db.DateTime(timezone=True),nullable=True)
    completed_at = db.Column(db.DateTime(timezone=True),nullable=True)

    user = db.relationship("User",back_populates="tasks")