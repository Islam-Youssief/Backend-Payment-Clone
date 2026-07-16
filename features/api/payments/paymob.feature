
Feature: Paymob Payment API
  Test possible scenarios for creating a payment intention via the Paymob endpoint,
  Some scenarios include creating an intention with:
    - Valid credentials and valid payment data.
    - Invalid credentials (wrong secret key).
    - Missing item name, missing item amount, and missing billing phone.

  Scenario: 1 - Successfully create a payment intention with valid data
    A merchant with a valid secret key and complete, valid payment data
    should be able to create a payment intention that Paymob accepts.

    Given a request url ${BASE_URL}/accept.paymob.com/v1/intention/
        And request headers
            | param         | value                        |
            | Authorization | Token ${PAYMOB_SECRET_KEY}   |
        And a request json payload
            """
            {
                "amount": 2000,
                "currency": "EGP",
                "payment_methods": [158],
                "items": [
                    {"name": "Staff", "amount": 2000}
                ],
                "billing_data": {
                    "first_name": "Roxy",
                    "last_name": "Migurdia",
                    "phone": "010010010101"
                }
            }
            """
        When the request sends POST
        Then the response status is OK
          And the response json at $.status is equal to "intended"
          And the response json at $.id is equal to "1234567890"
          And the response json at $.client_secret is equal to "client_secret"

  Scenario: 2 - Unsuccessful attempt with an invalid secret key
    A request signed with a secret key that Paymob doesn't recognize
    should be rejected as unauthorized.

    Given a request url ${BASE_URL}/accept.paymob.com/v1/intention/
        And request headers
            | param         | value                    |
            | Authorization | Token INVALID_SECRET_KEY |
        And a request json payload
            """
            {
                "amount": 2000,
                "currency": "EGP",
                "payment_methods": [158],
                "items": [
                    {"name": "Staff", "amount": 2000}
                ],
                "billing_data": {
                    "first_name": "Roxy",
                    "last_name": "Migurdia",
                    "phone": "010010010101"
                }
            }
            """
        When the request sends POST
        Then the response status is UNAUTHORIZED
          And the response json at $.detail is equal to "Invalid token."
          
  Scenario: 3 - Unsuccessful attempt with an invalid integration id
    a request must have valid integration id . Paymob rejects the intention
     if its missing or invalid.

    Given a request url ${BASE_URL}/accept.paymob.com/v1/intention/
        And request headers
            | param         | value                      |
            | Authorization | Token ${PAYMOB_SECRET_KEY} |
        And a request json payload
            """
            {
                "amount": 2000,
                "currency": "EGP",
                "payment_methods": [99999999999],
                "items": [
                    {"name": "Staff", "amount": 2000}
                ],
                "billing_data": {
                    "first_name": "Roxy",
                    "last_name": "Migurdia",
                    "phone": "010010010101"
                }
            }
            """
        When the request sends POST
        Then the response status is NOT_FOUND
          And the response json at $.detail is equal to "Integration ID/Name does not exist in our system . You can find the list of Integration ID’/Names from Merchant Dashboard under Developers → Payment Integrations Tab"
 
  Scenario: 4 - Unsuccessful attempt with a missing item name
    Every item in the "items" list must have a name. Paymob rejects the
    intention when it's missing.

    Given a request url ${BASE_URL}/accept.paymob.com/v1/intention/
        And request headers
            | param         | value                      |
            | Authorization | Token ${PAYMOB_SECRET_KEY} |
        And a request json payload
            """
            {
                "amount": 2000,
                "currency": "EGP",
                "payment_methods": [158],
                "items": [
                    {"amount": 2000}
                ],
                "billing_data": {
                    "first_name": "Roxy",
                    "last_name": "Migurdia",
                    "phone": "010010010101"
                }
            }
            """
        When the request sends POST
        Then the response status is BAD_REQUEST
          And the response json at $.items.name[0] is equal to "This field is required."

  Scenario: 5 - Unsuccessful attempt with a missing item amount
    Every item in the "items" list must have an amount. Paymob rejects the
    intention when it's missing.

    Given a request url ${BASE_URL}/accept.paymob.com/v1/intention/
        And request headers
            | param         | value                      |
            | Authorization | Token ${PAYMOB_SECRET_KEY} |
        And a request json payload
            """
            {
                "amount": 2000,
                "currency": "EGP",
                "payment_methods": [158],
                "items": [
                    {"name": "Staff"}
                ],
                "billing_data": {
                    "first_name": "Roxy",
                    "last_name": "Migurdia",
                    "phone": "010010010101"
                }
            }
            """
        When the request sends POST
        Then the response status is BAD_REQUEST
          And the response json at $.items.amount[0] is equal to "This field is required."

  Scenario: 6 - Unsuccessful attempt with a missing billing phone
    The billing data must include an phone. Paymob rejects the
    intention when it's missing.

    Given a request url ${BASE_URL}/accept.paymob.com/v1/intention/
        And request headers
            | param         | value                      |
            | Authorization | Token ${PAYMOB_SECRET_KEY} |
        And a request json payload
            """
            {
                "amount": 2000,
                "currency": "EGP",
                "payment_methods": [158],
                "items": [
                    {"name": "Staff", "amount": 2000}
                ],
                "billing_data": {
                    "first_name": "Roxy",
                    "last_name": "Migurdia"
                }
            }
            """
        When the request sends POST
        Then the response status is BAD_REQUEST
          And the response json at $.billing_data.phone[0] is equal to "This field is required."
