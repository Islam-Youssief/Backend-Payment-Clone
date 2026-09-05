import datetime

import flask_migrate as migrate_ext
import flask_sqlalchemy as sqlalchemy
import hashlib
import secrets

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
    phone = db.Column(db.String(20),unique=True,nullable=True)
    password = db.Column(db.Text, nullable=False)
    salt = db.Column(db.Text, nullable=False)
    totp_secret = db.Column(db.Text, nullable=True)
    totp_enabled = db.Column(db.Boolean, nullable=False, default=False)
    permissions = db.Column(db.Text, nullable=True, default="")

    user_permissions = db.relationship("UserPermission",back_populates="user",cascade="all, delete-orphan")
    tasks = db.relationship("Task",back_populates="user",cascade="all, delete-orphan")

    def set_password(self, password):
        self.salt = secrets.token_hex(32)

        self.password = hashlib.pbkdf2_hmac(
            'sha256',password.encode('utf-8'),self.salt.encode('utf-8'),100_000).hex()

    def check_password(self, password):
        password = hashlib.pbkdf2_hmac(
            'sha256',password.encode('utf-8'),self.salt.encode('utf-8'),100_000).hex()

        return secrets.compare_digest(password,self.password)

from .customer import Customer
from .paymentsHistory import PaymentsHistory
from .idempotencyKeys import IdempotencyKeys
from api.models.transaction import Transaction
from api.models.image import Image
from api.models.permission import Permission
from api.models.userPermission import UserPermission
from api.models.task import Task