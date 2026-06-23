import os


class Config:
    
    @property
    def env(self):
        return os.environ.get('ENV', 'lcl')

class PaymentsConfig:
    @property
    def stripe_secret_key(self):
        return os.environ.get('STRIPE_SECRET_KEY')

