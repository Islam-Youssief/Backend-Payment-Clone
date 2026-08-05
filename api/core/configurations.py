import os


class AppConfig:
    
    @property
    def env(self):
        return os.environ.get('ENV', 'lcl')

    @property
    def wiremock_url(self):
        return f'http://127.0.0.1:{self.wiremock_port}'
        
    @property
    def wiremock_port(self):
        return '8080'


class PaymentsConfig:
    @property
    def fawry_merchant_code(self):
        return os.environ.get('FAWRY_MERCHANT_CODE')
    
    @property
    def fawry_security_key(self):
        return os.environ.get('FAWRY_SECURITY_KEY')

    @property
    def stripe_secret_key(self):
        return os.environ.get('STRIPE_SECRET_KEY')
    

    @property
    def checkout_prefix_code(self):
        return os.environ.get('CHECKOUT_PREFIX_CODE') or 'sl73izp6'

    @property
    def checkout_secret_key(self):
        return os.environ.get('CHECKOUT_SECRET_KEY')

    @property
    def paymob_secret_key(self):
        return os.environ.get('PAYMOB_SECRET_KEY')
