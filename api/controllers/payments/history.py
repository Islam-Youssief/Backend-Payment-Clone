import http
import logging
import uuid

import api.controllers.base as base
import api.core.exceptions as exceptions
import api.services.payment_attempt_service as payment_attempt_service


class CustomerPaymentDataValidator:
    """Validator for customer payment history input parameters."""

    def validate(self, customer_id: str) -> bool:
        if not customer_id:
            raise exceptions.RequiredInputError('customer_id')
        try:
            uuid.UUID(str(customer_id))
        except ValueError:
            raise exceptions.InvalidInputError('customer_id', customer_id, 'customer_id must be a valid UUID')
        return True


class SinglePaymentDataValidator:
    """Validator for single payment detail input parameters."""

    def validate(self, payment_id: str) -> bool:
        if not payment_id:
            raise exceptions.RequiredInputError('payment_id')
        try:
            uuid.UUID(str(payment_id))
        except ValueError:
            raise exceptions.InvalidInputError('payment_id', payment_id, 'payment_id must be a valid UUID')
        return True


class CustomerPaymentsController:
    def __init__(self, flask_request, validator=None, handler=None, serializer=None):
        self._flask_request = flask_request
        self._validator = validator or CustomerPaymentDataValidator()
        self._handler = handler or _PaymentHistoryHandler()
        self._serializer = serializer or _PaymentAttemptSerializer()

    @property
    def _url(self):
        return self._flask_request.path

    def get(self, customer_id: str):
        try:
            self._validator.validate(customer_id)
            attempts = self._handler.get_customer_payments(customer_id)
            return self._serializer.serialize_customer_payments(customer_id, attempts), http.HTTPStatus.OK
        except (exceptions.RequiredInputError, exceptions.InvalidInputError) as exc:
            return self._as_error_response(exc, http.HTTPStatus.BAD_REQUEST)
        except exceptions.RecordNotFoundError as exc:
            return self._as_error_response(exc, http.HTTPStatus.NOT_FOUND)

    def _as_error_response(self, error, status):
        logging.error(f"Creating error response: {error} {status}")
        return base.CoreErrorSerializer(error, status).serialize(self._url), status


class SinglePaymentController:
    def __init__(self, flask_request, validator=None, handler=None, serializer=None):
        self._flask_request = flask_request
        self._validator = validator or SinglePaymentDataValidator()
        self._handler = handler or _PaymentHistoryHandler()
        self._serializer = serializer or _PaymentAttemptSerializer()

    @property
    def _url(self):
        return self._flask_request.path

    def get(self, payment_id: str):
        try:
            self._validator.validate(payment_id)
            attempt = self._handler.get_payment_detail(payment_id)
            return self._serializer.serialize(attempt), http.HTTPStatus.OK
        except (exceptions.RequiredInputError, exceptions.InvalidInputError) as exc:
            return self._as_error_response(exc, http.HTTPStatus.BAD_REQUEST)
        except exceptions.RecordNotFoundError as exc:
            return self._as_error_response(exc, http.HTTPStatus.NOT_FOUND)

    def _as_error_response(self, error, status):
        logging.error(f"Creating error response: {error} {status}")
        return base.CoreErrorSerializer(error, status).serialize(self._url), status


class _PaymentHistoryHandler:
    def __init__(self, payment_attempt_svc=None):
        self._payment_attempt_service = payment_attempt_svc or payment_attempt_service.PaymentAttemptService()

    def get_customer_payments(self, customer_id: str):
        cust_uuid = uuid.UUID(str(customer_id))
        return self._payment_attempt_service.get_payment_attempts_by_customer_id(cust_uuid)

    def get_payment_detail(self, payment_id: str):
        pay_uuid = uuid.UUID(str(payment_id))
        attempt = self._payment_attempt_service.get_payment_attempt_by_id(pay_uuid)
        if not attempt:
            raise exceptions.RecordNotFoundError(f"Payment attempt <{payment_id}> not found", record_id=str(payment_id))
        return attempt


class _PaymentAttemptSerializer:
    def serialize(self, attempt):
        return {
            "id": str(attempt.id),
            "customer_id": str(attempt.customer_id) if attempt.customer_id is not None else None,
            "customer_name": attempt.customer_name,
            "customer_email": attempt.customer_email,
            "provider": attempt.provider,
            "provider_reference": attempt.provider_reference,
            "idempotency_key": str(attempt.idempotency_key),
            "amount": attempt.amount,
            "currency": attempt.currency,
            "status": attempt.status,
            "failure_reason": attempt.failure_reason,
            "created_at": attempt.created_at.isoformat()
        }

    def serialize_customer_payments(self, customer_id: str, attempts):
        return {
            "customer_id": str(customer_id),
            "payments": [self.serialize(att) for att in attempts]
        }
