import re

import api.core.exceptions as exceptions


REQUIRED_FIELDS =("cardHolder", "cardNumber", "amount", "cvv" )

class UserPaymentDataValidator:

    def validate(self, data):
        self._validate_card_holder(data.get('cardHolder'))
        self._validate_amount(data.get('amount'))
        self._validate_card_number(data.get('cardNumber'))
        self._validate_cvv(data.get('cvv'))
        return True

    def _validate_card_holder(self, cardHolder):
        if not cardHolder:
            raise exceptions.RequiredInputError('user_name')
        names = cardHolder.strip().split()
        if len(names) < 3:
            raise exceptions.InvalidInputError(pname='cardHolder', invalid_value=cardHolder, message='User name must contain at least 3 names')

    def _validate_amount(self, amount):
        if amount == '':
            raise exceptions.RequiredInputError('amount')
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
        except (ValueError, TypeError):
            raise exceptions.InvalidInputError(pname='amount', invalid_value=amount, message='Amount must be a number')

    def _validate_card_number(self, cardNumber):
            if cardNumber == '':
                raise exceptions.RequiredInputError('visa_number')
            visa_clean = str(cardNumber).replace(' ', '').replace('-', '')

            if not re.match(r'^4[0-9]{15}$', visa_clean):
                raise exceptions.InvalidInputError(pname='cardNumber', invalid_value=cardNumber, message='Visa number must be 16 digits long')

    def _validate_cvv(self, cvv):
        if cvv == '':
            raise exceptions.RequiredInputError('cvv')
        cvv_clean = str(cvv).strip()
        if not re.match(r'^[0-9]{3,4}$', cvv_clean):
            raise exceptions.InvalidInputError(pname='cvv', invalid_value=cvv, message='CVV must be 3 or 4 digits long')