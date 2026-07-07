Feature: Checkout Payment


    Scenario: 1- Successful payment with a valid card
        Given the request URL is "${configuration.PaymentsConfig().checkout_prefix_code}.${CHECKOUT_PAYMENT_URL}"
        And the request header contains the authorization token "Bearer ${configuration.PaymentsConfig().checkout_secret_key}"
        And the request body contains valid card details
        When the request is sent
        Then the response status should be 200
        And the response JSON at "$.message" should be "Payment successful"

    Scenario: 2- Unsuccessful payment with an invalid card
        Given the request URL is "${configuration.PaymentsConfig().checkout_prefix_code}.${CHECKOUT_PAYMENT_URL}"
        And the request header contains the authorization token "Bearer ${configuration.PaymentsConfig().checkout_secret_key}"
        And the request body contains invalid card details
        When the request is sent
        Then the response status should be 400
        And the response JSON at "$.message" should be "Payment failed: Invalid card details"
    
    Scenario: 3- Unsuccessful payment with missing data
        Given the request URL is "${configuration.PaymentsConfig().checkout_prefix_code}.${CHECKOUT_PAYMENT_URL}"
        And the request header contains the authorization token "Bearer ${configuration.PaymentsConfig().checkout_secret_key}"
        And the request body contains missing data
        When the request is sent
        Then the response status should be 400
        And the response JSON at "$.message" should be "Payment failed: Missing required data"
    
    Scenario: 4- Unsuccessful payment with an expired card
        Given the request URL is "${configuration.PaymentsConfig().checkout_prefix_code}.${CHECKOUT_PAYMENT_URL}"
        And the request header contains the authorization token "Bearer ${configuration.PaymentsConfig().checkout_secret_key}"
        And the request body contains expired card details
        When the request is sent
        Then the response status should be 400
        And the response JSON at "$.message" should be "Payment failed: Card expired"

    Scenario: 5- Unsuccessful payment with an invalid authorization token
        Given the request URL is "${configuration.PaymentsConfig().checkout_prefix_code}.${CHECKOUT_PAYMENT_URL}"
        And the request header contains the authorization token "Bearer invalid_token"
        And the request body contains valid card details
        When the request is sent
        Then the response status should be 401
        And the response JSON at "$.message" should be "Unauthorized"

    Scenario: 6- Unsuccessful payment with an invalid card data
        Given the request URL is "${configuration.PaymentsConfig().checkout_prefix_code}.${CHECKOUT_PAYMENT_URL}"
        And the request header contains the authorization token "Bearer ${configuration.PaymentsConfig().checkout_secret_key}"
        And the request body contains invalid card data
        When the request is sent
        Then the response status should be 400
        And the response JSON at "$.message" should be "Payment failed: Invalid card data"