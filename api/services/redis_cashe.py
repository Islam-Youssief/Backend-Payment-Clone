import json
import redis


class RedisCache:

    def __init__(self):
        self.client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )

    def set(self,key, value, ttl=300):
        self.client.set(
            key,
            json.dumps(value),
            ex=ttl
        )

    def get(self, key):
        value = self.client.get(key)

        if value is None:
            return None
        return json.loads(value)

    def delete(self, key):
        self.client.delete(key)
