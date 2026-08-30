import pyotp
from api.services.authentication.encryption import EncryptionService
from api.models import db

class TotpService:
    @staticmethod
    def generate_secret():
        return pyotp.random_base32()

    @staticmethod
    def  setup(user):
        secret = TotpService.generate_secret()
        user.totp_secret = EncryptionService.encrypt(secret)
        user.totp_enabled = False
        try:
            db.session.commit()
        except Exception:
             db.session.rollback()
        return pyotp.TOTP(secret).provisioning_uri(name=user.email,issuer_name="Backend Payment Clone")
    
    @staticmethod
    def confirm(user,code):
        if not user.totp_secret:
            return False
        
        secret = EncryptionService.decrypt(user.totp_secret)
        totp = pyotp.TOTP(secret)

        if not totp.verify(code):
            return False
        
        user.totp_enabled = True
        try:
           db.session.commit()
        except Exception:
          db.session.rollback()
        return True
    
    @staticmethod
    def verify(user, code):
        if not user.totp_secret:
            return False

        secret = EncryptionService.decrypt(user.totp_secret)

        return pyotp.TOTP(secret).verify(code)