import time
import uuid

import api.services.requests_service as requests_service


class MezzaPaymentService:
    def __init__(self, env, test_request_sender=None):
        self._env = env
        self._request_sender = test_request_sender or requests_service.get_service(self._env)
        self._payments = {}

    def create_payment(self, data):
        payment_id = f'R-{uuid.uuid4()}'
        payment = {
            'id': payment_id,
            'amount': data['amount'],
            'currency': data['currency'],
            'country': data['country'],
            'payment_method_id': data['payment_method_id'],
            'payment_method_type': 'BANK_TRANSFER',
            'payment_method_flow': data['payment_method_flow'],
            'order_id': data['order_id'],
            'description': data['description'],
            'payer': data['payer'],
            'notification_url': data['notification_url'],
            'callback_url': data['callback_url'],
            'created_date': time.strftime('%Y-%m-%dT%H:%M:%S.000+0000'),
            'status': 'PENDING',
            'status_detail': 'The payment is pending.',
            'status_code': '100',
            'redirect_url': f'http://127.0.0.1:5000/mock/pay/{payment_id}',
        }
        self._payments[payment_id] = payment
        return payment

    def get_payment(self, payment_id):
        return self._payments.get(payment_id)

    def mark_paid(self, payment_id):
        payment = self._payments.get(payment_id)
        if payment:
            payment['status'] = 'PAID'
            payment['status_code'] = '200'
            payment['status_detail'] = 'The payment was paid.'
        return payment

    def mark_failed(self, payment_id):
        payment = self._payments.get(payment_id)
        if payment:
            payment['status'] = 'FAILED'
            payment['status_code'] = '400'
            payment['status_detail'] = 'Payment failed.'
        return payment

    def send_webhook(self, payment):
        try:
            self._request_sender.request(method='POST', url=payment['notification_url'], json=payment)
        except Exception:
            pass  # ponytail: best-effort webhook; merchant outage must not fail the gateway

    def async_finalize(self, payment_id):
        time.sleep(5)
        payment = self.mark_paid(payment_id)
        if payment:
            self.send_webhook(payment)
