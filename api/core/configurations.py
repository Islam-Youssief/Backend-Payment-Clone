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

    @property
    def redis_host(self):
        return os.environ.get('REDIS_HOST', 'localhost')

    @property
    def redis_port(self):
        return int(os.environ.get('REDIS_PORT', 6379))

    @property
    def redis_db(self):
        return int(os.environ.get('REDIS_DB', 0))

    @property
    def celery_broker_url(self):
        return os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')

    @property
    def celery_result_backend(self):
        return os.environ.get('CELERY_RESULT_BACKEND', f'redis://{self.redis_host}:{self.redis_port}/1')



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
