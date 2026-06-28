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
    def stripe_secret_key(self):
        return os.environ.get('STRIPE_SECRET_KEY')
