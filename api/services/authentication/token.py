import jwt
import uuid
from datetime import datetime, timedelta, timezone
import api.core.configurations as config

class TokenService:

    @staticmethod
    def _secret():
        secret = config.TotpConfig.jwt_secret_key
        if not secret:
            raise RuntimeError("JWT_SECRET_KEY is not configured")

        return secret

    @staticmethod
    def create_access_token(user_id):
        now = datetime.now(timezone.utc)

        payload = {
            "sub" : str(user_id),
            "type" : "access",
            "iat" : now,
            "exp" : now + timedelta(minutes=15),
            "jti" : str(uuid.uuid4())
        }
        return jwt.encode(payload,TokenService._secret(),algorithm="HS256")

    @staticmethod
    def create_refresh_token(user_id):
        now = datetime.now(timezone.utc)

        payload = {
            "sub" : str(user_id),
            "type" : "refresh",
            "iat" : now,    
            "exp" : now + timedelta(days=30),
            "jti" : str(uuid.uuid4())
        }
        return jwt.encode(payload,TokenService._secret(),algorithm="HS256")

    @staticmethod
    def verify_access_token(token):
        try:
            payload = jwt.decode(token,TokenService._secret(),algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

        if payload.get("type") != "access":
            return None

        return payload
    
    @staticmethod
    def verify_refresh_token(token):
        try:
            payload = jwt.decode(
                token,
                TokenService._secret(),
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

        if payload.get("type") != "refresh":
            return None

        return payload

    @staticmethod
    def create_2fa_challenge_token(user_id):
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "type": "2fa_challenge",
            "iat": now,
            "exp": now + timedelta(minutes=5),
            "jti": str(uuid.uuid4())
        }

        return jwt.encode(payload,TokenService._secret(),algorithm="HS256")

    @staticmethod
    def verify_2fa_challenge_token(token):
        try:
            payload = jwt.decode(token,TokenService._secret(),algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

        if payload.get("type") != "2fa_challenge":
            return None

        return payload

    @staticmethod
    def create_password_reset_token(user_id):
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "type": "passwod_reset_token",
            "iat": now,
            "exp": now + timedelta(minutes=5),
            "jti": str(uuid.uuid4())
        }
        return jwt.encode(payload,TokenService._secret(),algorithm="HS256")

    @staticmethod
    def verify_password_reset_token(token):
        try:
            payload = jwt.decode(token,TokenService._secret(),algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

        if payload.get("type") != "passwod_reset_token":
            return None

        return payload