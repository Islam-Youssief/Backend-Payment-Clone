import unittest
import os 
from assertpy import assert_that

import api.services.requests_service as requests_service
import api.services.payment.checkout as checkout

import tests.doubles.requests as requests_doubles
import api.core.exceptions as exception


class TestCheckoutClient(unittest.TestCase):
    def setUp(self):
        self.request_sender = requests_doubles.RequestSenderDouble(json={'message': 'success'})
        self.client = checkout.CheckoutClient('lcl' , self.request_sender)

    def card_fake_data(self):
        return{
            "source":{
            "type": "card",
            "number": "2242424242424242",
            "cvv": "100",
            "expiry_month": 12,
            "expiry_year": 2030
        },
        "currency": "USD",
        "amount": 1000,
        "processing_channel_id": "pc_test_123"
        }

    def test_client_uses_real_if_doubles_are_not_sent(self):
        client_without_doubles = checkout.CheckoutClient('lcl')
        assert_that(client_without_doubles._request_sender).is_instance_of(requests_service.RequestsWrapper)

    
    def test_pay_with_card_calls_requests_with_expected_params(self):
        response = self.client.pay_with_card(data=self.card_fake_data())
        assert_that(response.json().get('message')).is_equal_to('success')
        self.request_sender.assert_that_request_is_called_with(
            method='POST',
            url=checkout.CHECKOUT_PAYMENT_URL,
            data=self.card_fake_data(),
            headers={'Authorization': f"Bearer {os.environ.get('CHECKOUT_SECRET_KEY')}" ,
            'Content-Type':'application/json'
}
        )

    def test_invalid_amount_type_raise_error(self):
        with self.assertRaises(exception.InputDataTypeError):
            self.client.validate_amount("ABC123")

    def test_invalid_amount_value_raise_error(self):
        with self.assertRaises(exception.ValidationError):
            self.client.validate_amount(0)


    def test_invalid_card_number_length_raise_error(self):
        with self.assertRaises(exception.ValidationError):
            self.client.validate_card_number("123")

    def test_invalid_card_number_type_raise_error(self):
        with self.assertRaises(exception.ValidationError):
            self.client.validate_card_number("a")

    def test_validate_card_cvv_length_raise_error(self):
        with self.assertRaises(exception.ValidationError):
            self.client.validate_card_cvv("1")

    def test_validate_card_cvv_type_raise_error(self):
        with self.assertRaises(exception.ValidationError):
            self.client.validate_card_cvv("a")
    
    if __name__ == '__main__':
        unittest.main()