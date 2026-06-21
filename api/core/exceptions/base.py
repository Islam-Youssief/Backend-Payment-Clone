"""
This module provides base classes for most common types of exceptions. Applications should provide their own exception
classes by deriving from the most concrete exception provided by this module.

..  code-block:: python

    import api.core.exceptions as exc

    class CustomError(exc.SerializableError):
        def __init__(self, custom_parameter, message=None):
            super().__init__(message or f'Custom message for {custom_parameter}')
            self.custom_parameter = custom_parameter

        def _add_data(self, serialized):
            serialized.update(custom_parameter=self.custom_parameter)

"""

import json
import traceback

import api.core.serializers.json as sj


class SerializableError(Exception, sj.Serializable):
    """
    Base class for all the exceptions. Every exception class provided in applications and libraries must, ultimately,
    derived from this class, but best practices recommend to derived from a more concrete exception type.
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    @property
    def data(self):
        """
        Returns a dictionary representation of the custom data in the exception.
        This class does not represent any custom data, but derived classes can
        override ``_add_data()`` to provide additional
        data.
        """
        data = {}
        self._add_data(data)
        return data

    def __str__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        """
        Overrides the Serializable interface to inject the message property.

        :return:
            A dictionary representation of the exception.
        :rtype:
            dict
        """
        serialized = super().to_dict()
        serialized.update(message=self.message)
        return serialized


class InvalidInputError(SerializableError):
    """
    Exception representing an input error. The exception is initialized with the name of the attribute, property, or
    parameter with the invalid value, and the invalid value that caused the exception.

    :param str pname:
        Name of the attribute, property, or parameter for which an invalid value was specified.
    :param any value:
        Invalid value specified that caused the exception.
    """

    def __init__(self, pname, invalid_value, message=None):
        super().__init__(message or f"Invalid value <{invalid_value}> for <{pname}>")
        self.name = pname
        self.value = invalid_value

    def _add_data(self, serialized):
        serialized.update(name=self.name, value=self.value)


class RequiredInputError(SerializableError):
    """
    Exception representing and error from a required attribute, property, or parameter missing from the input.

    :param str pname:
        Name of the required attribute, property, or parameter that is missing from the input.
    """

    def __init__(self, pname, message=None):
        super().__init__(message or f"Input <{pname}> is required")
        self.name = pname

    def _add_data(self, serialized):
        serialized.update(name=self.name)


class ResponseError(SerializableError):
    """
    This exception should be raised to represent an HTTP error when calling another service. The exception wraps a
    response object and exposes the ``status_code`` and contents of the response as the exception information.

    When the response object contains JSON as the body, the exception will expose the ``JsonObject`` as the info
    attribute. Responses that don't contain JSON are converted using the text as the value of the ``body`` property
    of the ``JsonObject``.

    :param Response response:
        Response that indicates an error from a service request.
    :param str message:
        Optional message to describe the exception.

    The following example shows how to use this exception:

    ..  code-block:: python

        import requests
        import api.core.exceptions as exc

        url = 'https://third.part.url/api'
        response = request.get(url)
        if response.status_code != 200
            raise exc.ResponseError(response)

    The application can raise the exception to indicate the error response and insure the data from the response is
    maintained.
    """

    def __init__(self, response, message=None):
        super().__init__(message or f"Response error <{response.status_code}>")
        self.status_code = response.status_code
        self.info = self._extract_info(response)

    def _extract_info(self, response):
        try:
            return sj.JsonObject(response.json())
        except json.JSONDecodeError:
            return sj.JsonObject(self._make_dict(response.text))

    def _add_data(self, serialized):
        serialized.update(status_code=self.status_code)
        serialized.update(self.info.to_dict())

    def _make_dict(self, text):
        return {"body": text or "no body"}


class UnknownError(SerializableError):
    """
    This exception wraps another exception when an unknown error is raised. It allows exceptions caused by other
    libraries for unknown reasons to be wrapped into the Serializable interface. The exception provides the original
    traceback as part of the data.

    :param Exception original_exception:
        The original exception raised.
    """

    def __init__(self, original_exception, message=None):
        super().__init__(message or str(original_exception))
        self.original_exception = original_exception

    def _add_data(self, serialized):
        tb = traceback.format_exception(
            type(self.original_exception), self.original_exception, self.original_exception.__traceback__
        )
        serialized.update(traceback=tb)


class CrudOperationError(SerializableError):
    """
    Exception representing any error that could happen on run time during a CRUD operation.

    :param str operation_name:
        Name of the operation that failed.
    """

    def __init__(self, message, operation_name):
        super().__init__(message)
        self.operation_name = operation_name

    def _add_data(self, serialized):
        serialized.update(operation_name=self.operation_name)


class NotImplementedError(SerializableError):
    """
    Exception representing ant not implemented functionality

    :param str message:
        Message describing the error.
    :param str missing:
        Name of the function/class that is not implemented.
    """

    def __init__(self, message="Not Implemented", missing=""):
        super().__init__(message)
        self.missing = missing

    def _add_data(self, serialized):
        serialized.update(missing=self.missing)


class RecordNotFoundError(SerializableError):
    """
    Exception representing an error from a record not found in the database.

    :param str record_id:
        Id of the record that was not found.
    """

    def __init__(self, message, record_id=''):
        super().__init__(message)
        self.record_id = record_id

    def _add_data(self, serialized):
        serialized.update(record_id=self.record_id)


class InputDataTypeError(SerializableError):
    """
    Exception raised when a field has an invalid data type.

    :param str field: The name of the field.
    :param str expected_type: The expected data type of the field.
    """

    def __init__(self, field=None, expected_type=None, message=None):
        super().__init__(message or f"Field '{field}' should be of type '{expected_type}'.")
        self.field = field
        self.expected_type = expected_type

    def _add_data(self, serialized):
        serialized.update(field=self.field, expected_type=self.expected_type)


class UnauthorizedAccessError(SerializableError):
    """
    Exception representing unauthorized error when trying to access an api with invalid or missing authentication token.

    :param str message: error message explains the error
    """

    def __init__(self, message="Unauthorized access. Please provide valid authentication credentials."):
        super().__init__(message)


class ForbiddenAccessError(SerializableError):
    """
    Exception representing a forbidden Access error when trying to access an api with insufficient permissions.

    :param str message: error message explains the error
    """

    def __init__(self, message="Access denied. You do not have sufficient permissions to perform this action."):
        super().__init__(message)


class ValidationError(SerializableError):
    """
    Exception raised when a validation error occurs.
    """

    def __init__(self, message='Validation error'):
        super().__init__(message)


class SecurityError(SerializableError):
    """
    Exception raised when security validation fails (e.g., virus detected in file upload).

    :param str message: Error message describing the security issue
    :param **data: Additional data about the security error
    """

    def __init__(self, message="Security validation failed", **data):
        super().__init__(message)
        self._data = data

    def _add_data(self, serialized):
        serialized.update(self._data)


class ExternalServiceError(SerializableError):
    """
    Exception raised when an external service is unavailable or returns an error.

    :param str message: Error message describing the issue
    :param str service: Name of the external service
    :param **data: Additional data about the error
    """

    def __init__(self, message="External service error", service="", **data):
        super().__init__(message)
        self.service = service
        self._data = data

    def _add_data(self, serialized):
        serialized.update(service=self.service)
        serialized.update(self._data)


class ExternalServiceUnavailableError(SerializableError):
    """
    Exception raised when an external service is unavailable or cannot be reached.

    :param str message: Error message describing the issue
    :param str service: Name of the external service
    :param **data: Additional data about the error
    """

    def __init__(self, message="External service unavailable", service="", **data):
        super().__init__(message)
        self.service = service
        self._data = data

    def _add_data(self, serialized):
        serialized.update(service=self.service)
        serialized.update(self._data)


class EmptyRecordsError(SerializableError):
    """
    Exception representing an error when a query returns no records.
    """

    def __init__(self, message='No records found'):
        super().__init__(message)


class ConflictError(SerializableError):
    """
    Exception representing a conflict with the current state of a resource
    (e.g., a duplicate that violates a uniqueness constraint). Maps to HTTP 409.
    """

    def __init__(self, message='Resource conflict'):
        super().__init__(message)


class MaximumLengthError(SerializableError):
    """
    Exception representing an error when an input exceeds its maximum allowed length.

    :param str pname:
        Name of the attribute, property, or parameter that exceeded the limit.
    :param int max_length:
        The maximum allowed length.
    """

    def __init__(self, pname=None, max_length=None, message=None):
        super().__init__(message or f"Input <{pname}> exceeds maximum length of {max_length}")
        self.name = pname
        self.max_length = max_length

    def _add_data(self, serialized):
        serialized.update(name=self.name, max_length=self.max_length)
