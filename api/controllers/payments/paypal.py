import http
import logging

import api.controllers.base as base
import api.core.exceptions as exceptions
import api.core.serializers.json as sjson
import api.services.payment.validators as validators
import api.services.payment.paypal as paypal_service


class PayPalController:
    def __init__(self, flask_request, config, validator=None, handler=None):
        self._flask_request = flask_request
        self._config = config
        self._validator = validator or validators.UserPaymentDataValidator()
        self._handler = handler or _PayPalHandler(self._config)

    @property
    def _body(self):
        return self._flask_request.json
    
    @property
    def _token(self):
        return self._flask_request.headers.get('Authorization')
    
    def pay(self):
        try:
            self._validator.validate(self._body, self._token)
            invoice = self._handler.process_payment(data=self._body)
            return _PayPalSerializer(invoice).serialize(self._flask_request.path), http.HTTPStatus.CREATED
        except (exceptions.RequiredInputError, exceptions.InvalidInputError) as exc:
            return self._as_error_response(exc, http.HTTPStatus.BAD_REQUEST)
        except exceptions.UnauthorizedAccessError as exc:
            return self._as_error_response(exc, http.HTTPStatus.UNAUTHORIZED)


    def _as_error_response(self, error, status):
        logging.error(f"Creating error response: {error} {status}")
        return base.CoreErrorSerializer(error, status).serialize(self._flask_request.path), status


class _PayPalHandler:
    def __init__(self, config, test_client=None):
        self._config = config
        self._client = test_client or paypal_service.PayPalClient(self._config.env)

    def process_payment(self, data):
        response = self._client.pay_with_visa(data=data)
        invoice = sjson.JsonObject(response.json())
        # TODO: store the invoice for the current logged-in user
        return invoice
        
        
class _PayPalSerializer:
    def __init__(self, invoice):
        self._invoice = invoice

    def serialize(self, url):
        return {
            "url": url,
            "message": self._invoice.message,
            "status": self._invoice.status,       
            "transaction_id": self._invoice.transaction_id,
            "amount": self._invoice.amount,
            "currency": self._invoice.currency,
            "payment_method": self._invoice.payment_method
        }