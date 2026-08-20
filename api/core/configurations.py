import os
from dotenv import load_dotenv

load_dotenv()

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
    def paymob_secret_key(self):
        return os.environ.get('PAYMOB_SECRET_KEY')
    
    @property
    def checkout_prefix_code(self):
        return os.environ.get('CHECKOUT_PREFIX_CODE') or 'sl73izp6'

    @property
    def checkout_secret_key(self):
        return os.environ.get('CHECKOUT_SECRET_KEY')
    
    @property
    def paymob_hmac_secret(self):
        return os.environ.get('PAYMOB_HMAC_SECRET')   

class RedisConfig:
    @property
    def url(self):
        return os.environ.get('REDIS_URL', 'redis://localhost:6379/2')

    @property
    def port(self):
        return int(os.environ.get('REDIS_PORT', 6379))

class CeleryConfig:
    @property
    def broker_url(self):
        return os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/2')

    @property
    def result_backend(self):
        return os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')

    @property
    def task_serializer(self):
        return os.environ.get('CELERY_TASK_SERIALIZER', 'json')

    @property
    def task_time_limit(self):
        return int(os.environ.get('CELERY_TASK_TIME_LIMIT', 600))

    @property
    def task_acks_late(self):
        return os.environ.get('CELERY_TASK_ACKS_LATE', 'True')

    @property
    def worker_concurrency(self):
        return int(os.environ.get('CELERY_WORKER_CONCURRENCY', 2))

class TotpConfig:
    totp_encryption_key = os.environ.get('TOTP_ENCRYPTION_KEY')
    jwt_secret_key = os.environ.get('JWT_SECRET_KEY')