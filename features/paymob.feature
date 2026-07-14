Feature: Paymob Create Intention

    Scenario: 1- Successful payment with valid credentials
      Given the request URL is "${PAYMOB_INTENTION_URL}"
        And the request header contains the authorization token "Token ${configurations.PaymentsConfig.paymob_secret_key}" 
        When the request is sent
        Then the response status should be 201
        And the response JSON at "$.payment_keys" should exist
        And the response JSON at "$.client_secret" should exist
        And the response JSON at "$.id" should exist

    Scenario: 2- Unsuccessful payment with invalid integration ID
      Given the request URL is "${PAYMOB_INTENTION_URL}"
        And the request header contains the authorization token "Token ${configurations.PaymentsConfig.paymob_secret_key}"
        And the request body contains an invalid integration ID
        When the request is sent
        Then the response status should be 404
        And the response JSON at "$.detail" should be "integration ID/Name does not exist in our system . You can find the list of Integration ID’/Names from Merchant Dashboard under Developers → Payment Integrations Tab"
      
    Scenario: 3- Unsuccessful payment with missing item name
      Given the request URL is "${PAYMOB_INTENTION_URL}"
        And the request header contains the authorization token "Token ${configurations.PaymentsConfig.paymob_secret_key}"
        When the request is sent
        Then the response should be 400
        And the response JSON at "$.items.name" should be "This field is required."

    Scenario: 4- Unsuccessful payment with missing item amount
      Given the request URL is "${PAYMOB_INTENTION_URL}"
        And the request header contains the authorization token "Token ${configurations.PaymentsConfig.paymob_secret_key}"
        And the request body contains missing item amount
        When the request is sent
        Then the response status should be 400
        And the response JSON at "$.items.amount" should be "This field is required."
    
    Scenario: 5- Unsuccessful payment with missing phone number
      Given the request URL is "${PAYMOB_INTENTION_URL}"
        And the request header contains the authorization token "Token ${configurations.PaymentsConfig.paymob_secret_key}"
        And the request body contains missing phone number
        When the request is sent
        Then the response status should be 400
        And the response JSON at "$.billing_data.phone_number" should be "This field is required."
