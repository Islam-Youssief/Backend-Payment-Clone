from api.services.redis import RedisService
from api.services.rate_limiter import RateLimiter

redis_service = RedisService()
rate_limiter = RateLimiter(redis_service, fail_open=True)