from cryptography.fernet import Fernet
import api.core.configurations as config

class EncryptionService:

    @staticmethod
    def _get_cipher():
        key = config.TotpConfig.totp_encryption_key
        if not key :
            raise RuntimeError("TOTP_ENCRYPTION_KEY is not configured")
        return Fernet(key)

    @staticmethod
    def encrypt(value):
        cipher = EncryptionService._get_cipher()
        return cipher.encrypt(value.encode("utf-8")).decode("utf-8")
    
    @staticmethod
    def decrypt(value):
        cipher = EncryptionService._get_cipher()
        return cipher.decrypt(value.encode("utf-8")).decode("utf-8")  