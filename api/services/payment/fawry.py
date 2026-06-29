import hashlib

import api.core.configurations as configurations
import api.core.exceptions as exceptions
import api.services.requests_service as requests_service

FAWRY_PAYMENT_URL = 'atfawry.com/ECommerceWeb/Fawry/payments/charge'


class FawryClient:
    def __init__(self, env, test_request_sender=None, test_signature_builder=None, test_validator=None):
        self._env = env
        self._request_sender = test_request_sender or requests_service.get_service(self._env)
        self._signature_builder = test_signature_builder or _FawrySignatureBuilder()
        self._validator = test_validator or UserDataValidator()

    def pay_with_visa(self, data):
        """
        Executes a card payment using Fawry's server-to-server API.
        The data dictionary should at least contain:
        - merchantRefNum: Unique order identifier
        - customerProfileId: (Optional) Customer ID
        - amount: Order total amount
        - cardNumber: Credit card number
        - cardExpiryYear: 2-digit expiry year
        - cardExpiryMonth: 2-digit expiry month
        - cvv: 3-digit CVV
        """
        self._validator.validate(data)
        data['signature'] = self._signature_builder.build_signature(data)
        response = self._request_sender.request(
            method='POST', 
            url=FAWRY_PAYMENT_URL, 
            json=data, 
            headers={'Content-Type': 'application/json'}
        )
        return response

class UserDataValidator:
    def validate(self, data):
        required_fields = ['merchantRefNum', 'amount', 'cardNumber', 'cardExpiryYear', 'cardExpiryMonth', 'cvv']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise exceptions.RequiredInputError(f'Missing fields: {missing_fields}')
        self._validate_amount(data['amount'])
        self._validate_card(data['cardNumber'])
        self._validate_expiry(data['cardExpiryYear'], data['cardExpiryMonth'])
        self._validate_cvv(data['cvv'])

    def _validate_amount(self, amount):
        try:
            amount = float(amount)
        except ValueError:
            raise exceptions.InputDataTypeError(message=f'Invalid amount type. Expected: Decimal, Got: {type(amount).__name__}')
        if amount <= 0:
            raise exceptions.ValidationError(message='Amount must be greater than zero')

    def _validate_card(self, card_number):
        if not (len(card_number) == 16 and card_number.isdigit()):
            raise exceptions.ValidationError(message='Invalid card number')

    def _validate_expiry(self, year, month):
        if not (len(year) == 2 and len(month) == 2 and int(year) > 20 and int(month) >= 1 and int(month) <= 12):
            raise exceptions.ValidationError(message='Invalid card expiry date')

    def _validate_cvv(self, cvv):
        if not (len(cvv) == 3 and cvv.isdigit()):
            raise exceptions.ValidationError(message='Invalid CVV')


class _FawrySignatureBuilder:
    def __init__(self):
        self._secure_key = configurations.PaymentsConfig.fawry_security_key
        self._merchant_code = configurations.PaymentsConfig.fawry_merchant_code

    def build_signature(self, data):
        """
        Generates the SHA-256 signature required by Fawry Card Payment API.
        Format: merchantCode + merchantRefNum + customerProfileId + paymentMethod + amount + cardNumber + cardExpiryYear + cardExpiryMonth + cvv + secureKey
        """
        merchant_ref_num = data.get('merchantRefNum', '')
        customer_profile_id = data.get('customerProfileId', '')
        payment_method = data.get('paymentMethod', 'CARD')
        amount = f"{float(data.get('amount', 0)):.2f}"
        card_number = data.get('cardNumber', '')
        expiry_year = data.get('cardExpiryYear', '')
        expiry_month = data.get('cardExpiryMonth', '')
        cvv = data.get('cvv', '')
        signature_string = (
            f"{self._merchant_code}{merchant_ref_num}{customer_profile_id}"
            f"{payment_method}{amount}{card_number}{expiry_year}"
            f"{expiry_month}{cvv}{self._secure_key}"
        )
        return hashlib.sha256(signature_string.encode('utf-8')).hexdigest()
