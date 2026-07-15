import re

import api.core.exceptions as exceptions

REQUIRED_FIELDS = ('cardHolder', 'cardNumber', 'amount', 'cvv')


class UserPaymentDataValidator:

    def validate(self, data):
        self._validate_required_fileds(data)
        self._validate_having_many_names(data.get('cardHolder'))
        self._validate_card_number(data.get('cardNumber'))
        self._validate_amount(data.get('amount'))
        self._validate_cvv(data.get('cvv'))
        return True

    def _validate_required_fileds(self, data):
        for required_field in REQUIRED_FIELDS:
            if required_field not in data:
                raise exceptions.RequiredInputError(required_field)

    def _validate_having_many_names(self, card_holder):
        if len(card_holder.split()) < 3:
            raise exceptions.InvalidInputError(pname='cardHolder', invalid_value=card_holder,
                                               message='Card holder must contain at least 3 names')

    def _validate_card_number(self, card):
        card = str(card).replace(' ', '').replace('-', '')
        if not re.match(r'^[0-9]{16}$', card):
            raise exceptions.InvalidInputError(pname='cardNumber', invalid_value=card,
                                               message='Card number must be 16 digits long')

    def _validate_amount(self, amount):
        if not str(amount).isdigit() or amount <= 0:
            raise exceptions.InvalidInputError(pname='amount', invalid_value=amount,
                                               message='Amount must be valid number')

    def _validate_cvv(self, cvv):
        if not re.match(r'^[0-9]{3,4}$', cvv):
            raise exceptions.InvalidInputError(pname='cvv', invalid_value=cvv, message='CVV must be 3 or 4 digits long')

    def _validate_email(self, email):
        if email == "":
            raise exceptions.RequiredInputError(pname='email',  message='Email address cannot be empty')
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise exceptions.InvalidInputError(pname='email', invalid_value=email, message='Email must be valid email')

    def _validate_password(self, password):
        if password == "":
            raise exceptions.RequiredInputError(pname='password', message='Password cannot be empty')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            raise exceptions.InvalidInputError(pname='password', invalid_value=password, message='Password must be between 8 and 20 alphanumeric characters')