import unittest

from assertpy import assert_that

from app import app
from routes.payments_getaway import service


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


class TestCreatePaymentEndpoint(unittest.TestCase):
    def setUp(self):
        service._payments.clear()
        self.client = app.test_client()

    def test_post_payments_returns_201_with_pending_payment(self):
        response = self.client.post('/api/v1/payments', json=SAMPLE_REQUEST)

        assert_that(response.status_code).is_equal_to(201)
        data = response.get_json()
        assert_that(data.get('status')).is_equal_to('PENDING')
        assert_that(data).contains_key('id', 'redirect_url')


class TestGetPaymentEndpoint(unittest.TestCase):
    def setUp(self):
        service._payments.clear()
        self.client = app.test_client()
        self.payment = self.client.post('/api/v1/payments', json=SAMPLE_REQUEST).get_json()

    def test_get_payment_returns_200_with_stored_payment(self):
        response = self.client.get(f"/api/v1/payments/{self.payment['id']}")

        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.get_json().get('id')).is_equal_to(self.payment['id'])

    def test_get_payment_returns_404_for_unknown_id(self):
        response = self.client.get('/api/v1/payments/does-not-exist')

        assert_that(response.status_code).is_equal_to(404)


if __name__ == '__main__':
    unittest.main()
