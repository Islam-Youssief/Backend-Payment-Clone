import http
import logging

import api.controllers.base as base
import api.core.exceptions as exceptions
import api.core.serializers.json as sjson
import api.services.payment.loginValidators as loginValidators
import api.services.payment.login as login_service


class LoginController:

    def __init__(self, flask_request, config, validator=None, handler=None ):
        self._flask_request = flask_request
        self._config = config
        self._validator = validator or loginValidators.UserLoginValidator()
        self._handler = handler or _LoginHandler(self._config)

    @property
    def _body(self):
        return self._flask_request.json

    def login(self):
        try:
            self._validator.validate(self._body)
            result = self._handler.process_login(data=self._body,
                authorization=self._flask_request.headers.get("Authorization")
            )
            return _LoginSerializer(result).serialize(self._flask_request.path), result.http_status
        except (exceptions.RequiredInputError,exceptions.InvalidInputError)as exc:
            return self._as_error_response(exc, http.HTTPStatus.BAD_REQUEST)

    def _as_error_response(self, error, status):
        logging.error(f"Creating error response: {error} {status}")
        return base.CoreErrorSerializer(error, status).serialize(self._flask_request.path), status


class _LoginHandler:

    def __init__(self, config ,test_client=None):
        self._config = config
        self._client = test_client or login_service.LoginClient(self._config.env)

    def process_login(self, data, authorization):
        response = self._client.login(
            data=data,
            authorization=authorization
        )
        print(response.json())

        result = sjson.JsonObject(response.json())
        result.http_status = http.HTTPStatus.OK

        if result.status == "success":
            result.http_status = http.HTTPStatus.CREATED
        elif result.status in (
                "invalid_credentials",
                "invalid_token",
                "expired_token",
                "invalid_user_token"
        ):
            result.http_status = http.HTTPStatus.UNAUTHORIZED
        elif result.status == "missing_permission_token":
            result.http_status = http.HTTPStatus.FORBIDDEN
        return result


class _LoginSerializer:

    def __init__(self,result):
        self._result = result

    def serialize(self, url):
        return {
            "url":url,
            "message":self._result.message,
            "status": self._result.status,
        }

