import os
import json

import api.core.configurations as configuration
import api.services.requests_service as requests_service
import api.core.exceptions as exception
import api.services.rate_limit_service as rate_limiter_service

CHECKOUT_PAYMENT_URL = "api.sandbox.checkout.com/payments"


class CheckoutClient:
    def __init__(self , env, rate_limiter = None, user_data_validator = None , test_request_sender=None):
        self._env = env 
        self._request_sender = test_request_sender or requests_service.get_service(env)
        self._user_data_validator= user_data_validator or UserDataValidator()
        self._rate_limiter = rate_limiter or  rate_limiter_service.RateLimitService()
        
    
    def pay_with_card(self, data , idempotency_key):
        self._idempotency_key = idempotency_key
        self._user_data_validator.validate_payment_data(data)
        self._rate_limiter.check(configuration.PaymentsConfig().checkout_secret_key)
        response = self._request_sender.request(method='POST', url=f'{configuration.PaymentsConfig().checkout_prefix_code}.{CHECKOUT_PAYMENT_URL}', json=data, headers=self._headers)
        return response

    @property
    def _headers(self):
        return{
            'Content-Type':'application/json',
            'Authorization': f"Bearer {configuration.PaymentsConfig().checkout_secret_key}",
            "Cko-Idempotency-Key": self._idempotency_key,
        }

class UserDataValidator:

    def validate_payment_data(self, data):
        self.validate_amount(data["amount"])
        self.validate_card_number(data["cardNumber"])
        self.validate_card_cvv(data["cvv"])

    def validate_amount(self, amount):
        if type(amount) not in [int, float]:
            raise exception.InputDataTypeError("Amount must be numeric")
        if amount <= 0:
            raise exception.InvalidInputError(amount, "Amount must be greater than 0")

    def validate_card_number(self, number):
        if not number.isdigit():
            raise exception.InputDataTypeError(number, "Card number must contain digits only")
        if len(number) != 16:
            raise exception.InvalidInputError(number, "Card number must be 16 digits")

    def validate_card_cvv(self, cvv):
        if not cvv.isdigit():
            raise exception.InputDataTypeError(cvv, "CVV must contain digits only")
        if len(cvv) != 3:
            raise exception.InvalidInputError(cvv, "CVV length must be 3 digits")