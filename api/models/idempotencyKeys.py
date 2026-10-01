from api.models import db,TimestampMixin
from sqlalchemy.dialects.postgresql import JSONB



class IdempotencyKeys(db.Model,TimestampMixin):
    __tablename__ = "idempotency_keys"

    idempotencyKey = db.Column(db.String(255),primary_key = True)
    status = db.Column(db.String(32),nullable = False, default = "PROCESSING")
    response_body = db.Column(JSONB, nullable=True)
    response_code = db.Column(db.Integer, nullable=True)
    request_hash = db.Column(db.String(64), nullable=False)
