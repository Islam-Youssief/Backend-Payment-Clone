import unittest

from assertpy import assert_that

from api.services.payment.validators import UserPaymentDataValidator
from api.core.exceptions import InvalidInputError, RequiredInputError, ValidationError

class TestUserPaymentDataValidator(unittest.TestCase):

    def setUp(self):
        self.validator = UserPaymentDataValidator()

    def test_validate_valid_data(self):
        data = {
            "user_name": "Ahmed Mohammad Ali",
            "amount": 100,
            "visa_number": "4242424242424242",
            "cvv": "123"
        }
        result = self.validator.validate(data)
        assert_that(result).is_true()

    def test_user_name_missing(self):
        with self.assertRaises(RequiredInputError):
            self.validator._validate_user_name(None)

    def test_user_name_invalid(self):
        with self.assertRaises(ValidationError):
            self.validator._validate_user_name("Ahmed Mohammad")

    def test_amount_missing(self):
        with self.assertRaises(RequiredInputError):
            self.validator._validate_amount(None)

    def test_amount_zero(self):
        with self.assertRaises(InvalidInputError):
            self.validator._validate_amount(0)

    def test_amount_string_invalid(self):
        with self.assertRaises(InvalidInputError):
            self.validator._validate_amount("abc")

    def test_visa_missing(self):
        with self.assertRaises(RequiredInputError):
            self.validator._validate_visa_number(None)

    def test_visa_invalid(self):
        with self.assertRaises(InvalidInputError):
            self.validator._validate_visa_number("0123456789")

    def test_cvv_missing(self):
        with self.assertRaises(RequiredInputError):
            self.validator._validate_cvv(None)

    def test_cvv_invalid(self):
        with self.assertRaises(InvalidInputError):
            self.validator._validate_cvv("12")


if __name__ == '__main__':
    unittest.main()