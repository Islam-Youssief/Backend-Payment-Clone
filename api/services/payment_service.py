from sqlalchemy.orm import Session

from api.services.crud import Crud
from models.payment_history import PaymentHistory

class PaymentService:
    def __init__(self, session: Session, crud=None):
        self._crud = crud or Crud(PaymentHistory, session) 
    
    def create_payment(self, data):
        """
        Create a new payment record.
        :param data: Dictionary containing the data for the new payment.
        :return: The created payment record.
        """
        return self._crud.create(data)
    
    def get_payment_by_id(self, payment_id):
        """
        Retrieve a payment record by its ID.
        :param payment_id: The ID of the payment record to retrieve.
        :return: The payment record if found, else None.
        """
        return self._crud.read(payment_id)

    def get_all_payments(self):
        """
        Retrieve all payment records.
        :return: A list of all payment records.
        """
        return self._crud.get_all()

    def get_all_payments_by_customer_id(self, customer_id):
        """
        Retrieve all payment records for a specific customer.
        :param customer_id: The ID of the customer whose payments to retrieve.
        :return: A list of payment records for the specified customer.
        """
        return self._crud.get_all_by_field('customer_id', customer_id)