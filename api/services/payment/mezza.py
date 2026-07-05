import api.services.requests_service as requests_service
import api.services.payment.mezza_validator as validators
import api.core.configurations as configurations
import time
import hashlib


MEZZA_PAYMENT_URL = "https://api.dlocal.com/payments"


class MezzaClient:

    def __init__(self, env, test_request_sender=None, test_validator=None, test_headers_builder=None):
        self._env = env
        self._request_sender = test_request_sender or requests_service.get_service(self._env)
        self._validator = test_validator or validators.MeezaPaymentDataValidator()
        self._headers_builder = test_headers_builder or _MeezaAuthBuilder()

    def create_payment(self, data):
        self._validator.validate(data)

        response = self._request_sender.request(
            method='POST',
            url=MEZZA_PAYMENT_URL,
            json=data,
            headers=self._headers_builder.build_headers(data)
        )
                

        return response

    @property
    def _headers(self):
        return {
            'Content-Type': 'application/json'
        }
    




class _MeezaAuthBuilder:

    def __init__(self):
        self._config = configurations.PaymentsConfig()

    def build_headers(self, data=None):
        return {
            "X-Login": self._config.meeza_login,
            "X-Trans-Key": self._config.meeza_trans_key,
            "X-Date": str(int(time.time())),
            "Content-Type": "application/json",
            "Authorization": self._build_signature(data),
        }

    def _build_signature(self, data):
        """
        Mock signature (NOT real dLocal implementation)
        just to simulate Fawry-like behavior
        """
        base_string = (
            f"{self._config.meeza_login}"
            f"{self._config.meeza_trans_key}"
            f"{data.get('amount', '') if data else ''}"
        )

        return hashlib.sha256(base_string.encode()).hexdigest()