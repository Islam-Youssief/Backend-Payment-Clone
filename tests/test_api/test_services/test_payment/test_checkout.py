import unittest
import os 
from assertpy import assert_that

import api.services.requests_service as requests_service
import api.services.payment.checkout as checkout

import tests.doubles.requests as requests_doubles
import api.core.exceptions as exception

import api.core.configurations as configuration


class TestCheckoutClient(unittest.TestCase):
    def setUp(self):
        self.request_sender = requests_doubles.RequestSenderDouble(json={'message': 'success'})
        self.validator_double = UserDataValidatorDouble()
        self.client = checkout.CheckoutClient('lcl' , self.validator_double ,self.request_sender)

    def _get_dummy_card():
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
        assert_that(client_without_doubles._request_sender).is_instance_of(requests_service.WiremockRequester)

    
    def test_pay_with_card_calls_requests_with_expected_params(self):
        response = self.client.pay_with_card(data=self._get_dummy_card)
        assert_that(response.json().get('message')).is_equal_to('success')
        self.request_sender.assert_that_request_is_called_with(
            method='POST',
            url=checkout.CHECKOUT_PAYMENT_URL,
            data=self._get_dummy_card,
            headers={
                'Authorization': f"Bearer {configuration.PaymentConfig.checkout_secret_key}",
                'Content-Type': 'application/json'
            }
        )
class TestUserDataValidator(unittest.TestCase):

    def setUp(self):
        self.validator = checkout.UserDataValidator()

    def test_invalid_amount_type_raise_error(self):
        with self.assertRaises(exception.InputDataTypeError):
            self.validator.validate_amount("ABC123")

    def test_invalid_amount_value_raise_error(self):
        with self.assertRaises(exception.InvalidInputError):
            self.validator.validate_amount(0)

    def test_invalid_card_number_length_raise_error(self):
        with self.assertRaises(exception.InvalidInputError):
            self.validator.validate_card_number("123")

    def test_invalid_card_number_type_raise_error(self):
        with self.assertRaises(exception.InputDataTypeError):
            self.validator.validate_card_number("a")

    def test_validate_card_cvv_length_raise_error(self):
        with self.assertRaises(exception.InvalidInputError):
            self.validator.validate_card_cvv("1")

    def test_validate_card_cvv_type_raise_error(self):
        with self.assertRaises(exception.InputDataTypeError):
            self.validator.validate_card_cvv("a")

class UserDataValidatorDouble:
    def __init__(self):
        self._validation_called = False

    def validate_payment_data(self , data):
        self._validation_called = True

    def assert_that_validate_payment_data_is_called(self):
        assert_that(self._validation_called).is_true()


if __name__ == '__main__':
    unittest.main()