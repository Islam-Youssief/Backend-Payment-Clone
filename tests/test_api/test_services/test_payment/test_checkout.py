import unittest
import os 
from assertpy import assert_that

import api.services.requests_service as requests_service
import api.services.payment.checkout as checkout

import tests.doubles.requests as requests_doubles


class TestCheckoutClient(unittest.TestCase):
    def setUp(self):
        self.request_sender = requests_doubles.RequestSenderDouble(json={'message': 'success'})
        self.client = checkout.CheckoutClient('lcl' , self.request_sender)

    def test_client_uses_real_if_doubles_are_not_sent(self):
        client_without_doubles = checkout.CheckoutClient('lcl')
        assert_that(client_without_doubles._request_sender).is_instance_of(requests_service.RequestsWrapper)

    
    def test_pay_with_card_calls_requests_with_expected_params(self):
        response = self.client.pay_with_card(data='fake_data')
        assert_that(response.json().get('message')).is_equal_to('success')
        self.request_sender.assert_that_request_is_called_with(
            method='POST',
            url=checkout.CHECKOUT_PAYMENT_URL,
            data='fake_data',
            headers={'Authorization': f"Bearer {os.environ.get('CHECKOUT_SECRET_KEY')}" ,
            'Content-Type':'application/json'
}
        )

if __name__ == '__main__':
    unittest.main()