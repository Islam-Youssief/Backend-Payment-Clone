from api.core import configurations
import hashlib
import unittest
from assertpy import assert_that

import api.services.payment.fawry as fawry
import api.core.exceptions as exceptions
import tests.doubles.requests as requests_doubles
import api.services.requests_service as requests_service

class TestFawryClient(unittest.TestCase):
    def setUp(self):
        self.request_sender = requests_doubles.RequestSenderDouble(json={'message': 'success'})
        self.signature_builder = _FawrySignatureBuilderDouble()
        self.client = fawry.FawryClient('lcl', self.request_sender, self.signature_builder)

    def test_client_uses_real_if_doubles_are_not_sent(self):
        client_without_doubles = fawry.FawryClient('lcl')
        assert_that(client_without_doubles._request_sender).is_instance_of(requests_service.RequestsWrapper)
        assert_that(client_without_doubles._signature_builder).is_instance_of(fawry._FawrySignatureBuilder)

    def test_pay_with_visa_calls_requests_with_expected_params(self):
        fake_data = {
            'amount': 100,
            'merchantRefNum': '123456',
            'customerProfileId': 'customer123',
            'paymentMethod': 'CARD',
            'cardNumber': '1234567890123456',
            'cardExpiryYear': '25',
            'cardExpiryMonth': '12',
            'cvv': '123'
        }
        response = self.client.pay_with_visa(data=fake_data)
        assert_that(response.json().get('message')).is_equal_to('success')
        self.request_sender.assert_that_request_is_called_with(
            method='POST',
            url=fawry.FAWRY_PAYMENT_URL,
            json={**fake_data, 'signature': 'fake_signature'},
            headers={'Content-Type': 'application/json'}
        )
        self.signature_builder.assert_that_build_signature_is_called_with(data=fake_data)


class TestFawryClientValidation(unittest.TestCase):
    def setUp(self):
        self.request_sender = requests_doubles.RequestSenderDouble(json={'message': 'success'})
        self.signature_builder = _FawrySignatureBuilderDouble()
        self.client = fawry.FawryClient('lcl', self.request_sender, self.signature_builder)
        self.valid_data = {
            'amount': 100,
            'merchantRefNum': '123456',
            'cardNumber': '1234567890123456',
            'cardExpiryYear': '25',
            'cardExpiryMonth': '12',
            'cvv': '123'
        }

    def test_raises_required_input_error_when_fields_are_missing(self):
        with self.assertRaises(exceptions.RequiredInputError):
            self.client.pay_with_visa(data={'amount': 100})

    def test_raises_validation_error_when_amount_is_zero(self):
        invalid_data = {**self.valid_data, 'amount': 0}
        with self.assertRaises(exceptions.ValidationError):
            self.client.pay_with_visa(data=invalid_data)

    def test_raises_validation_error_when_amount_is_negative(self):
        invalid_data = {**self.valid_data, 'amount': -50}
        with self.assertRaises(exceptions.ValidationError):
            self.client.pay_with_visa(data=invalid_data)
    
    def test_raises_input_data_type_error_when_amount_is_string(self):
        invalid_data = {**self.valid_data, 'amount': 'ABC100'}
        with self.assertRaises(exceptions.InputDataTypeError):
            self.client.pay_with_visa(data=invalid_data)

    def test_raises_validation_error_when_card_number_is_not_16_digits(self):
        invalid_data = {**self.valid_data, 'cardNumber': '12345'}
        with self.assertRaises(exceptions.ValidationError):
            self.client.pay_with_visa(data=invalid_data)

    def test_raises_validation_error_when_card_number_contains_letters(self):
        invalid_data = {**self.valid_data, 'cardNumber': 'ABC1234567890123'}
        with self.assertRaises(exceptions.ValidationError):
            self.client.pay_with_visa(data=invalid_data)

    def test_raises_validation_error_when_expiry_month_is_invalid(self):
        invalid_data = {**self.valid_data, 'cardExpiryMonth': '13'}
        with self.assertRaises(exceptions.ValidationError):
            self.client.pay_with_visa(data=invalid_data)

    def test_raises_validation_error_when_expiry_year_is_too_short(self):
        invalid_data = {**self.valid_data, 'cardExpiryYear': '5'}
        with self.assertRaises(exceptions.ValidationError):
            self.client.pay_with_visa(data=invalid_data)

    def test_raises_validation_error_when_cvv_is_not_3_digits(self):
        invalid_data = {**self.valid_data, 'cvv': '12'}
        with self.assertRaises(exceptions.ValidationError):
            self.client.pay_with_visa(data=invalid_data)

    def test_raises_validation_error_when_cvv_contains_letters(self):
        invalid_data = {**self.valid_data, 'cvv': 'ABC'}
        with self.assertRaises(exceptions.ValidationError):
            self.client.pay_with_visa(data=invalid_data)


class TestFawrySignatureBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = fawry._FawrySignatureBuilder()


    def test_build_signature_generates_correct_signature(self):
        data = {
            'merchantCode': 'test_merchant',
            'merchantRefNum': '123456',
            'customerProfileId': 'customer123',
            'amount': '100.50',
            'cardNumber': '1234567890123456',
            'cardExpiryYear': '25',
            'cardExpiryMonth': '12',
            'cvv': '123',
            'paymentMethod': 'CARD'
        }
        expected_string = str(configurations.PaymentsConfig.fawry_merchant_code) + data['merchantRefNum'] + data['customerProfileId'] + data['paymentMethod'] + data['amount'] + data['cardNumber'] + data['cardExpiryYear'] + data['cardExpiryMonth'] + data['cvv'] + str(configurations.PaymentsConfig.fawry_security_key)
        expected_signature = hashlib.sha256(expected_string.encode('utf-8')).hexdigest()
        assert_that(self.builder.build_signature(data)).is_equal_to(expected_signature)


class _FawrySignatureBuilderDouble:
    def __init__(self):
        self._build_signature_called_with = None

    def build_signature(self, data):
        self._build_signature_called_with = data
        return "fake_signature"
        
    def assert_that_build_signature_is_called_with(self,data):
        assert_that(self._build_signature_called_with).is_equal_to(data)