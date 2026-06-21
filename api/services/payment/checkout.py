import os

import api.services.requests_service as requests_service




class CheckoutClient:
    def __init__(self , env , test_request_sender=None):
        self.env = env 
        self._request_sender = test_request_sender or requests_service.get_service(env)
    
    def pay_with_card(self, data):
        response = self._request_sender.request(method='POST', url='/payments', data=data, headers=self._headers)
        return response

    @property
    def _headers(self):
        return{
            'Content-Type':'application/json',
            'Authorization': f"Bearer {os.environ.get('CHECKOUT_SECRET_KEY')}"
        }


