import redis
import json

class RedisService:
    def __init__(self, redis_client=None):
        self._redis_client = redis_client or redis.Redis(host='localhost', port=6379, db=0, decode_responses=True) 

    @property
    def redis_client(self):
        return self._redis_client
    
    def set_value(self, key, value, ttl):
        self._redis_client.set(key, json.dumps(value), ex=ttl)

    def get_value(self, key):
        value = self._redis_client.get(key)
        if value is None:
            return None
        return json.loads(value)
