import os


class AppConfig:
    
    @property
    def env(self):
        return os.environ.get('ENV', 'lcl')
<<<<<<< HEAD

    @property
    def wiremock_url(self):
        return f'http://127.0.0.1:{self.wiremock_port}'

    @property
    def wiremock_port(self):
        return '8080'

class PaymentsConfig:
    @property
    def stripe_secret_key(self):
        return os.environ.get('STRIPE_SECRET_KEY')
=======
    
class PaymentConfig:

    @property
    def checkout_prefix_code(self):
        return os.environ.get('CHECKOUT_PREFIX_CODE')

    @property
    def checkout_secret_key(self):
        return os.environ.get('CHECKOUT_SECRET_KEY')
>>>>>>> 7a31ed1 (feat: add payment config)
