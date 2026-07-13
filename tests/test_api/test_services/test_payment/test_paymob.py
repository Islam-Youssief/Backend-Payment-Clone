import unittest
import api.services.payment.paymob as paymob
import api.services.requests_service as requests_service
from assertpy import assert_that
import tests.doubles.requests as requests_doubles
import api.core.exceptions as exceptions

class TestPaymobClient(unittest.TestCase):
    def setUp(self):
        self.request_sender = requests_doubles.RequestSenderDouble(json={"message" : "success"})
        self.validator = _UserDataValidatorDouble()
        self.client = paymob.PaymobClient('lcl',self.request_sender,self.validator)
        self.fake_data=_get_dummy_data()
        
    def test_client_uses_real_if_doubles_are_not_sent(self):
        client_without_doubles  = paymob.PaymobClient('prd')
        assert_that(client_without_doubles._request_sender).is_instance_of(requests_service.RequestsWrapper)
        assert_that(client_without_doubles._validator).is_instance_of(paymob.PaymobUserDataValidator)

    def test_client_create_intention_calls_requests_with_expected_params(self):
        response = self.client.create_intention(self.fake_data)
        assert_that(response.json().get('message')).is_equal_to('success')
        self.request_sender.assert_that_request_is_called_with(
           method= "POST",
            url= paymob.PAYMOB_INTENTION_URL,
            headers= {
                     "Authorization": f"Token {self.client._secret_key}",
                     "Content-Type": "application/json"
                    },
            json= self.fake_data
        )
        self.validator.assert_that_validation_is_called_with(self.fake_data)


class TestUserDataValidator(unittest.TestCase):
    def setUp(self):
        self.validator = paymob.PaymobUserDataValidator()
        self.fake_data ={
            "amount": 2000,
            "currency": "EGP",
            "payment_methods": [158],
            "items": [
                {
                "name": "Item name",
                "amount": 2000,
                }],
            "billing_data": {
                "first_name": "ala",
                "last_name": "zain",
                "email": "ali@gmail.com",
            }}
    def test_raises_required_input_error_when_field_are_missing(self):
        with self.assertRaises(exceptions.RequiredInputError):
            self.validator.validate(data={'amount':34})

    def test_raises_validation_error_when_amount_is_zero(self):#
        invalid_data = {**self.fake_data, 'amount': 0}
        with self.assertRaises(exceptions.ValidationError):
            self.validator.validate(data=invalid_data)

    def test_raises_validation_error_when_amount_is_negative(self):
        invalid_data = {**self.fake_data,'amount' : -69}
        with self.assertRaises(exceptions.ValidationError):
            self.validator.validate(data=invalid_data)
    
    def test_raises_input_data_type_error_when_amount_is_string(self):
        invalid_data = {**self.fake_data, 'amount' : 'xD20'}
        with self.assertRaises(exceptions.InputDataTypeError):
            self.validator.validate(data=invalid_data)
    
    def test_raises_required_input_error_when_email_is_missing(self):
        invalid_data = {**self.fake_data,"billing_data":{"first_name" : "ala","last_name" : "zain"}}
        with self.assertRaises(exceptions.RequiredInputError):
            self.validator.validate(invalid_data)
            
    def test_valid_data_passes(self):
            self.validator.validate(self.fake_data)

class  _UserDataValidatorDouble:
        def __init__(self):
            self._validate_called_with = None

        def validate(self, data):
            self._validate_called_with = data

        def assert_that_validation_is_called_with(self, data):
            assert_that(self._validate_called_with).is_equal_to(data)

if __name__ == "__main__":
    unittest.main()

def _get_dummy_data(self):
    return {
                    "amount": 2000,
                    "currency": "EGP",
                    "payment_methods": [158],
                    "items": [
                        {
                        "name": "Item name",
                        "amount": 2000,
                        "description": "Item description",
                        "quantity": 1
                        }],
                    "billing_data": {
                        "apartment": "dumy",
                        "first_name": "ala",
                        "last_name": "zain",
                        "street": "dumy",
                        "building": "dumy",
                        "phone_number": "+92345xxxxxxxx",
                        "city": "dumy",
                        "country": "dumy",
                        "email": "ali@gmail.com",
                        "floor": "dumy",
                        "state": "dumy"
                    },
                    "extras": {
                        "ee": 22
                    },
                    "special_reference": "phe4sjw11q-1xxxxxxxxx",
                    "expiration": 3600,
                    "notification_url": "https://webhook.site/dabe4968-5xxxxxxxxxxxxxxxxxxxxxx",
                    "redirection_url": "https://www.google.com/"
                    }
