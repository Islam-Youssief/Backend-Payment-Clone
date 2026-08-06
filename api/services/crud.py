from sqlalchemy.orm import Session

import api.core.exceptions as exceptions


class Crud:

    def __init__(self, model , session: Session):
        self.model = model
        self.session = session

    def _get_record(self, record_id):
        """
        Helper method to retrieve a record by its ID.
        Raises RecordNotFoundError: If the record is not found.
        """
        record = self.session.get(self.model, record_id)
        if record is None:
            raise exceptions.RecordNotFoundError(
                f"{self.model.__name__} with id {record_id} not found"
            )
        return record
    
    def create(self, data):
        """
        Create a new record in the database.
        :param data: Dictionary containing the data for the new record.
        :return: The created record.
        """
        record = self.model(**data)
        self.session.add(record)
        self.session.commit()
        return record
    
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
        field = getattr(self.model, field_name, None)
        if field is None:
            raise ValueError(f"Field '{field_name}' does not exist in {self.model.__name__}")
        return self.session.query(self.model).filter(field == value).all()

    def update(self, record_id, data):
        """
        Update an existing record in the database.
        :param record_id: The ID of the record to update.
        :param data: Dictionary containing the updated data for the record.
        :return: The updated record.
        :raises ValueError: If the record is not found.
        """
        record = self._get_record(record_id)
        for key, value in data.items():
            setattr(record, key, value)
        self.session.commit()
        return record

    def get_all_by_field(self, field_name, value):
        """
        Retrieve all records where a specific field matches a given value.
        :param field_name: The name of the field to filter by.
        :param value: The value to match in the specified field.
        :return: A list of matching records.
        """
        field = getattr(self.model, field_name, None)
        if field is None:
            raise ValueError(f"Field '{field_name}' does not exist in {self.model.__name__}")
        return self.session.query(self.model).filter(field == value).all()