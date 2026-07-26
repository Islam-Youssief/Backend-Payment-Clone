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

     