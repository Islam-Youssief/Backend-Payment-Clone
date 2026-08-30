import http 

from api.services.payment_history import PaymentHistoryService
from api.core.serializers.payment_history_serializer import PaymentHistorySerializer


class PaymentHistoryController:

    def get_all(self):
        payments = PaymentHistoryService.get_all()   

        response = [PaymentHistorySerializer(payment).serialize() for payment in payments]

        return response, http.HTTPStatus.OK

    def get_by_id(self,payment_id):
        payment = PaymentHistoryService.get_by_id(payment_id)

        if payment is None:
            return {"message":"Payment was not found"}, http.HTTPStatus.NOT_FOUND

        respone = PaymentHistorySerializer(payment).serialize()
        return respone, http.HTTPStatus.OK

    def get_by_customer_id(self,customer_id):
        payments = PaymentHistoryService.get_by_customer(customer_id)

        if not payments:
          return {"message":"This customer doesn't have payments"}, http.HTTPStatus.NOT_FOUND
        
        response = [PaymentHistorySerializer(payment).serialize() for payment in payments]
        return response, http.HTTPStatus.OK