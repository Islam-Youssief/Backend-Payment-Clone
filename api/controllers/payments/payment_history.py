import http
import logging

import api.controllers.base as base
import api.services.payment.payment_history as payment_history
import api.core.exceptions as exceptions


class PaymentsHistoryController:
    def __init__(self, flask_request, config, handler=None):
        self._flask_request = flask_request
        self._config = config
        self._handler = handler or _PaymentHistoryHandler(self._config)

    @property
    def _body(self):
        return self._flask_request.json

    def get_payment(self, payment_id):
        try:
            payment = self._handler.get_payment(payment_id)
            return (
                _PaymentSerializer(payment).serialize(
                    self._flask_request.path
                ),
                http.HTTPStatus.OK,
            )
        except exceptions.RecordNotFoundError as exc:
            return self._as_error_response(
                exc,
                http.HTTPStatus.NOT_FOUND
            )

    def get_customer_payments(self, customer_id):
        try:
            payments = self._handler.get_customer_payments(
                customer_id
            )
            return (
                _PaymentHistorySerializer(payments).serialize(
                    self._flask_request.path
                ),
                http.HTTPStatus.OK,
            )
        except exceptions.RecordNotFoundError as exc:
            return self._as_error_response(
                exc,
                http.HTTPStatus.NOT_FOUND
            )

    def _as_error_response(self, error, status):
        logging.error(f"Creating error response: {error}")
        return (
            base.CoreErrorSerializer(error, status).serialize(self._flask_request.path),
            status
        )


class _PaymentHistoryHandler:
    def __init__(self, config, service=None):
        self._config = config
        self._service = service or payment_history.PaymentsHistoryService()

    def get_payment(self, payment_id):
        return  self._service.get_payment(payment_id)

    def get_customer_payments(self, customer_id):
        return self._service.get_customer_payments(customer_id)


class _PaymentSerializer:

    def __init__(self, payment):
        self._payment = payment

    def serialize(self, url):
        return {
            "url": url,
            "id": self._payment.id,
            "idempotency_key": self._payment.idempotency_key,
            "customer_id": self._payment.customer.id,
            "provider": self._payment.provider,
            "provider_reference": self._payment.provider_reference,
            "amount": float(self._payment.amount),
            "currency": self._payment.currency,
            "status": self._payment.status,
            "failure_reason": self._payment.failure_reason,
            "created_at": self._payment.created_at,
        }


class _PaymentHistorySerializer:

    def __init__(self, payments):
        self._payments = payments

    def serialize(self, url):
        return {
            "url": url,
            "payments":[
                _PaymentSerializer(payment).serialize(url)
                for payment in self._payments
            ]
        }



