from sqlalchemy.orm import Session

from api.services.crud import Crud
from models.customer import Customer 


class CustomerService:
    def __init__(self, session: Session, crud=None):
        self._crud = crud or Crud(Customer, session) 
    
    def create_customer(self, data):
        """
        Create a new customer record.
        :param data: Dictionary containing the data for the new customer.
        :return: The created customer record.
        """
        return self._crud.create(data)

    def get_customer_by_id(self, customer_id):
        """
        Retrieve a customer record by its ID.
        :param customer_id: The ID of the customer record to retrieve.
        :return: The customer record if found, else None.
        """
        return self._crud.read(customer_id)

    def get_all_customers(self):
        """
        Retrieve all customer records.
        :return: A list of all customer records.
        """
        return self._crud.get_all()
    