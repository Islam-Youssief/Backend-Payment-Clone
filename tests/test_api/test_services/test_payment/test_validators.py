import unittest

from assertpy import assert_that

import api.core.exceptions as exceptions
import api.services.payment.validators as validators


class TestUserPaymentDataValidator(unittest.TestCase):

    def setUp(self):
        self.validator = validators.UserPaymentDataValidator()
        self.data = {
            "user_name": "Ahmed Mohammad Ali",
            "amount": 100,
            "visa_number": "4242424242424242",
            "cvv": "123"
        }

    def test_validate_valid_data(self):
        result = self.validator.validate(self.data)
        assert_that(result).is_true()

    def test_user_name_is_missing(self):
        self.data['user_name'] = ''
        with self.assertRaises(exceptions.RequiredInputError) as exc:
            self.validator.validate(self.data)
        assert_that(exc.exception.message).is_equal_to("Input <user_name> is required")
        assert_that(exc.exception.name).is_equal_to("user_name")

    def test_user_name_is_invalid(self):
        self.data['user_name'] = 'Ahmed Mohammad'
        with self.assertRaises(exceptions.InvalidInputError) as exc:
            self.validator.validate(self.data)
        assert_that(exc.exception.message).is_equal_to("User name must contain at least 3 names")
        assert_that(exc.exception.name).is_equal_to("user_name")
        assert_that(exc.exception.value).is_equal_to("Ahmed Mohammad")

    def test_amount_is_missing(self):
        self.data['amount'] = ''
        with self.assertRaises(exceptions.RequiredInputError) as exc:
            self.validator.validate(self.data)
        assert_that(exc.exception.message).is_equal_to("Input <amount> is required")
        assert_that(exc.exception.name).is_equal_to('amount')

    def test_amount_is_zero(self):
        self.data['amount'] = 0
        with self.assertRaises(exceptions.InvalidInputError) as exc :
            self.validator.validate(self.data)
        assert_that(exc.exception.message).is_equal_to("Amount must be a number")
        assert_that(exc.exception.name).is_equal_to("amount")
        assert_that(exc.exception.value).is_equal_to(0)

    def test_amount_string_is_invalid(self):
        self.data['amount'] = 'abc'
        with self.assertRaises(exceptions.InvalidInputError) as exc:
            self.validator.validate(self.data)
        assert_that(exc.exception.message).is_equal_to("Amount must be a number")
        assert_that(exc.exception.name).is_equal_to('amount')
        assert_that(exc.exception.value).is_equal_to('abc')

    def test_visa_is_missing(self):
        self.data['visa_number'] = ''
        with self.assertRaises(exceptions.RequiredInputError) as exc:
            self.validator.validate(self.data)
        assert_that(exc.exception.message).is_equal_to("Input <visa_number> is required")
        assert_that(exc.exception.name).is_equal_to('visa_number')

    def test_visa_is_invalid(self):
        self.data['visa_number'] = '0123456789'
        with self.assertRaises(exceptions.InvalidInputError) as exc:
            self.validator.validate(self.data)
        assert_that(exc.exception.message).is_equal_to('Visa number must be 16 digits long')
        assert_that(exc.exception.name).is_equal_to('visa_number')
        assert_that(exc.exception.value).is_equal_to('0123456789')

    def test_cvv_is_missing(self):
        self.data['cvv'] = ''
        with self.assertRaises(exceptions.RequiredInputError) as exc:
            self.validator.validate(self.data)
        assert_that(exc.exception.message).is_equal_to("Input <cvv> is required")
        assert_that(exc.exception.name).is_equal_to('cvv')

    def test_cvv_is_invalid(self):
        self.data['cvv'] = '12'
        with self.assertRaises(exceptions.InvalidInputError) as exc:
            self.validator.validate(self.data)
        assert_that(exc.exception.message).is_equal_to("CVV must be 3 or 4 digits long")
        assert_that(exc.exception.name).is_equal_to('cvv')
        assert_that(exc.exception.value).is_equal_to('12')



if __name__ == '__main__':
    unittest.main()