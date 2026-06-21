import base64
import os

import api.services.requests_service as requests_service


PAYPAL_AUTHORIZATION_URL = 'api-m.paypal.com/v1/oauth2/token'
PAYPAL_PAYMENT_URL = 'api-m.paypal.com/v2/checkout/orders'


class PayPalClient:
    def __init__(self, env, test_request_sender=None, test_authorizer=None):
        self._env = env
        self._request_sender = test_request_sender or requests_service.get_service(self._env)
        self._authorizer = test_authorizer or _PayPalAuthorizer(self._env)


    def pay_with_visa(self, data):
        access_token = self._authorizer.authorize()        
        response = self._request_sender.request(method='POST', url=PAYPAL_PAYMENT_URL, data=data, headers={
            'Authorization': f'Bearer {access_token}'
        })
        return response


class _PayPalAuthorizer:
    def __init__(self, env, test_request_sender=None):
        self._env = env
        self._request_sender = test_request_sender or requests_service.get_service(self._env)


    @property
    def _headers(self):
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {base64.b64encode(self._secret).decode('utf-8')}'
        }

    @property
    def _secret(self):
        return f'{os.environ.get('PAYPAL_CLIENT_ID')}:{os.environ.get('PAYPAL_CLIENT_SECRET')}'.encode()


    def authorize(self):
        response = self._request_sender.request(method='POST', url=PAYPAL_AUTHORIZATION_URL, headers=self._headers)
        return response.json().get('access_token')
