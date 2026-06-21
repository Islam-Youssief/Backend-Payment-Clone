import hashlib
import os

import api.services.requests_service as requests_service

FAWRY_PAYMENT_URL = 'atfawry.com/ECommerceWeb/Fawry/payments/charge'


class FawryClient:
    def __init__(self, env, test_request_sender=None, test_signature_builder=None):
        self._env = env
        self._request_sender = test_request_sender or requests_service.get_service(self._env)
        self._signature_builder = test_signature_builder or _FawrySignatureBuilder()

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
        merchant_code = os.environ.get('FAWRY_MERCHANT_CODE')
        data['merchantCode'] = merchant_code
        
        # Build the security signature
        data['signature'] = self._signature_builder.build_signature(data)
        
        response = self._request_sender.request(
            method='POST', 
            url=FAWRY_PAYMENT_URL, 
            json=data, 
            headers={'Content-Type': 'application/json'}
        )
        return response


class _FawrySignatureBuilder:
    def __init__(self):
        self._secure_key = os.environ.get('FAWRY_SECURITY_KEY', '')

    def build_signature(self, data):
        """
        Generates the SHA-256 signature required by Fawry Card Payment API.
        Format: merchantCode + merchantRefNum + customerProfileId + paymentMethod + amount + cardNumber + cardExpiryYear + cardExpiryMonth + cvv + secureKey
        """
        merchant_code = data.get('merchantCode', '')
        merchant_ref_num = data.get('merchantRefNum', '')
        customer_profile_id = data.get('customerProfileId', '')
        payment_method = data.get('paymentMethod', 'CARD')
        
        # Amount must be formatted to two decimal places
        amount = f"{float(data.get('amount', 0)):.2f}"
        
        card_number = data.get('cardNumber', '')
        expiry_year = data.get('cardExpiryYear', '')
        expiry_month = data.get('cardExpiryMonth', '')
        cvv = data.get('cvv', '')

        signature_string = (
            f"{merchant_code}{merchant_ref_num}{customer_profile_id}"
            f"{payment_method}{amount}{card_number}{expiry_year}"
            f"{expiry_month}{cvv}{self._secure_key}"
        )
        
        return hashlib.sha256(signature_string.encode('utf-8')).hexdigest()
