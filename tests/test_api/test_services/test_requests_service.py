import http
import unittest

from assertpy import assert_that

import api.core.exceptions as api_exceptions
import api.services.requests_service as api_requests

import tests.doubles.requests as requests_doubles


class TestGetService(unittest.TestCase):

    def test_returns_request_wrapper_when_env_is_lcl(self):
        wrapper = api_requests.get_service('lcl')
        assert_that(wrapper).is_instance_of(api_requests.WiremockRequester)

    def test_returns_request_wiremock_when_env_is_not_lcl(self):
        wiremock = api_requests.get_service('prd')
        assert_that(wiremock).is_instance_of(api_requests.RequestsWrapper)
    

class TestRequestWrapper(unittest.TestCase):
    
    def setUp(self):
        self.test_requests = requests_doubles.RequestSenderDouble()
        self.wrapper = api_requests.RequestsWrapper(self.test_requests)

    def test_request_calls_requests_with_expected_params(self):
        self.wrapper.request(method='GET',
            url='fake_url',
            data='fake_data',
            headers={'X-Test-Header': 'fake value'}
        )
        self.test_requests.assert_that_request_is_called_with(
            method='GET',
            url='fake_url',
            data='fake_data',
            timeout=5,
            headers={'X-Test-Header': 'fake value'}
        )

    def test_request_raise_response_error_if_response_is_not_ok(self):
        test_requests = requests_doubles.RequestSenderDouble(status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR)
        wrapper = api_requests.RequestsWrapper(test_requests)
        with self.assertRaises(api_exceptions.ResponseError) as exc:
            wrapper.request(method='GET', url='fake_url')
        assert_that(exc.exception.message).is_equal_to('Response error <500>')


class TestWiremockRequester(unittest.TestCase):

    def test_request_calls_requests_with_expected_params(self):
        self.test_requests = requests_doubles.RequestSenderDouble()
        wrapper = api_requests.WiremockRequester(self.test_requests)
        wrapper.request(method='GET', url='fake_url', data='fake_data', headers={'X-Test-Header': 'fake value'})
        self.test_requests.assert_that_request_is_called_with(
            method='GET',
            url='http://127.0.0.1:8080/fake_url',
            data='fake_data',
            timeout=5,
            headers={'X-Test-Header': 'fake value'}
        )


if __name__ == '__main__':
    unittest.main()
