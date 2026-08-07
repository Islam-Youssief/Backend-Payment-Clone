

vars = {
    'BASE_URL': 'http://127.0.0.1:5000',
    'VALID_CARD_HOLDER': 'TESTER TESTING PAYPAL',
    'VALID_CARD_NUMBER': '1111111111111111',
    'PAYMOB_SECRET_KEY': 'SECRET_KEY_HAHAHA'
}

def initialize_definition(context):
    context.vars.add_vars(vars)
