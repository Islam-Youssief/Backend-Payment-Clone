import base64
import os

import api.services.requests_service as requests_service


STRIPE_PAYMENT_INTENTS_URL = "https://api.stripe.com/v1/payment_intents"
STRIPE_CUSTOMERS_URL = "https://api.stripe.com/v1/customers"

class StripeClient:
    def __init__(self,env,test_request_sender=None,test_authorizer=None):
        self._env = env
        self._request_sender = test_request_sender or requests_service.get_service(self._env)
        self._authorizer = test_authorizer or _StripeAuthorizer(os.environ["STRIPE_SECRET_KEY"])

    def  create_payment_intent(self,data):
        response = self._request_sender.request(
                    method='POST',
                    url=STRIPE_PAYMENT_INTENTS_URL,
                    data=data,
                    headers=self._authorizer.headers # type: ignore
                    )
        return response
class _StripeAuthorizer: 
    def __init__(self,secret_key):
        self.secret_key = secret_key 
        
    
    
    @property 
    def headers(self):
        return{ "Authorization":f"Bearer {self.secret_key}"
        }           
