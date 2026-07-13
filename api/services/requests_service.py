import http
import logging

import requests

import api.core.configurations as configurations
import api.core.exceptions as exceptions


def get_service(env):
    if env != 'lcl':
        return RequestsWrapper()
    return WiremockRequester()


class RequestsWrapper:

    def __init__(self, test_requests=None):
        self._requests = test_requests or requests
    
    def request(self, method, url, **kwargs):
        logging.info(f'[{method}] {url} with kwargs: {kwargs}')
        kwargs.setdefault('timeout', 5)
        response = self._requests.request(method, url, **kwargs)
        return self._handle_response(response, method, url, **kwargs)

    def _handle_response(self, response, method, url, **kwargs):
        if not (200 <= response.status_code < 300):
            logging.error(f'[{method}] {url} with kwargs: {kwargs}')
            raise exceptions.ResponseError(response)
        return response


class WiremockRequester:

    def __init__(self, test_requests=None):
        self._requests = test_requests or requests
        self._wiremock_url = configurations.AppConfig().wiremock_url

    def request(self, method, url, **kwargs):
        logging.info(f"[{method}] (wiremock) {self._wiremock_url}/{url.replace('https://', '')} with kwargs: {kwargs}")
        kwargs.setdefault('timeout', 5)
        response = self._requests.request(method, f"{self._wiremock_url}/{url.replace('https://', '')}", **kwargs)
        return self._handle_response(response, method, url, **kwargs)

    def _handle_response(self, response, method, url, **kwargs):
        if not (200 <= response.status_code < 300):
            logging.error(f'[{method}] {url} with kwargs: {kwargs}')
            raise exceptions.ResponseError(response)
        return response