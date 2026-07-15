import re

import api.core.exceptions as exceptions

REQUIRED_FIELDS = ('email', 'password')


class UserLoginValidator:

    def validate(self, data):
        self._validate_required_fields(data)
        self._validate_email(data.get('email'))
        self._validate_password(data.get('password'))
        return True

    def _validate_required_fields(self, data):
        for required_field in REQUIRED_FIELDS:
            if required_field not in data:
                raise exceptions.RequiredInputError(required_field)


    def _validate_email(self, email):
        if not email :
            raise exceptions.RequiredInputError(pname='email',  message='Email address cannot be empty')
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise exceptions.InvalidInputError(pname='email', invalid_value=email, message='"Email must be a valid email address"')

    def _validate_password(self, password):
        if not password :
            raise exceptions.RequiredInputError(pname='password', message='Password cannot be empty')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            raise exceptions.InvalidInputError(pname='password', invalid_value=password, message='Password must be between 8 and 20 alphanumeric characters')