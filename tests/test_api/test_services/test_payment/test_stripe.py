import unittest
import os

from assertpy import assert_that

import api.services.requests_service as requests_service
import api.services.payment.stripe as stripe
import tests.doubles.requests as requests_doubles


class TestStripeClient(unittest.TestCase):

    def setUp(self):
        os.environ['STRIPE_SECRET_KEY'] = 'fake_secret_key'
        self.request_sender = requests_doubles.RequestSenderDouble(json={'id': 'pi_fake_123'})
        self.client = stripe.StripeClient('lcl',self.request_sender)

    def test_client_uses_real_if_doubles_are_not_sent(self):
        client_without_doubles = stripe.StripeClient(env="lcl")
        assert_that(client_without_doubles._request_sender).is_instance_of(requests_service.WiremockRequester)

    def test_create_payment_intents_calls_stripe_correctly(self):
        data = {
            "cardHolder": "TESTER TESTING PAYMENT",
            "amount": 100,
            "cardNumber":"4242424242424242",
            "cvv":"123"
        }
        response = self.client.create_payment_intent(
            data=data,
            authorization="Bearer STRIPE_SECRET_KEY"
        )
        assert_that(response.json().get('id')).is_equal_to('pi_fake_123')

        self.request_sender.assert_that_request_is_called_with(
              method="POST",
              url=stripe.STRIPE_PAYMENT_INTENTS_URL,
              json=data,
              headers={
                   "Authorization":"Bearer STRIPE_SECRET_KEY"
              }
         )
          
if __name__ == '__main__':
    unittest.main()
