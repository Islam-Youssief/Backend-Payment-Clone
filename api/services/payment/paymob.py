import api.services.requests_service as requests_service
import api.core.configurations as config
import api.core.exceptions as exceptions
PAYMOB_INTENTION_URL = "https://accept.paymob.com/v1/intention/"

class PaymobClient:
    def __init__(self,env,test_request_sender = None,test_validator = None):
       self._env = env
       self._request_sender = test_request_sender or requests_service.get_service(self._env)
       self._validator = test_validator  or PaymobUserDataValidator() 
       self._secret_key = config.PaymentsConfig().paymob_secret_key 

    def _build_headers(self):
        return {
            "Authorization" : f"Token {self._secret_key}",
            'Content-Type' : 'application/json'
            }
    
    def create_intention(self,data):
        self._validator.validate(data)
        response = self._request_sender.request(
            method= "POST",
            url= PAYMOB_INTENTION_URL,
            headers= self._build_headers(),
            json= data  
        )
        return response

class PaymobUserDataValidator:
    def validate(self,data):
        required_fields = ["amount","currency","payment_methods","items","billing_data"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise exceptions.RequiredInputError(f'Missing fields: {missing_fields}')
        self._validate_amount(data['amount'])
        self._validate_currency(data['currency'])
        self._validate_payment_methods(data['payment_methods'])
        self._validate_items(data['items'])
        self._validate_total_amount(data['amount'],data['items'])
        self._validate_billing_data(data['billing_data'])

    def _validate_amount(self,amount):
        if not isinstance(amount,int):
            raise exceptions.InputDataTypeError("Amount must be an integar representing amount in cents")
        if amount <= 0:
            raise exceptions.ValidationError("Amount must be higher than zero")
    
    def _validate_items(self,items):
        if not isinstance(items,list):
            raise exceptions.InputDataTypeError(f"Expected list")
        if len(items) == 0:
            raise exceptions.RequiredInputError(f"Missing items")
        for item in items:
            if item.get("name") is None:
                raise exceptions.RequiredInputError(f"Missing item name")
            if item.get("amount") is None:
                raise exceptions.RequiredInputError(f"Missing item amount")

    def _validate_total_amount(self,amount,items):
        _total_amount = 0
        for item in items:
            _total_amount +=item["amount"]
        if amount !=_total_amount:
            raise exceptions.ValidationError(f"Amount doesn't match")
        
    def _validate_currency(self,currency):
       if not isinstance(currency, str):
            raise exceptions.InputDataTypeError(f"Expected string") 

    def _validate_billing_data(self,billing_data):
        required_fields = ["first_name","last_name","email"]
        missing_fields = [field for field in required_fields if not billing_data.get(field)]
        if missing_fields:
            raise exceptions.RequiredInputError(f'Missing fields: {missing_fields}')
            
    def _validate_payment_methods(self,payment_methods):
         if not isinstance(payment_methods, list):
            raise exceptions.InputDataTypeError(f"Expected list")
         if len(payment_methods) == 0:
            raise exceptions.RequiredInputError("Payment Methods can't be empty")
         for method in payment_methods:
            if not isinstance(method,int):
                raise exceptions.ValidationError("Integration ID is required")
            
    
