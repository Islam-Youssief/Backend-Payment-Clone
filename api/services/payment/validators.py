import re

from api.core.exceptions import InvalidInputError, RequiredInputError, ValidationError


class UserPaymentDataValidator:
    def validate(self, data):
        self._validate_user_name(data.get('user_name'))
        self._validate_amount(data.get('amount'))
        self._validate_visa_number(data.get('visa_number'))
        self._validate_cvv(data.get('cvv'))
        return True

    def _validate_user_name(self, user_name):
        if not user_name:
            raise RequiredInputError('user_name')
        names = user_name.strip().split()
        if len(names) < 3:
            raise ValidationError('User name must contain at least 3 names')

    def _validate_amount(self, amount):
        if amount is None:
            raise RequiredInputError('amount')
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
        except (ValueError, TypeError):
            raise InvalidInputError('Amount must be a number', amount)

    def _validate_visa_number(self, visa_number):
        if not visa_number:
            raise RequiredInputError('Visa number is required')
        visa_clean = str(visa_number).replace(' ', '').replace('-', '')

        if not re.match(r'^4[0-9]{15}$', visa_clean):
            raise InvalidInputError('Visa number must be 15 digits long', visa_number)

    def _validate_cvv(self, cvv):
        if not cvv:
            raise RequiredInputError('CVV is required')
        cvv_clean = str(cvv).strip()
        if not re.match(r'^[0-9]{3,4}$', cvv_clean):
            raise InvalidInputError('CVV must be 3 digits long', cvv)