import http
import logging
import requests

import api.controllers.base as base
import api.core.exceptions as exceptions
import api.core.serializers.json as sjson
import api.services.payment.validators as validators
import api.services.payment.fawry as fawry_service

class FawryController:
    def __init__(self, flask_request, app_config, validator=None, handler=None):
        self._flask_request = flask_request
        self._app_config = app_config
        self._validator = validator or validators.UserPaymentDataValidator()
        self._handler = handler or _FawryHandler(self._app_config)
        self._serializer = _FawrySerializer()

    @property
    def _body(self):
        return self._flask_request.json
    
    @property
    def _token(self):
        return self._flask_request.headers.get('Authorization')
    
    @property
    def _url(self):
        return self._flask_request.path

    def pay(self):
        try:
            self._validator.validate(self._body, self._token)
            invoice = self._handler.process_payment(self._body)
            return self._serializer.serialize(invoice, self._url), http.HTTPStatus.CREATED
        except (exceptions.RequiredInputError, exceptions.InvalidInputError) as exc:
            return self._as_error_response(exc, http.HTTPStatus.BAD_REQUEST)
        except exceptions.UnauthorizedAccessError as exc:
            return self._as_error_response(exc, http.HTTPStatus.UNAUTHORIZED)
        except exceptions.ResponseError as exc:
            status_code = exc.status_code
            if status_code in (http.HTTPStatus.BAD_GATEWAY, http.HTTPStatus.SERVICE_UNAVAILABLE):
                err = exceptions.ValidationError("External service unavailable")
                return self._as_error_response(err, http.HTTPStatus.BAD_GATEWAY)
            elif status_code == http.HTTPStatus.INTERNAL_SERVER_ERROR:
                err = exceptions.ValidationError("External service error")
                return self._as_error_response(err, http.HTTPStatus.BAD_GATEWAY)
            elif status_code == http.HTTPStatus.PAYMENT_REQUIRED:
                err = exceptions.ValidationError("Insufficient Balance")
                return self._as_error_response(err, http.HTTPStatus.PAYMENT_REQUIRED)
        except requests.exceptions.Timeout as exc:
            err = exceptions.ValidationError("External service timeout")
            return self._as_error_response(err, http.HTTPStatus.GATEWAY_TIMEOUT)

    def _as_error_response(self, error, status):
        logging.error(f"Creating error response: {error} {status}")
        return base.CoreErrorSerializer(error, status).serialize(self._url), status

class _FawryHandler:
    def __init__(self, app_config, test_client=None):
        self._config = app_config
        self._client = test_client or fawry_service.FawryClient(self._config.env)

    def process_payment(self, data):
        response = self._client.pay_with_card(data=data)
        invoice = sjson.JsonObject(response.json())
        return invoice


class _FawrySerializer:

    def serialize(self, invoice, url):
        return {
            "url": url,
            "reference_number": invoice.reference_number,
            "merchant_ref_number": invoice.merchant_ref_number,
            "order_amount": invoice.order_amount,
            "payment_amount": invoice.payment_amount,
            "fawry_fees": invoice.fawry_fees,
            "payment_method": invoice.payment_method,
            "order_status": invoice.order_status,
            "payment_time": invoice.payment_time,
            "customer_mobile": invoice.customer_mobile,
            "customer_mail": invoice.customer_mail,
            "customer_profile_id": invoice.customer_profile_id,
            "signature": invoice.signature,
            "status_code": invoice.status_code,
            "status_description": invoice.status_description
        }
