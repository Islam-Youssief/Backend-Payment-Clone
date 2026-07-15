import api.services.requests_service as requests_service
import api.services.payment.loginValidators as loginValidators

LOGIN_URL = "https://api.stripe.com/v1/login"


class LoginClient:
    def __init__(self,env,test_request_sender=None):
        self._env = env
        self._request_sender = test_request_sender or requests_service.get_service(self._env)
        self._validator = loginValidators.UserLoginValidator()

    def login(self,data, authorization):
        self._validator.validate(data)
        response = self._request_sender.request(
             method="POST",
             url=LOGIN_URL,
             json=data,
             headers={
                 "Authorization": authorization
             }
        )
        return response

