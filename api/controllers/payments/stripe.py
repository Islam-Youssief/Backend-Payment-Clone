import http
import logging
import uuid

import api.controllers.base as base
import api.core.exceptions as exceptions
import api.core.serializers.json as sjson
import api.services.payment.validators as validators
import api.services.payment.stripe as stripe_service
import api.services.payment.crud as payment_crud
from  api.tasks.email import send_receipt_email
from  api.tasks.webhook import send_webhook


class StripeController:

    def __init__(self, flask_request, config, validator=None, handler=None ):
        self._flask_request = flask_request
        self._config = config
        self._validator = validator or validators.UserPaymentDataValidator()
        self._handler = handler or _PaymentHandler(self._config)

    @property
    def _body(self):
        return self._flask_request.json

    def pay(self):
        try:
            self._validator.validate(self._body)
            invoice = self._handler.pay(data=self._body,
                authorization=self._flask_request.headers.get("Authorization")
            )
            return _StripeSerializer(invoice).serialize(self._flask_request.path), invoice.http_status
        except (exceptions.RequiredInputError,exceptions.InvalidInputError)as exc:
            return self._as_error_response(exc, http.HTTPStatus.BAD_REQUEST)

    def _as_error_response(self, error, status):
        logging.error(f"Creating error response: {error} {status}")
        return base.CoreErrorSerializer(error, status).serialize(self._flask_request.path), status


class _PaymentHandler:

    def __init__(self, config, test_client=None, crud=None):
        self._config = config
        self._client = test_client or stripe_service.StripeClient(config.env)
        self._crud = crud or payment_crud.PaymentCrud()

    def pay(self, data, authorization):
        idempotency_key = data.get("idempotency_key")

        if idempotency_key:
            existing = self._crud.get_by_idempotency_key(idempotency_key)

            if existing:
                invoice = sjson.JsonObject({
                    "status": existing.status,
                    "message": "payment already exists",
                    "transaction_id": existing.provider_reference,
                    "amount": existing.amount,
                    "currency": existing.currency,
                    "payment_method": existing.provider,
                })
                invoice.http_status = http.HTTPStatus.OK
                return invoice

        response = self._client.create_payment_intent(
            data=data,
            authorization=authorization
        )
        print(response.status_code)
        print(response.headers)
        print(response.text)
        invoice = sjson.JsonObject(response.json())

        if invoice.status == "success":
            invoice.http_status = http.HTTPStatus.CREATED

            self._crud.create({
                "idempotency_key": invoice.idempotency_key or str(uuid.uuid7()),
                "customer_id": invoice.customer_id,
                "provider": "stripe",
                "provider_reference": invoice.transaction_id,
                "amount": invoice.amount,
                "currency": invoice.currency,
                "status": invoice.status,
                "failure_reason": None,
            })
            payment_data = {
                "payment_id": invoice.transaction_id,
                "amount": invoice.amount,
                "currency": invoice.currency,
                "customer_id": invoice.customer_id,
            }
            send_webhook.delay(payment_data)
            if data.get("email"):
                send_receipt_email.delay(
                    data["email"],
                    invoice.transaction_id,
                    invoice.amount
                )


        elif invoice.status == "declined":
            invoice.http_status = http.HTTPStatus.PAYMENT_REQUIRED

        elif invoice.status == "server_error":
            invoice.http_status = http.HTTPStatus.INTERNAL_SERVER_ERROR

        elif invoice.status == "rate_limited":
            invoice.http_status = http.HTTPStatus.TOO_MANY_REQUESTS

        elif invoice.status in (
                "unauthorized",
                "invalid_secret",
                "invalid_token",
                "expired_token",    
        ):
            invoice.http_status = http.HTTPStatus.UNAUTHORIZED
           

        return invoice
class _StripeSerializer:

    def __init__(self,invoice):
        self._invoice = invoice

    def serialize(self, url):
        return {
            "url": url,
            "message": self._invoice.message,
            "status": self._invoice.status,
            "transaction_id": getattr(self._invoice, "transaction_id", None),
            "amount": getattr(self._invoice, "amount", None),
            "currency": getattr(self._invoice, "currency", None),
            "payment_method": getattr(self._invoice, "payment_method", None),
        }

