import api.services.payment_service as payment_service

class CheckoutWebhookService:
    def __init__(self, payment_service):
        self._payment_service = payment_service

    def process(self, payload):
        checkout_payment_id = payload["payment_id"]

        payment = self._payment_service.get_payment_by_checkout_payment_id(
            checkout_payment_id
        )

        return self._payment_service.update_payment(
            payment.id,
            {
                "status": payload["status"],
                "failure_reason": payload.get("failure_reason")
            }
        )