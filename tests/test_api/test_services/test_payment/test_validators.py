import unittest

from assertpy import assert_that

import api.core.exceptions as exceptions
import api.services.payment.validators as validators


class TestUserPaymentDataValidator(unittest.TestCase):

    def setUp(self):
        self.validator = validators.UserPaymentDataValidator()
        self.data = {
            "cardHolder": "TESTER TESTING VALUE",
            "cardNumber": "4242424242424242",
            "amount": 100,
            "cvv": "123"
        }

    def test_validate_valid_data_not_raising_error_if_values_are_valid(self):
        result = self.validator.validate(self.data)
        assert_that(result).is_true()

    def test_card_holder_is_missing(self):
        self.when_removing('cardHolder')
        self.expect_error_raised_with(exceptions.RequiredInputError, "Input <cardHolder> is required", 'cardHolder')

    def test_card_number_is_missing(self):
        self.when_removing('cardNumber')
        self.expect_error_raised_with(exceptions.RequiredInputError, "Input <cardNumber> is required", 'cardNumber')

    def test_amount_is_missing(self):
        self.when_removing('amount')
        self.expect_error_raised_with(exceptions.RequiredInputError, "Input <amount> is required", 'amount')

    def test_cvv_is_missing(self):
        self.when_removing('cvv')
        self.expect_error_raised_with(exceptions.RequiredInputError, "Input <cvv> is required", 'cvv')

    def test_validating_having_only_two_names(self):
        self.when_changed('cardHolder', 'Missing Name')
        self.expect_error_raised_with(exceptions.InvalidInputError, "Card holder must contain at least 3 names", 'cardHolder')

    def test_validating_valid_card_number(self):
        self.when_changed('cardNumber', '12345')
        self.expect_error_raised_with(exceptions.InvalidInputError, "Card number must be 16 digits long",'cardNumber')

    def test_validating_having_only_numbers_for_amount(self):
        self.when_changed('amount', '1AAA')
        self.expect_error_raised_with(exceptions.InvalidInputError, "Amount must be valid number", 'amount')
    
    def test_validating_positive_value_for_amount(self):
        self.when_changed('amount', -100)
        self.expect_error_raised_with(exceptions.InvalidInputError, "Amount must be valid number", 'amount')

    def test_validating_valid_cvv_numbers(self):
        self.when_changed('cvv', 'AAAAA')
        self.expect_error_raised_with(exceptions.InvalidInputError, "CVV must be 3 or 4 digits long", 'cvv')
    
    def test_validating_cvv_is_not_less_than_three_numbers(self):
        self.when_changed('cvv', '56')
        self.expect_error_raised_with(exceptions.InvalidInputError, "CVV must be 3 or 4 digits long", 'cvv')

    def test_validating_cvv_is_not_more_than_four_numbers(self):
        self.when_changed('cvv', '12345')
        self.expect_error_raised_with(exceptions.InvalidInputError, "CVV must be 3 or 4 digits long", 'cvv')

    def when_removing(self, key):
        del self.data[key]
        return self
    
    def when_changed(self, key, value):
        self.data[key] = value
        return self

    def expect_error_raised_with(self, error, message, name):
        with self.assertRaises(error) as exc:
            self.validator.validate(self.data)
        assert_that(exc.exception.message).is_equal_to(message)
        assert_that(exc.exception.name).is_equal_to(name)


if __name__ == '__main__':
    unittest.main()