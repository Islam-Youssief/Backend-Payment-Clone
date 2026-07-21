import datetime

import flask_migrate as migrate_ext
import flask_sqlalchemy as sqlalchemy

db = sqlalchemy.SQLAlchemy()
migrate = migrate_ext.Migrate()


def _utcnow():
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.datetime.now(datetime.timezone.utc)


class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), default=_utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=_utcnow, nullable=False, onupdate=_utcnow)


class User(db.Model, TimestampMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    salt = db.Column(db.Text, nullable=False)


from api.models.customer import Customer
from api.models.payment_attempt import PaymentAttempt

__all__ = ['db', 'migrate', 'TimestampMixin', 'User', 'Customer', 'PaymentAttempt']
