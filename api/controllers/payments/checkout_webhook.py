import http
import logging

import api.controllers.base as base
import api.core.exceptions as exceptions
import api.core.serializers.json as sjson
import api.services.webhook_service as webhook_service

class CheckoutWebhookController:

    def __init__(self, flask_request, session, handler=None):
        self._flask_request = flask_request
        self._handler = handler or _CheckoutWebhookHandler(session)

    @property
    def _body(self):
        return self._flask_request.json

    def process(self):
        try:
            invoice = self._handler.process(self._body)
            serializer = _CheckoutWebhookSerializer(invoice)
            return serializer.serialize(self._flask_request.path), invoice.http_status
        except exceptions.CoreException as e:
            return self._as_error_response(e, e.status_code)
        except Exception as e:
            logging.exception("Unexpected error processing webhook")
            return self._as_error_response(e, http.HTTPStatus.INTERNAL_SERVER_ERROR)

    def _as_error_response(self, error, status):
        logging.error(f"Creating error response: {error} {status}")
        return base.CoreErrorSerializer(error, status).serialize(self._flask_request.path), status

class _CheckoutWebhookHandler:
    def __init__(self, session, service=None):
        self._service = service or webhook_service.CheckoutWebhookService(
            payment_service.PaymentService(session)
        )

    def process(self, payload):
        return self._service.process(payload)

class _CheckoutWebhookSerializer:

    def __init__(self, payment):
        self._payment = payment

    def serialize(self, url):
        return {
            "url": url,
            "message": "Webhook: payment processed successfully",
            "status": self._payment.status,       
            "amount": self._payment.amount,
            "payment_id": self._payment.checkout_payment_id,
            "product_id": self._payment.product_id,
        }
