import time
import functools
from flask import jsonify, request
import api.core.exceptions as exc

class RateLimiter:
    def __init__(self, redis_service, fail_open=True):
        self._redis = redis_service
        self._fail_open = fail_open

    def limit(self, max_requests, window_seconds, key_func=None):
        def decorator(f):
            @functools.wraps(f)
            def wrapped(*args, **kwargs):
                identity = key_func(request) if key_func else request.remote_addr
                window = int(time.time() // window_seconds)
                redis_key = f"ratelimit:{f.__name__}:{identity}:{window}"

                try:
                    count = self._redis.increment(redis_key, ttl=window_seconds)
                except exc.RedisServiceError:
                    if self._fail_open:
                        return f(*args, **kwargs)
                    return jsonify({"error": "Service temporarily unavailable"}), 503

                if count > max_requests:
                    return jsonify({"error": "Rate limit exceeded"}), 429

                return f(*args, **kwargs)
            return wrapped
        return decorator