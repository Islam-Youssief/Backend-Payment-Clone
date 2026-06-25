import re

import api.core.exceptions as exceptions


class UserPaymentDataValidator:

    def validate(self, data):
        self._validate_user_name(data.get('user_name'))
        self._validate_amount(data.get('amount'))
        self._validate_visa_number(data.get('visa_number'))
        self._validate_cvv(data.get('cvv'))
        return True

    def _validate_user_name(self, user_name):
        if not user_name:
            raise exceptions.RequiredInputError('user_name')
        names = user_name.strip().split()
        if len(names) < 3:
            raise exceptions.InvalidInputError(pname='user_name', invalid_value=user_name, message='User name must contain at least 3 names')

    def _validate_amount(self, amount):
        if amount is '':
            raise exceptions.RequiredInputError('amount')
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
        except (ValueError, TypeError):
            raise exceptions.InvalidInputError(pname='amount', invalid_value=amount, message='Amount must be a number')

    def _validate_visa_number(self, visa_number):
            if visa_number is '':
                raise exceptions.RequiredInputError('visa_number')
            visa_clean = str(visa_number).replace(' ', '').replace('-', '')

            if not re.match(r'^4[0-9]{15}$', visa_clean):
                raise exceptions.InvalidInputError(pname='visa_number', invalid_value=visa_number, message='Visa number must be 16 digits long')

    def _validate_cvv(self, cvv):
        if cvv is '':
            raise exceptions.RequiredInputError('cvv')
        cvv_clean = str(cvv).strip()
        if not re.match(r'^[0-9]{3,4}$', cvv_clean):
            raise exceptions.InvalidInputError(pname='cvv', invalid_value=cvv, message='CVV must be 3 or 4 digits long')