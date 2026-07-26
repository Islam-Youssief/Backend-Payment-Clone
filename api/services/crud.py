import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class Crud:

    def __init__(self, model , session: Session):
        self.model = model
        self.session = session

    def _get_record(self, record_id):
        """
        Helper method to retrieve a record by its ID.
        Raises ValueError if the record is not found.
        """
        record = self.session.get(self.model, record_id)
        if record is None:
            raise ValueError(
                f"{self.model.__name__} with id {record_id} not found"
            )
        return record
    
    def create(self, data):
        """
        Create a new record in the database.
        :param data: Dictionary containing the data for the new record.
        :return: The created record.
        :raises SQLAlchemyError: If there is an error during the database operation.
        """
        try:
            record = self.model(**data)
            self.session.add(record)
            self.session.commit()
            return record
        except SQLAlchemyError as e:
            self.session.rollback()
            logging.exception("Error creating record")
            raise
    
    def read(self, record_id):
        """
        Retrieve a record by its ID.
        :param record_id: The ID of the record to retrieve.
        :return: The retrieved record.
        :raises ValueError: If the record is not found.
        """
        return self._get_record(record_id)

    def get_all(self):
        """
        Retrieve all records of the model.
        :return: A list of all records.
        """
        return self.session.query(self.model).all()
    
    def get_all_by_field(self, field_name, value):
        """
        Retrieve all records where a specific field matches a given value.
        :param field_name: The name of the field to filter by.
        :param value: The value to match in the specified field.
        :return: A list of matching records.
        """
        field = getattr(self.model, field_name)
        if field is None:
            raise ValueError(f"Field '{field_name}' does not exist in {self.model.__name__}")
        return self.session.query(self.model).filter(field == value).all()

     