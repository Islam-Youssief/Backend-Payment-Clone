import api.core.exceptions as exceptions
import api.services.payment.crud as payment_crud


class PaymentsHistoryService:

    def __init__(self, crud=None):
        self._crud = crud or payment_crud.PaymentCrud()

    def get_payment(self, payment_id):
        payment = self._crud.get(payment_id)

        if payment is None:
            raise exceptions.RecordNotFoundError(
                f"Payment  {payment_id} was not found."
            )
        return payment

    def get_customer_payments(self, customer_id):
        payments = self._crud.list_by_customer(customer_id)

        if payments is None:
            raise exceptions.RecordNotFoundError(
                f"No Payments found for customer {customer_id}."
            )
        return payments

