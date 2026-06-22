import os


class Config:
    
    @property
    def env(self):
        return os.environ.get('ENV', 'lcl')
    
class PaymentsConfig:
    fawry_merchant_code = os.environ.get('FAWRY_MERCHANT_CODE')
    fawry_security_key = os.environ.get('FAWRY_SECURITY_KEY')