import os

import api.services.requests_service as requests_service
from api.core import configurations


STRIPE_PAYMENT_INTENTS_URL = "https://api.stripe.com/v1/payments_intents"

class StripeClient:
    def __init__(self,env,test_request_sender=None,test_headers=None):
        self._env = env
        self._request_sender = test_request_sender or requests_service.get_service(self._env)
        self.headers = {
            "Authorization": f"Bearer {configurations.PaymentsConfig().stripe_secret_key}"
        }
    def create_payment_intent(self,data):
        response = self._request_sender.request(
             method="POST",
             url=STRIPE_PAYMENT_INTENTS_URL,
             data=data,
             headers=self.headers,
        )
        return response

