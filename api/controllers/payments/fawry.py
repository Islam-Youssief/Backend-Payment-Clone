import http
import logging
import uuid
import requests
import flask as fl

import api.controllers.base as base
import api.core.exceptions as exceptions
import api.core.serializers.json as sjson
import api.services.customer_service as customer_service
import api.services.payment_attempt_service as payment_attempt_service
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
        except (exceptions.ExternalServiceUnavailableError, exceptions.ExternalServiceError) as exc:
            return self._as_error_response(exc, http.HTTPStatus.BAD_GATEWAY)
        except exceptions.InsufficientBalanceError as exc:
            return self._as_error_response(exc, http.HTTPStatus.PAYMENT_REQUIRED)
        except exceptions.ResponseError as exc:
            return self._as_error_response(exc, exc.status_code)
        except requests.exceptions.Timeout as exc:
            return self._as_error_response(exceptions.ExternalServiceUnavailableError("External service timeout"), http.HTTPStatus.GATEWAY_TIMEOUT)

    def _as_error_response(self, error, status):
        logging.error(f"Creating error response: {error} {status}")
        return base.CoreErrorSerializer(error, status).serialize(self._url), status

class _FawryHandler:
    def __init__(self, app_config, test_client=None, customer_svc=None, payment_attempt_svc=None):
        self._config = app_config
        self._client = test_client or fawry_service.FawryClient(self._config.env)
        self._customer_service = customer_svc or customer_service.CustomerService()
        self._payment_attempt_service = payment_attempt_svc or payment_attempt_service.PaymentAttemptService()

    def process_payment(self, data):
        customer_name = data.get('customer_name') or data.get('card_holder') or data.get('cardHolder') or 'Fawry Customer'
        customer_email = data.get('customer_email') or data.get('customer_mail') or data.get('email') or 'customer@fawry.com'
        amount = float(data.get('amount', 0.0))
        currency = data.get('currency', 'EGP')
        raw_idem = fl.request.headers.get('X-Idempotency-Key') if fl.has_request_context() else None
        idem_key = uuid.UUID(str(raw_idem)) if raw_idem else uuid.uuid7()

        customer = self._customer_service.get_or_create_customer(name=customer_name, email=customer_email)
        payment_attempt = self._payment_attempt_service.create_payment_attempt(
            customer_id=customer.id,
            provider='FAWRY',
            amount=amount,
            customer_name=customer.name,
            customer_email=customer.email,
            idempotency_key=idem_key,
            currency=currency,
            status='PENDING'
        )

        response = self._client.pay_with_card(data=data)
        if response.status_code != http.HTTPStatus.OK:
            self._payment_attempt_service.update_payment_attempt_status(
                payment_id=payment_attempt.id,
                status='FAILED',
                provider_reference='NONE',
                failure_reason=f"External service status {response.status_code}"
            )
            status_code = response.status_code
            if status_code in (http.HTTPStatus.BAD_GATEWAY, http.HTTPStatus.SERVICE_UNAVAILABLE):
                raise exceptions.ExternalServiceUnavailableError()
            elif status_code == http.HTTPStatus.INTERNAL_SERVER_ERROR:
                raise exceptions.ExternalServiceError()
            elif status_code == http.HTTPStatus.PAYMENT_REQUIRED:
                raise exceptions.InsufficientBalanceError()
            else:
                raise exceptions.ResponseError(response)

        invoice = sjson.JsonObject(response.json())
        ref_num = str(getattr(invoice, 'reference_number', 'FAWRY_REF'))
        self._payment_attempt_service.update_payment_attempt_status(payment_id=payment_attempt.id, status='SUCCESS', provider_reference=ref_num)
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
