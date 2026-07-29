import http
import logging
import uuid
import requests
import flask as fl
import sqlalchemy.exc as sa_exc

import api.controllers.base as base
import api.core.exceptions as exceptions
import api.core.serializers.json as sjson
import api.services.customer_service as customer_service
import api.services.payment_attempt_service as payment_attempt_service
import api.services.payment.validators as validators
import api.services.payment.fawry as fawry_service
import api.services.rate_limiter_service as rate_limiter_service

class FawryController:
    def __init__(self, flask_request, app_config, validator=None, handler=None, rate_limiter=None):
        self._flask_request = flask_request
        self._app_config = app_config
        self._validator = validator or validators.UserPaymentDataValidator()
        self._handler = handler or _FawryHandler(self._app_config)
        self._rate_limiter = rate_limiter or rate_limiter_service.RateLimiterService()
        self._serializer = _FawrySerializer()

    @property
    def _body(self):
        return self._flask_request.json
    
    @property
    def _token(self):
        return self._flask_request.headers.get('Authorization')

    @property
    def _idempotency_key(self):
        return self._flask_request.headers.get('X-Idempotency-Key')

    @property
    def _client_ip(self):
        return self._flask_request.remote_addr

    @property
    def _url(self):
        return self._flask_request.path

    def pay(self):
        try:
            self._rate_limiter.check_rate_limit(self._client_ip, self._url)
            self._validator.validate(self._body, self._token)
            invoice = self._handler.process_payment(self._body, self._idempotency_key)
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
        except sa_exc.IntegrityError as exc:
            return self._as_error_response(exceptions.ValidationError(str(exc)), http.HTTPStatus.UNPROCESSABLE_ENTITY)
        except exceptions.RateLimitExceededError as exc:
            return self._as_error_response(exc, http.HTTPStatus.TOO_MANY_REQUESTS)

    def _as_error_response(self, error, status):
        logging.error(f"Creating error response: {error} {status}")
        return base.CoreErrorSerializer(error, status).serialize(self._url), status

class _PaymentTracker:
    def __init__(self, customer_svc=None, payment_attempt_svc=None):
        self._customer_service = customer_svc or customer_service.CustomerService()
        self._payment_attempt_service = payment_attempt_svc or payment_attempt_service.PaymentAttemptService()

    def create_attempt(self, provider, customer_name, customer_email, amount, currency, idempotency_key):
        customer = self._customer_service.get_or_create_customer(name=customer_name, email=customer_email)
        return self._payment_attempt_service.create_payment_attempt(
            customer_id=customer.id,
            provider=provider,
            amount=amount,
            customer_name=customer.name,
            customer_email=customer.email,
            idempotency_key=idempotency_key,
            currency=currency,
            status='PENDING'
        )

    def update_status(self, payment_id, status, provider_reference=None, failure_reason=None):
        return self._payment_attempt_service.update_payment_attempt_status(
            payment_id=payment_id,
            status=status,
            provider_reference=provider_reference,
            failure_reason=failure_reason
        )

class _FawryHandler:
    def __init__(self, app_config, test_client=None, tracker=None):
        self._config = app_config
        self._client = test_client or fawry_service.FawryClient(self._config.env)
        self._tracker = tracker or _PaymentTracker()

    def process_payment(self, data, idempotency_key):
        customer_name = data.get('cardHolder')
        customer_email = data.get('customerEmail')
        amount = float(data.get('amount', 0.0))
        currency = data.get('currency', 'EGP')
        idem_key = uuid.UUID(str(idempotency_key))

        payment_attempt = self._tracker.create_attempt(
            provider='FAWRY',
            customer_name=customer_name,
            customer_email=customer_email,
            amount=amount,
            currency=currency,
            idempotency_key=idem_key
        )

        response = self._client.pay_with_card(data=data)
        if response.status_code != http.HTTPStatus.OK:
            self._tracker.update_status(
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
        self._tracker.update_status(payment_id=payment_attempt.id, status='SUCCESS', provider_reference=ref_num)
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
