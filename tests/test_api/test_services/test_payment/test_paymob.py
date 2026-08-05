import unittest

from assertpy import assert_that

import api.services.requests_service as requests_service
import api.services.payment.paymob as paymob

import tests.doubles.requests as requests_doubles


class TestPaymobClient(unittest.TestCase):

    def setUp(self):
        self.request_sender = requests_doubles.RequestSenderDouble(json={'client_secret': 'fake_client_secret'})
        self.client = paymob.PaymobClient('lcl', self.request_sender)

    def test_client_uses_real_if_double_is_not_sent(self):
        client_without_double = paymob.PaymobClient('prd')
        assert_that(client_without_double._request_sender).is_instance_of(requests_service.RequestsWrapper)

    def test_create_intention_calls_requests_with_expected_params(self):
        response = self.client.create_intention(
            amount=1000,
            currency='EGP',
            payment_methods=[1, 2],
            items=[{'name': 'item', 'amount': 1000}],
            billing_data={'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com', 'phone_number': '+201234567890'}
        )
        assert_that(response.json().get('client_secret')).is_equal_to('fake_client_secret')
        self.request_sender.assert_that_request_is_called_with(
            method='POST',
            url=paymob.PAYMOB_INTENTION_URL,
            json={
                'amount': 1000,
                'currency': 'EGP',
                'payment_methods': [1, 2],
                'items': [{'name': 'item', 'amount': 1000}],
                'billing_data': {'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com', 'phone_number': '+201234567890'}
            },
            headers=self.client._headers
        )


if __name__ == '__main__':
    unittest.main()
