import os

import api.services.requests_service as requests_service
import api.core.exceptions as exception


CHECKOUT_PAYMENT_BASE_URL='https://sl73izp6.api.sandbox.checkout.com'
CHECKOUT_PAYMENT_URL=CHECKOUT_PAYMENT_BASE_URL + '/payments'


class CheckoutClient:
    def __init__(self , env , test_request_sender=None):
        self._env = env 
        self._request_sender = test_request_sender or requests_service.get_service(env)
    
    def pay_with_card(self, data):
        self.validate_payment_data(data)
        response = self._request_sender.request(method='POST', url=CHECKOUT_PAYMENT_URL, data=data, headers=self._headers)
        return response

    @property
    def _headers(self):
        return{
            'Content-Type':'application/json',
            'Authorization': f"Bearer {os.environ.get('CHECKOUT_SECRET_KEY')}"
        }


    ################################# validations #################################

    def validate_payment_data(self, data):
        self.validate_amount(data["amount"])
        self.validate_card_number(data["source"]["number"])
        self.validate_card_cvv(data["source"]["cvv"])


    def validate_amount(self, amount):
        if type(amount) not in [int, float]:
            raise exception.InputDataTypeError("Amount must be numeric")

        if amount <= 0:
            raise exception.ValidationError("Amount must be greater than 0")


    def validate_card_number(self, number):
        if not number.isdigit():
            raise exception.ValidationError("Card number must contain digits only")

        if len(number) != 16:
            raise exception.ValidationError("Card number must be 16 digits")


    def validate_card_cvv(self , cvv):
        if not cvv.isdigit():
            raise exception.ValidationError("CVV must contain digits only")

        if len(cvv) != 3:
            raise exception.ValidationError("CVV length must be 3 digits")

