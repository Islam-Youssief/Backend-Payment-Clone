import redis
import api.core.configurations as configurations


class RedisService:

    def __init__(self, app_config=None, redis_client=None):
        config = app_config or configurations.AppConfig()
        self._client = redis_client or redis.Redis(
            host=config.redis_host,
            port=config.redis_port,
            db=config.redis_db,
        )

    def incr(self, key):
        """Increment the integer value of *key* by one and return the new value."""
        return self._client.incr(key)

    def expire(self, key, seconds):
        """Set a timeout on *key* in seconds."""
        return self._client.expire(key, seconds)

    def get(self, key):
        """Return the value of *key*, or ``None`` if it does not exist."""
        return self._client.get(key)

    def delete(self, *keys):
        """Delete one or more keys."""
        return self._client.delete(*keys)

    def flush_pattern(self, pattern):
        """Delete all keys matching a glob *pattern*."""
        keys = self._client.keys(pattern)
        if keys:
            self._client.delete(*keys)
