from typing import Optional
from uuid import UUID
from api.models import db
from api.models.customer import Customer


class CustomerService:

    def create_customer(self, name: str, email: str) -> Customer:
        """Create and persist a new Customer record."""
        customer = Customer(name=name, email=email)
        db.session.add(customer)
        db.session.commit()
        return customer

    def get_customer_by_id(self, customer_id: UUID) -> Optional[Customer]:
        """Fetch a Customer by primary key UUID."""
        return db.session.get(Customer, customer_id)

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Fetch a Customer by email address."""
        return Customer.query.filter_by(email=email).first()

    def get_or_create_customer(self, name: str, email: str) -> Customer:
        """Fetch an existing Customer by email or create a new one if not found."""
        customer = self.get_customer_by_email(email)
        if not customer:
            customer = self.create_customer(name=name, email=email)
        return customer

    def update_customer(self, customer_id: UUID, name: Optional[str] = None, email: Optional[str] = None) -> Optional[Customer]:
        """Update Customer fields."""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return None
        if name is not None:
            customer.name = name
        if email is not None:
            customer.email = email
        db.session.commit()
        return customer

    def delete_customer(self, customer_id: UUID) -> bool:
        """Delete a Customer record by ID."""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return False
        db.session.delete(customer)
        db.session.commit()
        return True
