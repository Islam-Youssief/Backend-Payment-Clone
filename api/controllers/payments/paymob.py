import http
import logging
import api.services.payment.paymob_webhook as paymob_webhook
import api.services.idempotency as idempotency
import api.services.payment_history as payment_history

class PaymobWebhookController:
    def __init__(self,flask_request,verifier=None,idempotency_service=None,history_service=None):
        self._flask_request = flask_request
        self._verifier = verifier or paymob_webhook.PaymobHmacVerifier()
        self._idempotency_service = idempotency_service or idempotency.IdempotencyService()
        self._payment_history_service = history_service or payment_history.PaymentHistoryService()

    def handle_webhook(self):
        payload = self._flask_request.get_json(silent=True) or {}
        obj = payload.get('obj', {})
        received_hmac = self._flask_request.args.get('hmac')

        if not self._verifier.verify(obj,received_hmac):
            logging.error('Invalid signature for webhook request')
            return {'error': 'Invalid signature'}, http.HTTPStatus.UNAUTHORIZED

        key = str(obj.get('id'))
        existing = self._idempotency_service.get(key)
        if existing and existing.status == 'COMPLETED':
            logging.info('Already completed!!')
            return {"message": "Already completed"}, http.HTTPStatus.OK

        status = 'SUCCESS' if obj.get('success') else 'FAILED'
        self._payment_history_service.update_status_by_transaction_id(
                    str(obj.get('order', {}).get('id')),status,
        None if status == 'SUCCESS' else 'payment failed at provider',)
        self._idempotency_service.complete(key, http.HTTPStatus.OK, {'status': status})
        return {'message': 'ok'}, http.HTTPStatus.OK