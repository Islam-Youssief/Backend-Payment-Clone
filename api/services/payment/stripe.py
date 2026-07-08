import api.core.configurations as configurations
import api.services.requests_service as requests_service
import api.services.payment.validators as validators


STRIPE_PAYMENT_INTENTS_URL = "https://api.stripe.com/v1/payments_intents"


class StripeClient:
    def __init__(self,env,test_request_sender=None):
        self._env = env
        self._request_sender = test_request_sender or requests_service.get_service(self._env)
        self._validator = validators.UserPaymentDataValidator()

    @property
    def _headers(self):
         return {
            "Authorization": f"Bearer {configurations.PaymentsConfig().stripe_secret_key}"
        }

    def create_payment_intent(self,data):
        self._validator.validate(data)
        response = self._request_sender.request(
             method="POST",
             url=STRIPE_PAYMENT_INTENTS_URL,
             json=data,
             headers=self._headers
        )
        return response

