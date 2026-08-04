from flask import request
from flask_limiter import Limiter

def rate_limit_key() -> str:
    return (
        request.headers.get("X-Test-Scenario")
        or request.remote_addr
        or "anonymous"
    )

limiter = Limiter(
    key_func=rate_limit_key
)