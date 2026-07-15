import http
import unittest
import requests
import json
from assertpy import assert_that

import api.controllers.payments.fawry as fawry
import api.core.exceptions as exceptions


class TestFawryController(unittest.TestCase):
    def setUp(self):
        self.json = {'cardNumber': '1234567890123456'}
        self.path = '/api/payments/fawry'
        self.headers = {}
        self.config = ConfigDouble()
        self.validator = ValidatorDouble()
        self.handler = HandlerDouble()
        self.controller = fawry.FawryController(self, self.config, self.validator, self.handler)

    def test_pay_calls_right_components(self):
        response, status_code = self.controller.pay()
        assert_that(response.get('url')).is_equal_to('/api/payments/fawry')
        assert_that(status_code).is_equal_to(http.HTTPStatus.CREATED)
        self.validator.assert_that_validate_is_called_with(self.json)
        self.handler.assert_that_process_payment_is_called_with(self.json)
    
    def test_controller_has_right_properties_if_no_doubles_sent(self):
        controller = fawry.FawryController(self, self.config)
        assert_that(controller._body).is_equal_to(self.json)
        assert_that(controller._validator).is_instance_of(fawry.validators.UserPaymentDataValidator)
        assert_that(controller._handler).is_instance_of(fawry._FawryHandler)

    def test_controller_catch_required_input_error(self):
        self.validator.raise_exception = exceptions.RequiredInputError('cardNumber')
        response, status_code = self.controller.pay()
        assert_that(response.get('message')).is_equal_to('Input <cardNumber> is required')
        assert_that(status_code).is_equal_to(http.HTTPStatus.BAD_REQUEST)

    def test_controller_catch_invalid_input_error(self):
        self.validator.raise_exception = exceptions.InvalidInputError('cardNumber', '12345')
        response, status_code = self.controller.pay()
        assert_that(response.get('message')).is_equal_to('Invalid value <12345> for <cardNumber>')
        assert_that(status_code).is_equal_to(http.HTTPStatus.BAD_REQUEST)

    def test_controller_catch_unauthorized_access_error(self):
        self.validator.raise_exception = exceptions.UnauthorizedAccessError('Unauthorized access.')
        response, status_code = self.controller.pay()
        assert_that(response.get('message')).is_equal_to('Unauthorized access.')
        assert_that(status_code).is_equal_to(http.HTTPStatus.UNAUTHORIZED)

    def test_controller_catch_external_service_unavailable_error(self):
        self.handler.raise_exception = exceptions.ExternalServiceUnavailableError()
        response, status_code = self.controller.pay()
        assert_that(response.get('message')).is_equal_to('External service unavailable')
        assert_that(status_code).is_equal_to(http.HTTPStatus.BAD_GATEWAY)


    def test_controller_catch_external_service_error(self):
        self.handler.raise_exception = exceptions.ExternalServiceError()
        response, status_code = self.controller.pay()
        assert_that(response.get('message')).is_equal_to('External service error')
        assert_that(status_code).is_equal_to(http.HTTPStatus.BAD_GATEWAY)

    def test_controller_catch_insufficient_balance_error(self):
        self.handler.raise_exception = exceptions.InsufficientBalanceError()
        response, status_code = self.controller.pay()
        assert_that(response.get('message')).is_equal_to('Insufficient Balance')
        assert_that(status_code).is_equal_to(http.HTTPStatus.PAYMENT_REQUIRED)

    def test_controller_catch_timeout_error(self):
        self.handler.raise_exception = requests.exceptions.Timeout("Timeout")
        response, status_code = self.controller.pay()
        assert_that(response.get('message')).is_equal_to('External service timeout')
        assert_that(status_code).is_equal_to(http.HTTPStatus.GATEWAY_TIMEOUT)

class ConfigDouble:
    def __init__(self):
        self.env = 'lcl'


class ValidatorDouble:
    def __init__(self, raise_exception=None):
        self.data = None
        self.token = None
        self.raise_exception = raise_exception
    
    def validate(self, data, token=None):
        self.data = data
        self.token = token
        if self.raise_exception: 
            raise self.raise_exception
    
    def assert_that_validate_is_called_with(self, data):
        assert_that(data).is_equal_to(self.data)    


class HandlerDouble:
    def __init__(self, raise_exception=None):
        self.data = None
        self.raise_exception = raise_exception
        self.reference_number = '1234567890'
        self.merchant_ref_number = 'ORDER_123'
        self.order_amount = 100.5
        self.payment_amount = 100.5
        self.fawry_fees = 1.0
        self.payment_method = 'CARD'
        self.order_status = 'PAID'
        self.payment_time = '2026-07-14 18:00:00'
        self.customer_mobile = '0123456789'
        self.customer_mail = 'tester@test.com'
        self.customer_profile_id = 'CUST_123'
        self.signature = 'fake_signature'
        self.status_code = '200'
        self.status_description = 'Operation done successfully'
    
    def process_payment(self, data):
        self.data = data
        if self.raise_exception:
            raise self.raise_exception
        return self
    
    def assert_that_process_payment_is_called_with(self, data):
        assert_that(data).is_equal_to(self.data)


class TestFawryHandler(unittest.TestCase):
    def test_returns_expected_response_from_client(self):
        client_double = FawryClientDouble()
        handler = fawry._FawryHandler(ConfigDouble(), client_double)
        response = handler.process_payment(data={'amount': 100.5})
        assert_that(response.reference_number).is_equal_to('1234567890')
        client_double.assert_that_pay_with_card_sent_with({'amount': 100.5})


class FawryClientDouble:
    def __init__(self):
        self.data = None
        self.status_code = http.HTTPStatus.OK

    def pay_with_card(self, data):
        self.data = data
        return self

    def json(self):
        return {
            'reference_number': '1234567890',
            'merchant_ref_number': 'ORDER_123',
            'order_amount': 100.5,
            'payment_amount': 100.5,
            'fawry_fees': 1.0,
            'payment_method': 'CARD',
            'order_status': 'PAID',
            'payment_time': '2026-07-14 18:00:00',
            'customer_mobile': '0123456789',
            'customer_mail': 'tester@test.com',
            'customer_profile_id': 'CUST_123',
            'signature': 'fake_signature',
            'status_code': '200',
            'status_description': 'Operation done successfully'
        }

    def assert_that_pay_with_card_sent_with(self, expected_data):
        assert_that(self.data).is_equal_to(expected_data)


class TestFawrySerializer(unittest.TestCase):
    def test_returns_expected_json(self):
        invoice = self._get_dummy_invoice()
        json_response = fawry._FawrySerializer().serialize(invoice, '/api/payments/fawry')
        assert_that(json_response.get('url')).is_equal_to('/api/payments/fawry')
        assert_that(json_response.get('reference_number')).is_equal_to('1234567890')
        assert_that(json_response.get('merchant_ref_number')).is_equal_to('ORDER_123')
        assert_that(json_response.get('order_amount')).is_equal_to(100.5)
        assert_that(json_response.get('payment_amount')).is_equal_to(100.5)
        assert_that(json_response.get('fawry_fees')).is_equal_to(1.0)
        assert_that(json_response.get('payment_method')).is_equal_to('CARD')
        assert_that(json_response.get('order_status')).is_equal_to('PAID')
        assert_that(json_response.get('payment_time')).is_equal_to('2026-07-14 18:00:00')
        assert_that(json_response.get('customer_mobile')).is_equal_to('0123456789')
        assert_that(json_response.get('customer_mail')).is_equal_to('tester@test.com')
        assert_that(json_response.get('customer_profile_id')).is_equal_to('CUST_123')
        assert_that(json_response.get('signature')).is_equal_to('fake_signature')
        assert_that(json_response.get('status_code')).is_equal_to('200')
        assert_that(json_response.get('status_description')).is_equal_to('Operation done successfully')

    def _get_dummy_invoice(self):
        invoice = HandlerDouble()
        return invoice


if __name__ == '__main__':
    unittest.main()
