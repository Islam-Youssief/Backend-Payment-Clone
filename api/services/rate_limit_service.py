from api.services.redis_service import RedisService
import api.core.exceptions as exceptions

class RateLimitService:
    def __init__(self, window = 60, limit = 10, redis_service=None):

        self.redis_service = redis_service or RedisService()
        self.window = window
        self.limit = limit

    def check(self, key):
        redis = self.redis_service.redis_client
        current_count = redis.incr(key, amount=1)
        if current_count == 1:
            redis.expire(key, self.window)
        if current_count > self.limit:
            retry_after = redis.ttl(key)
            raise exceptions.RateLimitExceeded(retry_after)
