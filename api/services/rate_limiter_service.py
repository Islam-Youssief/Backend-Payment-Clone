from datetime import datetime, timezone, timedelta
from api.models import db
from api.models.rate_limit_log import RateLimitLog
from api.core.exceptions import RateLimitExceededError


class RateLimiterService:
    """Database rate limiter using a sliding window algorithm.

    Tracks request timestamps in the ``rate_limit_logs`` table and raises
    :class:`RateLimitExceededError` when the configured limit is exceeded.
    """

    def __init__(self, max_requests=5, window_seconds=60):
        self._max_requests = max_requests
        self._window_seconds = window_seconds

    def check_rate_limit(self, client_ip, endpoint):
        """Check if the client has exceeded the rate limit.

        If the client is within the allowed limit, a new log entry is recorded.
        If the limit is exceeded, :class:`RateLimitExceededError` is raised.
        """
        window_start = datetime.now(timezone.utc) - timedelta(seconds=self._window_seconds)
        request_count = RateLimitLog.query.filter(
            RateLimitLog.client_ip == client_ip,
            RateLimitLog.endpoint == endpoint,
            RateLimitLog.created_at >= window_start
        ).count()
        if request_count >= self._max_requests:
            raise RateLimitExceededError()
        log_entry = RateLimitLog(client_ip=client_ip, endpoint=endpoint)
        db.session.add(log_entry)
        db.session.commit()
