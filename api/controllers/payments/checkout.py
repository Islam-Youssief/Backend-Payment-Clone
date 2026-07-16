import http
import logging

import api.controllers.base as base
import api.core.exceptions as exceptions
import api.core.serializers.json as sjson
import api.services.payment.validators as validators
import api.services.payment.checkout as checkout_service


class CheckoutController:
    def __init__(self, flask_request, config, validator=None, handler=None):
        self._flask_request = flask_request
        self._config = config
        self._validator = validator or validators.UserPaymentDataValidator()
        self._handler = handler or _CheckoutHandler(self._config)

    @property
    def _body(self):
        return self._flask_request.json

    def pay(self):
        try:
            self._validator.validate(self._body)
            invoice = self._handler.process_payment(data=self._body)
            return (
                _CheckoutSerializer(invoice).serialize(self._flask_request.path),
                invoice.http_status
            )  
        except (exceptions.RequiredInputError, exceptions.InvalidInputError) as exc:
            return self._as_error_response(exc, http.HTTPStatus.BAD_REQUEST)  
        except exceptions.UnauthorizedAccessError as exc:  
            return self._as_error_response(exc, http.HTTPStatus.UNAUTHORIZED)


    def _as_error_response(self, error, status):
        logging.error(f"Creating error response: {error} {status}")
        return base.CoreErrorSerializer(error, status).serialize(self._flask_request.path), status

class _CheckoutHandler:
    def __init__(self, config, test_client=None):
        self._config = config
        self._client = test_client or checkout_service.CheckoutClient(self._config.env)

    def process_payment(self, data):
        response = self._client.pay_with_card(data=data)
        invoice = sjson.JsonObject(response.json())
        if invoice.status == 'success':
            invoice.http_status = http.HTTPStatus.CREATED
        elif invoice.status == 'bad_request':
            invoice.http_status = http.HTTPStatus.BAD_REQUEST
        elif invoice.status == 'unauthorized':
            invoice.http_status = http.HTTPStatus.UNAUTHORIZED
        elif invoice.status == 'Internal_server_error':
            invoice.http_status = http.HTTPStatus.INTERNAL_SERVER_ERROR
        elif invoice.status == 'invalid_secret_key':
            invoice.http_status = http.HTTPStatus.UNAUTHORIZED
        return invoice

class _CheckoutSerializer:
    def __init__(self, invoice):
        self._invoice = invoice

    def serialize(self, url):
        return {
            "url": url,
            "message": self._invoice.message,
            "status": self._invoice.status,       
            "amount": self._invoice.amount,
            "currency": self._invoice.currency,
            
        }