from flask import request
from flask_limiter import Limiter
from api.services import redis_cashe


def rate_limit_key() -> str:
    return (
        request.headers.get("X-Test-Scenario")
        or request.remote_addr
        or "anonymous"
    )

limiter = Limiter(
    key_func=rate_limit_key,
    storage_uri="redis://localhost:6379",
)
cache = redis_cashe.RedisCache()