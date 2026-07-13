import http
import unittest

from assertpy import assert_that

import api.controllers.payments.paypal as paypal
import api.core.exceptions as exceptions


class TestPayPalController(unittest.TestCase):
    def setUp(self):
        self.json = {'cardNumber': '1234567890'}
        self.path = '/api/payments/paypal'
        self.config = {'env': 'lcl'} 
        self.validator = ValidatorDouble()
        self.handler = HandlerDouble()
        self.controller = paypal.PayPalController(self, self.config, self.validator, self.handler)

    def test_pay_calls_right_components(self):
        response, status_code = self.controller.pay()
        assert_that(response.get('url')).is_equal_to('/api/payments/paypal')
        assert_that(status_code).is_equal_to(http.HTTPStatus.CREATED)
        self.validator.assert_that_validate_is_called_with(self.json)
        self.handler.assert_that_process_payment_is_called_with(self.json)
    
    def test_controller_has_right_properties_if_no_doubles_sent(self):
        self.env = 'lcl'
        controller = paypal.PayPalController(self, self)
        assert_that(controller._body).is_equal_to(self.json)
        assert_that(controller._validator).is_instance_of(paypal.validators.UserPaymentDataValidator)
        assert_that(controller._handler).is_instance_of(paypal._PayPalHandler)
    
    def test_controller_catch_required_input_error(self):
        self.validator.raise_exception = exceptions.RequiredInputError('cardNumber')
        response, status_code = self.controller.pay()
        assert_that(response.get('message')).is_equal_to('Input <cardNumber> is required')
        assert_that(status_code).is_equal_to(http.HTTPStatus.BAD_REQUEST)


class ValidatorDouble:
    def __init__(self, raise_exception=False):
        self.data = None
        self.raise_exception = raise_exception
    
    def validate(self, data):
        self.data = data
        if self.raise_exception: 
            raise self.raise_exception
    
    def assert_that_validate_is_called_with(self, data):
        assert_that(data).is_equal_to(self.data)    


class HandlerDouble:

    def __init__(self):
        self.data = None
        self.message = 'Payment successful'
        self.status = 'COMPLETED'
        self.transaction_id = '1234567890'
        self.amount = 100.0
        self.currency = 'USD'
        self.payment_method = 'VISA'
    
    def process_payment(self, data):
        self.data = data
        return self
    
    def assert_that_process_payment_is_called_with(self, data):
        assert_that(data).is_equal_to(self.data)


class TestPayPalHandler(unittest.TestCase):

    def test_returns_expected_response_from_client(self):
        client_double = PayPalClientDouble()
        handler = paypal._PayPalHandler({'api-key': ''}, client_double)
        response = handler.process_payment(data={'amount': 100.0})
        assert_that(response.message).is_equal_to('Payment successful')
        client_double.assert_that_pay_with_visa_sent_with({'amount': 100.0})
        
        
class PayPalClientDouble:
    def __init__(self):
        self.data = None

    def pay_with_visa(self, data):
        self.data = data
        return self

    def json(self):
        return {'message': 'Payment successful'}

    def assert_that_pay_with_visa_sent_with(self, expected_data):
        assert_that(self.data).is_equal_to(expected_data)
        
        
        
class TestPayPalSerializer(unittest.TestCase):

    def test_returns_expected_json(self):
        json_response = paypal._PayPalSerializer(self._get_dummy_invoice()).serialize('/api/payments/paypal')
        assert_that(json_response.get('url')).is_equal_to('/api/payments/paypal')
        assert_that(json_response.get('message')).is_equal_to('Payment successful')
        assert_that(json_response.get('status')).is_equal_to('COMPLETED')
        assert_that(json_response.get('transaction_id')).is_equal_to('1234567890')
        assert_that(json_response.get('amount')).is_equal_to(100.0)
        assert_that(json_response.get('currency')).is_equal_to('USD')
        assert_that(json_response.get('payment_method')).is_equal_to('VISA')

    def _get_dummy_invoice(self):
        self.message = 'Payment successful'
        self.status = 'COMPLETED'
        self.transaction_id = '1234567890'
        self.amount = 100.0
        self.currency = 'USD'
        self.payment_method = 'VISA'
        return self
