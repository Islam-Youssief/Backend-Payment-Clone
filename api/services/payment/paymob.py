import api.core.configurations as configurations
import api.services.requests_service as requests_service


PAYMOB_INTENTION_URL = 'accept.paymob.com/v1/intention/'


class PaymobClient:
    def __init__(self, env, test_request_sender=None):
        self._env = env
        self._request_sender = test_request_sender or requests_service.get_service(self._env)


    @property
    def _headers(self):
        return {
            'Authorization': f'Token {configurations.PaymentsConfig().paymob_secret_key}',
            'Content-Type': 'application/json',
        }


    def create_intention(self, amount, currency, payment_methods, items, billing_data):
        response = self._request_sender.request(
            method='POST',
            url=PAYMOB_INTENTION_URL,
            json={
                'amount': amount,
                'currency': currency,
                'payment_methods': payment_methods,
                'items': items,
                'billing_data': billing_data,
            },
            headers=self._headers
        )
        return response
