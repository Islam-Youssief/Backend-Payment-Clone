import random

from api.services.redis import RedisService


class PasswordResetService:

    OTP_EXPIRATION = 300

    @staticmethod
    def generate_otp():
        return f"{random.randint(0, 999999):06d}"

    @staticmethod
    def _key(email):
        return f"password_reset:{email.lower()}"

    @staticmethod
    def store_otp(email, otp):
        RedisService.set(PasswordResetService._key(email),otp,PasswordResetService.OTP_EXPIRATION)

    @staticmethod
    def verify_otp(email, otp):
        key = PasswordResetService._key(email)

        stored_otp = RedisService.get(key)

        if stored_otp is None:
            return False

        if stored_otp != otp:
            return False

        RedisService.delete(key)

        return True