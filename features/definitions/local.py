

vars = {
    'BASE_URL': 'http://127.0.0.1:5000',
    'VALID_CARD_HOLDER': 'TESTER TESTING PAYPAL',
    'VALID_CARD_NUMBER': '1111111111111111',
    'VALID_TOKEN': 'valid_token_123',
    'INVALID_TOKEN': 'invalid_token_123',
    'EXPIRED_TOKEN': 'expired_token_123',
    'MISSING_PERMISSIONS_TOKEN': 'missing_permissions_token_123'
}

def initialize_definition(context):
    context.vars.add_vars(vars)
