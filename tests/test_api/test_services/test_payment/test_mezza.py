import unittest

from assertpy import assert_that

import api.services.requests_service as requests_service
import api.services.payment.mezza as mezza

import tests.doubles.requests as requests_doubles


SAMPLE_REQUEST = {
    'amount': 100,
    'currency': 'EGP',
    'country': 'EG',
    'payment_method_id': 'EW',
    'payment_method_flow': 'REDIRECT',
    'payer': {'name': 'Jane Doe'},
    'order_id': '123',
    'description': 'Tshirt',
    'notification_url': 'http://localhost/webhook',
    'callback_url': 'http://localhost/callback',
}


class TestMezzaPaymentService(unittest.TestCase):

    def setUp(self):
        self.request_sender = requests_doubles.RequestSenderDouble()
        self.service = mezza.MezzaPaymentService('lcl', self.request_sender)

    def test_service_uses_real_if_doubles_are_not_sent(self):
        service_without_doubles = mezza.MezzaPaymentService('lcl')
        assert_that(service_without_doubles._request_sender).is_instance_of(requests_service.RequestsWrapper)

    def test_create_payment_returns_pending_payment_with_expected_fields(self):
        payment = self.service.create_payment(SAMPLE_REQUEST)

        assert_that(payment.get('amount')).is_equal_to(100)
        assert_that(payment.get('currency')).is_equal_to('EGP')
        assert_that(payment.get('status')).is_equal_to('PENDING')
        assert_that(payment.get('status_code')).is_equal_to('100')
        assert_that(payment).contains_key('id', 'redirect_url', 'created_date')

    def test_create_payment_stores_payment(self):
        payment = self.service.create_payment(SAMPLE_REQUEST)

        assert_that(self.service.get_payment(payment['id'])).is_equal_to(payment)

    def test_get_payment_returns_none_for_unknown_id(self):
        assert_that(self.service.get_payment('does-not-exist')).is_none()

    def test_mark_paid_updates_status_fields(self):
        payment = self.service.create_payment(SAMPLE_REQUEST)

        updated = self.service.mark_paid(payment['id'])

        assert_that(updated.get('status')).is_equal_to('PAID')
        assert_that(updated.get('status_code')).is_equal_to('200')

    def test_mark_paid_returns_none_for_unknown_id(self):
        assert_that(self.service.mark_paid('does-not-exist')).is_none()

    def test_mark_failed_updates_status_fields(self):
        payment = self.service.create_payment(SAMPLE_REQUEST)

        updated = self.service.mark_failed(payment['id'])

        assert_that(updated.get('status')).is_equal_to('FAILED')
        assert_that(updated.get('status_code')).is_equal_to('400')

    def test_mark_failed_returns_none_for_unknown_id(self):
        assert_that(self.service.mark_failed('does-not-exist')).is_none()

    def test_send_webhook_posts_payment_to_notification_url(self):
        payment = self.service.create_payment(SAMPLE_REQUEST)

        self.service.send_webhook(payment)

        self.request_sender.assert_that_request_is_called_with(
            method='POST',
            url='http://localhost/webhook',
            json=payment,
        )


if __name__ == '__main__':
    unittest.main()
