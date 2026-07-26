import http
import logging

import api.controllers.base as base
import api.core.exceptions as exceptions
import api.services.payment_service as payment_service


class PaymentHistoryController:
    def __init__(self, flask_request, session, handler=None):
        self._flask_request = flask_request
        self._handler = handler or _PaymentHistoryHandler(session)
    
    @property
    def _body(self):
        return self._flask_request.json

    def _as_error_response(self, error, status):
        logging.error(f"Creating error response: {error} {status}")
        return base.CoreErrorSerializer(error, status).serialize(self._flask_request.path), status

    def get_payment(self, payment_id):
        """
        Retrieve a payment by its ID.

        :param payment_id: The ID of the payment.
        :return: A serialized payment response and HTTP status code.
        """
        try:
            payment = self._handler.get_payment_by_id(payment_id)
            return _PaymentHistorySerializer(payment).serialize(self._flask_request.path), http.HTTPStatus.OK
        except exceptions.RecordNotFoundError as e:
            return self._as_error_response(e, http.HTTPStatus.NOT_FOUND)
    
    def get_payments(self):
        """
        Retrieve all payment records.

        :return: A serialized list of payment records and an HTTP 200 OK status.
        """
        payments = self._handler.get_payments()
        return _PaymentHistorySerializer(payments).serialize_payments(self._flask_request.path), http.HTTPStatus.OK

    def get_customer_payments(self, customer_id):
        """
        Retrieve all payments for a specific customer.

        :param customer_id: The ID of the customer.
        :return: A serialized list of the customer's payment records and an HTTP 200 OK status.
        """
        customer_payments = self._handler.get_payments_by_customer_id(customer_id)
        return _PaymentHistorySerializer(customer_payments).serialize_payments(self._flask_request.path), http.HTTPStatus.OK



class _PaymentHistoryHandler:
    def __init__(self, session, service=None):
        self._service = service or payment_service.PaymentService(session)
    
    def get_payment_by_id(self ,payment_id):
        """
        Retrieve a payment by its ID.
        """
        return self._service.get_payment_by_id(payment_id)
    
    def get_payments(self):
        """
        Retrieve list of payments.
        """
        return self._service.get_all_payments()
    
    def get_payments_by_customer_id(self, customer_id):
        """
        Retrieve list of payments by customer ID.
        """
        return self._service.get_all_payments_by_customer_id(customer_id)
    
class _PaymentHistorySerializer:
    def __init__(self, payments):
        self._payments = payments

    def serialize(self, url):
        return {
            "url": url,
            "id": self._payments.id,
            "customer_id": self._payments.customer_id, 
            "idempotency_key": self._payments.idempotency_key,
            "checkout_payment_id": self._payments.checkout_payment_id,
            "status": self._payments.status,      
            "amount": self._payments.amount,
            "currency": self._payments.currency,
            "failure_reason": self._payments.failure_reason
        }

    def serialize_payments(self, url):
        return {
            "url": url,
            "payments": [
                _PaymentHistorySerializer(payment).serialize(url)
                for payment in self._payments
            ]
        }