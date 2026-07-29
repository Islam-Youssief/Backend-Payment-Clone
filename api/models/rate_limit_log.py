import uuid
from sqlalchemy.dialects.postgresql import UUID
from api.models import db, TimestampMixin


class RateLimitLog(db.Model, TimestampMixin):
    __tablename__ = 'rate_limit_logs'

    __table_args__ = (
        db.Index('ix_rate_limit_lookup', 'client_ip', 'endpoint', 'created_at'),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7)
    client_ip = db.Column(db.String(45), nullable=False)
    endpoint = db.Column(db.String(255), nullable=False)
