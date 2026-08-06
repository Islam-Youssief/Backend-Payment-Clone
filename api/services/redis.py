import redis
import api.core.configurations as config
import json
import logging
import api.core.exceptions as exc
logger = logging.getLogger(__name__)


class RedisService:
    def __init__(self,redis_client = None):
        try:
            self._redis_client = redis_client or redis.Redis.from_url(config.AppConfig().redis_url, decode_responses=True)
        except redis.exceptions.RedisError as e:
            logger.error(f"Error initializing Redis client: {e}")
            raise exc.RedisServiceError("Failed to initialize Redis client") from e

    def redis_client(self):
        return self._redis_client

    def set(self,key,value,ttl=None):
        try:
            serrialized = json.dumps(value)
        except (TypeError, ValueError) as e:
            logger.error(f"Error serrializing value for key {key}: {e}")
            raise exc.RedisServiceError(f"Failed to serrialize value for key {key}") from e
        try:
            return self._redis_client.set(key,serrialized,ex=ttl)
        except redis.exceptions.RedisError as e:
            logger.error(f"Error setting key {key} in Redis: {e}")
            raise exc.RedisServiceError(f"Failed to set key {key} in Redis") from e

    def get(self,key):
        try:
            value = self._redis_client.get(key)
        except redis.exceptions.RedisError as e:
            logger.error(f"Error getting key {key} from Redis: {e}")
            raise exc.RedisServiceError(f"Failed to get key {key} from Redis") from e
        if value is None:
            return None
        try:
            return json.loads(value)
        except (TypeError, ValueError) as e:
            logger.error(f"Error deserrializing value for key {key}: {e}")
            raise exc.RedisServiceError(f"Failed to deserrialize value for key {key}") from e

    def delete(self,key):
        try:
            return self._redis_client.delete(key)
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis DELETE failed for key '{key}': {e}")
            raise exc.RedisServiceError(f"Failed to delete key '{key}'") from e

    def clear(self):
        try:
            return self._redis_client.flushdb()
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis FLUSHDB failed: {e}")
            raise exc.RedisServiceError("Failed to clear Redis DB") from e

    def increment(self, key, ttl=None):
        try:
            value = self._redis_client.incr(key)
            if ttl and value == 1:
                self._redis_client.expire(key, ttl)
            return value
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis INCR failed for key '{key}': {e}")
            raise exc.RedisServiceError(f"Failed to increment key '{key}'", key=key) from e