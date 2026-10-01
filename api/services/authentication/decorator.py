from functools import wraps

import flask as fl

from api.models import User, db
from api.services.authentication.token import TokenService


def require_authentication(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        authorization = fl.request.headers.get("Authorization")

        if not authorization:
            return {
                "message": "Authorization header is required"
            }, 401

        parts = authorization.split()

        if len(parts) != 2 or parts[0] != "Bearer":
            return {
                "message": "Invalid authorization header"
            }, 401

        token = parts[1]

        payload = TokenService.verify_access_token(token)

        if payload is None:
            return {
                "message": "Invalid or expired token"
            }, 401

        try:
            user_id = int(payload["sub"])
        except (KeyError, ValueError, TypeError):
            return {
                "message": "Invalid token payload"
            }, 401

        user = db.session.get(User, user_id)

        if user is None:
            return {
                "message": "User not found"
            }, 401

        return function(user, *args, **kwargs)

    return wrapper