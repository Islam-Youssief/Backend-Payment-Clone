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


class UnauthorizedAccessError(SerializableError):
    """
    Exception representing unauthorized error when trying to access an api with invalid or missing authentication token.

    :param str message: error message explains the error
    """

    def __init__(self, message="Unauthorized access. Please provide valid authentication credentials."):
        super().__init__(message)


class ConflictError(SerializableError):
    """
    Exception representing a conflict error when trying to create a resource that already exists.

    :param str pname: Name of the attribute, property, or parameter that conflicts.
    :param any value: The conflicting value.
    :param str message: Optional message describing the conflict.
    """

    def __init__(self, pname, conflicting_value, message=None):
        super().__init__(message or f"Resource conflict for <{pname}>: <{conflicting_value}> already exists")
        self.name = pname
        self.value = conflicting_value

    def _add_data(self, serialized):
        serialized.update(name=self.name, value=self.value)


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



# TODO: Add more specific validation error types as needed.
class ValidationError(SerializableError):
    """
    Exception raised when a validation error occurs.
    """

    def __init__(self, message='Validation error'):
        super().__init__(message)


class ExternalServiceUnavailableError(SerializableError):
    """
    Exception representing an error when an external service is unavailable.
    """

    def __init__(self, message="External service unavailable"):
        super().__init__(message)


class ExternalServiceError(SerializableError):
    """
    Exception representing an error when an external service returns an error.
    """

    def __init__(self, message="External service error"):
        super().__init__(message)


class InsufficientBalanceError(SerializableError):
    """
    Exception representing an error when the balance is insufficient.
    """
    def __init__(self, message="Insufficient Balance"):
        super().__init__(message)


class RateLimitExceededError(SerializableError):
    """
    Exception raised when a client exceeds the allowed number of requests
    within the configured time window.
    """
    def __init__(self, message="Rate limit exceeded. Try again later."):
        super().__init__(message)

