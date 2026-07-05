import hashlib
import os
import unittest
from unittest.mock import patch

from assertpy import assert_that

import api.core.exceptions as exceptions
import api.services.payment.mezza as mezza
import api.services.payment.mezza_validator as mezza_validator
import api.services.requests_service as requests_service
import tests.doubles.requests as requests_doubles


SAMPLE_REQUEST = {
    "amount": 100,
    "currency": "EGP",
    "country": "EG",
    "payment_method_id": "EW",
    "payment_method_flow": "REDIRECT",
    "payer": {"name": "Manoura"},
    "order_id": "ORDER_123",
    "description": "Tshirt",
    "notification_url": "http://localhost/webhook",
    "callback_url": "http://localhost/callback",
}


class TestMezzaClient(unittest.TestCase):

    def setUp(self):
        self.request_sender = requests_doubles.RequestSenderDouble(json={'message': 'success'})
        self.headers_builder = HeadersBuilderDouble()
        self.validator = ValidatorDouble()
        self.client = mezza.MezzaClient('lcl', self.request_sender, self.validator, self.headers_builder)

    def test_client_uses_real_if_doubles_are_not_sent(self):
        client_without_doubles = mezza.MezzaClient('prd')
        assert_that(client_without_doubles._request_sender).is_instance_of(requests_service.RequestsWrapper)
        assert_that(client_without_doubles._validator).is_instance_of(mezza_validator.MeezaPaymentDataValidator)
        assert_that(client_without_doubles._headers_builder).is_instance_of(mezza._MeezaAuthBuilder)

    def test_create_payment_calls_requests_with_expected_params(self):
        response = self.client.create_payment(SAMPLE_REQUEST)
        assert_that(response.json().get('message')).is_equal_to('success')
        self.request_sender.assert_that_request_is_called_with(
            method='POST',
            url=mezza.MEZZA_PAYMENT_URL,
            json=SAMPLE_REQUEST,
            headers={'Authorization': 'fake_headers'}
        )
        self.validator.assert_that_validation_is_called_with(data=SAMPLE_REQUEST)
        self.headers_builder.assert_that_build_headers_is_called_with(data=SAMPLE_REQUEST)


class TestMeezaPaymentDataValidator(unittest.TestCase):

    def setUp(self):
        self.validator = mezza_validator.MeezaPaymentDataValidator()
        self.valid_data = SAMPLE_REQUEST.copy()

    def test_validate_valid_data(self):
        result = self.validator.validate(self.valid_data)
        assert_that(result).is_none()

    def test_raises_required_input_error_when_fields_are_missing(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop('amount')

        with self.assertRaises(exceptions.RequiredInputError) as exc:
            self.validator.validate(invalid_data)

        assert_that(exc.exception.message).contains('Missing fields')

    def test_raises_validation_error_when_amount_is_zero(self):
        invalid_data = {**self.valid_data, 'amount': 0}

        with self.assertRaises(exceptions.ValidationError) as exc:
            self.validator.validate(invalid_data)

        assert_that(exc.exception.message).contains('greater than zero')

    def test_raises_input_data_type_error_when_amount_is_string(self):
        invalid_data = {**self.valid_data, 'amount': 'ABC100'}

        with self.assertRaises(exceptions.InputDataTypeError) as exc:
            self.validator.validate(invalid_data)

        assert_that(exc.exception.message).contains('Invalid amount type')

    def test_raises_validation_error_when_payment_method_is_invalid(self):
        invalid_data = {**self.valid_data, 'payment_method_id': 'CC'}

        with self.assertRaises(exceptions.ValidationError) as exc:
            self.validator.validate(invalid_data)

        assert_that(exc.exception.message).contains('payment_method_id must be EW')


class TestMeezaAuthBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = mezza._MeezaAuthBuilder()

    def test_build_headers_includes_expected_auth_fields(self):
        with patch.dict(os.environ, {'MEZZA_LOGIN': 'fake_login', 'MEZZA_TRANS_KEY': 'fake_trans_key'}, clear=False):
            headers = self.builder.build_headers({'amount': 100})

        assert_that(headers['X-Login']).is_equal_to('fake_login')
        assert_that(headers['X-Trans-Key']).is_equal_to('fake_trans_key')
        assert_that(headers['Content-Type']).is_equal_to('application/json')
        assert_that(headers['X-Date']).is_not_empty()
        expected_signature = hashlib.sha256(
            'fake_loginfake_trans_key100'.encode('utf-8')
        ).hexdigest()
        assert_that(headers['Authorization']).is_equal_to(expected_signature)


class HeadersBuilderDouble:
    def __init__(self):
        self._build_headers_called_with = None

    def build_headers(self, data=None):
        self._build_headers_called_with = data
        return {'Authorization': 'fake_headers'}

    def assert_that_build_headers_is_called_with(self, data):
        assert_that(self._build_headers_called_with).is_equal_to(data)


class ValidatorDouble:
    def __init__(self):
        self._validate_called_with = None

    def validate(self, data):
        self._validate_called_with = data
        return True

    def assert_that_validation_is_called_with(self, data):
        assert_that(self._validate_called_with).is_equal_to(data)


if __name__ == '__main__':
    unittest.main()