from throttled import Throttled, RateLimiterType, rate_limiter
import api.core.exceptions as exceptions

class RateLimitService:
    def __init__(self):

        self.throttle = Throttled(
            using = RateLimiterType.FIXED_WINDOW.value,
            quota = rate_limiter.per_min(60),
        )
    
    def check(self, key):
        result = self.throttle.limit(key)
        if result.limited:
            raise exceptions.RateLimitExceeded(result.state.retry_after)