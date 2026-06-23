import os

import api.services.requests_service as requests_service


CHECKOUT_PAYMENT_BASE_URL='https://sl73izp6.api.sandbox.checkout.com'
CHECKOUT_PAYMENT_URL=CHECKOUT_PAYMENT_BASE_URL + '/payments'


class CheckoutClient:
    def __init__(self , env , test_request_sender=None):
        self._env = env 
        self._request_sender = test_request_sender or requests_service.get_service(env)
    
    def pay_with_card(self, data):
        response = self._request_sender.request(method='POST', url=CHECKOUT_PAYMENT_URL, data=data, headers=self._headers)
        return response

    @property
    def _headers(self):
        return{
            'Content-Type':'application/json',
            'Authorization': f"Bearer {os.environ.get('CHECKOUT_SECRET_KEY')}"
        }


