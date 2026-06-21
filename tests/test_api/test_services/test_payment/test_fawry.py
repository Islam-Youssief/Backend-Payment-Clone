import hashlib
import unittest
import os
from assertpy import assert_that

import api.services.payment.fawry as fawry
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
        fake_data = {'amount': 100}
        os.environ['FAWRY_MERCHANT_CODE'] = 'test_merchant'
        response = self.client.pay_with_visa(data=fake_data)
        del os.environ['FAWRY_MERCHANT_CODE']
        assert_that(response.json().get('message')).is_equal_to('success')
        self.request_sender.assert_that_request_is_called_with(
            method='POST',
            url=fawry.FAWRY_PAYMENT_URL,
            json={'amount': 100, 'merchantCode': 'test_merchant', 'signature': 'fake_signature'},
            headers={'Content-Type': 'application/json'}
        )
        self.signature_builder.assert_that_build_signature_is_called()


class TestFawrySignatureBuilder(unittest.TestCase):
    def setUp(self):
        os.environ['FAWRY_SECURITY_KEY'] = 'test_secure_key'
        self.builder = fawry._FawrySignatureBuilder()

    def tearDown(self):
        del os.environ['FAWRY_SECURITY_KEY']

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
        
        # The expected string to hash based on the Fawry logic:
        # merchantCode + merchantRefNum + customerProfileId + paymentMethod + amount + cardNumber + cardExpiryYear + cardExpiryMonth + cvv + secureKey
        expected_string = "test_merchant123456customer123CARD100.5012345678901234562512123test_secure_key"
        expected_signature = hashlib.sha256(expected_string.encode('utf-8')).hexdigest()
        
        assert_that(self.builder.build_signature(data)).is_equal_to(expected_signature)


class _FawrySignatureBuilderDouble:
    def __init__(self):
        self._build_signature_called = False

    def build_signature(self, data):
        self._build_signature_called = True
        return "fake_signature"
        
    def assert_that_build_signature_is_called(self):
        assert_that(self._build_signature_called).is_true()