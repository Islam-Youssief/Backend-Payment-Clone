import base64
import unittest

from assertpy import assert_that

import api.services.requests_service as requests_service
import api.services.payment.paypal as paypal

import tests.doubles.requests as requests_doubles


class TestPayPalClient(unittest.TestCase):

    def setUp(self):
        self.request_sender = requests_doubles.RequestSenderDouble(json={'message': 'success'})
        self.authorizer = AuthorizerDouble()
        self.client = paypal.PayPalClient('lcl', self.request_sender, self.authorizer)

    def test_client_uses_real_if_doubles_are_not_sent(self):
        client_without_doubles = paypal.PayPalClient('prd')
        assert_that(client_without_doubles._request_sender).is_instance_of(requests_service.RequestsWrapper)
        assert_that(client_without_doubles._authorizer).is_instance_of(paypal._PayPalAuthorizer)

    def test_pay_with_visa_calls_requests_with_expected_params(self):
        response = self.client.pay_with_visa(data='fake_data')
        assert_that(response.json().get('message')).is_equal_to('success')
        self.request_sender.assert_that_request_is_called_with(
            method='POST',
            url=paypal.PAYPAL_PAYMENT_URL,
            data='fake_data',
            headers={'Authorization': 'Bearer fake_access_token'}
        )
        self.authorizer.assert_that_authorize_is_called()



class AuthorizerDouble:
    def __init__(self):
        self._authorize_called = False

    def authorize(self):
        self._authorize_called = True
        return 'fake_access_token'

    def assert_that_authorize_is_called(self):
        assert_that(self._authorize_called).is_true()


class TestPayPalAuthorizer(unittest.TestCase):
    def setUp(self):
        self.request_sender = requests_doubles.RequestSenderDouble(json={'access_token': 'fake_access_token'})
        self.authorizer = paypal._PayPalAuthorizer('lcl', self.request_sender)

    def test_client_uses_real_if_doubles_are_not_sent(self):
        client_without_doubles = paypal._PayPalAuthorizer('prd')
        assert_that(client_without_doubles._request_sender).is_instance_of(requests_service.RequestsWrapper)

    def test_authorize_calls_requests_with_expected_params(self):  
        response = self.authorizer.authorize()
        assert_that(response).is_equal_to('fake_access_token')
        self.request_sender.assert_that_request_is_called_with(
            method='POST',
            url=paypal.PAYPAL_AUTHORIZATION_URL,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f"Basic {base64.b64encode(self.authorizer._secret).decode('utf-8')}"}
        )



if __name__ == '__main__':
    unittest.main()
