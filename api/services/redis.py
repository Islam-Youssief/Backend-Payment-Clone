import redis

import api.core.configurations as config


class RedisService:

    _config = config.RedisConfig()

    _client = redis.Redis.from_url(_config.url,decode_responses=True)

    @staticmethod
    def set(key, value, expires_in):
        RedisService._client.set(key,value,ex=expires_in)

    @staticmethod
    def get(key):
        return RedisService._client.get(key)

    @staticmethod
    def delete(key):
        RedisService._client.delete(key)

    @staticmethod
    def exists(key):
        return RedisService._client.exists(key)