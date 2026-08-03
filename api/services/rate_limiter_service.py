from api.core.exceptions import RateLimitExceededError
from api.services.redis_service import RedisService


class RateLimiterService:
    """Redis-backed rate limiter using a sliding window counter."""

    def __init__(self, max_requests=5, window_seconds=60, redis_service=None):
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._redis = redis_service or RedisService()

    def check_rate_limit(self, client_ip, endpoint):
        """Check if the client has exceeded the rate limit."""
        key = f"rate_limit:{client_ip}:{endpoint}"
        current_count = self._redis.incr(key)
        if current_count == 1:
            self._redis.expire(key, self._window_seconds)
        if current_count > self._max_requests:
            raise RateLimitExceededError()
