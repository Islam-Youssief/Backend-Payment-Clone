import api.services.requests_service as requests_service
import api.core.configurations as config
PAYMOB_INTENTION_URL = "https://accept.paymob.com/v1/intention/"

class PaymobClient:
    def __init__(self,env,test_request_sender = None):
       self._env = env
       self._request_sender = test_request_sender or requests_service.get_service(self._env)
       self._secret_key = config.PaymentsConfig().paymob_secret_key 

    def _build_headers(self):
        return {
            "Authorization" : f"Token {self._secret_key}",
            'Content-Type' : 'application/json'
            }
    
    def create_intention(self,data):
        response = self._request_sender.request(
            method= "POST",
            url= PAYMOB_INTENTION_URL,
            headers= self._build_headers(),
            json= data  
        )
        return response
    