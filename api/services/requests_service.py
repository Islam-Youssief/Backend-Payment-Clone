import http
import logging

import requests

import api.core.exceptions as exceptions


def get_service(env):
    if env == 'lcl':
        return RequestsWrapper()
    return WiremockRequester()


class RequestsWrapper:
    def __init__(self, test_requests=None):
        self._requests = test_requests or requests
    
    def request(self, method, url, **kwargs):
        logging.info(f'[{method}] {url} with kwargs: {kwargs}')
        response = self._requests.request(method, url, **kwargs)
        return self._handle_response(response, method, url, **kwargs)

    def _handle_response(self, response, method, url, **kwargs):
        if response.status_code != http.HTTPStatus.OK:
            logging.error(f'[{method}] {url} with kwargs: {kwargs}')
            raise exceptions.ResponseError(response)
        return response


class WiremockRequester:

    def __init__(self, test_requests=None):
        self._requests = test_requests or requests
        self._wiremock_url = '127.0.0.1:8080'

    def request(self, method, url, **kwargs):
        logging.info(f'[{method}] (wiremock) {self._wiremock_url}/{url} with kwargs: {kwargs}')
        return self._requests.request(method, f'{self._wiremock_url}/{url}', **kwargs)
