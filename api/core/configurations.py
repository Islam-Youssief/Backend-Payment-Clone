import os


class Config:
    
    @property
    def env(self):
        return os.environ.get('ENV', 'lcl')
    
class PaymentsConfig:
    @property
    def fawry_merchant_code(self):
        return os.environ.get('FAWRY_MERCHANT_CODE')
    
    @property
    def fawry_security_key(self):
        return os.environ.get('FAWRY_SECURITY_KEY')