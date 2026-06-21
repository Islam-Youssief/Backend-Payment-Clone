from assertpy import assert_that


class RequestSenderDouble:
    def __init__(self, status_code=200, text='', json=None):
        self.status_code = status_code
        self.text = text
        self._returned_json = json or {}
        self._method = None
        self._url = None
        self._kwargs = None

    def request(self, method, url, **kwargs):
        self._method = method
        self._url = url
        self._kwargs = kwargs
        return self

    def json(self):
        return self._returned_json

    def assert_that_request_is_called_with(self, method, url, **kwargs):
        assert_that(self._method).is_equal_to(method)
        assert_that(self._url).is_equal_to(url)
        assert_that(self._kwargs).is_equal_to(kwargs)
