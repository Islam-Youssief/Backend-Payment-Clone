import os
import json

import api.core.configurations as configuration
import api.services.requests_service as requests_service
import api.core.exceptions as exception


CHECKOUT_PAYMENT_BASE_URL=f'https://{configuration.PaymentsConfig().checkout_prefix_code}.api.sandbox.checkout.com'
CHECKOUT_PAYMENT_URL=f'{CHECKOUT_PAYMENT_BASE_URL}/payments'


class CheckoutClient:
    def __init__(self , env, user_data_validator = None , test_request_sender=None):
        self._env = env 
        self._request_sender = test_request_sender or requests_service.get_service(env)
        self._user_data_validator= user_data_validator or UserDataValidator()
        
    
    def pay_with_card(self, data):
        self._user_data_validator.validate_payment_data(data)
        response = self._request_sender.request(method='POST', url=CHECKOUT_PAYMENT_URL, data=json.dumps(data), headers=self._headers)
        return response

    @property
    def _headers(self):
        return{
            'Content-Type':'application/json',
            'Authorization': f"Bearer {configuration.PaymentsConfig().checkout_secret_key}"
        }

class UserDataValidator:

    def validate_card(self, card):
        self.validate_card_number(card["number"])
        self.validate_card_cvv(card["cvv"])

    def validate_payment_data(self, data):
        self.validate_amount(data["amount"])
        self.validate_card(data["source"])

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


    def validate_card_cvv(self , cvv):
        if not cvv.isdigit():
            raise exception.InputDataTypeError(cvv, "CVV must contain digits only")

        if len(cvv) != 3:
            raise exception.InvalidInputError(cvv, "CVV length must be 3 digits")

