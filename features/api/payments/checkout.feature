Feature: Checkout Payment API

    Test possible scenarios for processing card payments through Checkout API endpoints.
        Scenarios include:
        - Valid, invalid, expired, and missing card data.
        - Valid, invalid, and missing authorization tokens.
        - Missing required payment fields such as amount and currency.
        - Checkout API error responses such as 400 Bad Request and 500 Internal Server Error.

    Scenario: 1- Successful payment with a valid card
            Given the request URL is "${configuration.PaymentsConfig().checkout_prefix_code}.${CHECKOUT_PAYMENT_URL}"
            And the request header contains the authorization token "Bearer ${configuration.PaymentsConfig().checkout_secret_key}"
            And the request body contains valid card details
            And the request json payload
            """
            {
                "source": {
                    "type": "card",
                    "number": "2242424242424242",
                    "cvv": "100",
                    "expiry_month": 12,
                    "expiry_year": 2030
                },
                "currency": "USD",
                "amount": 1000,
                "processing_channel_id": "pc_test_123"
            }
            """
            When the request is sent
            Then the response status should be 200
            And the response JSON at "$.message" should be "Payment successful"

    Scenario: 2- Unsuccessful payment with an invalid card number
            Given the request URL is "${configuration.PaymentsConfig().checkout_prefix_code}.${CHECKOUT_PAYMENT_URL}"
            And the request header contains the authorization token "Bearer ${configuration.PaymentsConfig().checkout_secret_key}"
            And the request body contains invalid card details
            And the request json payload
            """
            {
                "source": {
                    "type": "card",
                    "number": "2504450000000000",
                    "cvv": "123",
                    "expiry_month": 12,
                    "expiry_year": 2030
                },
                "currency": "USD",
                "amount": 1000,
                "processing_channel_id": "pc_test_123"
            }
            """
            When the request is sent
            Then the response status should be 400
            And the response JSON at "$.message" should be "Payment failed: Invalid card details"
    
    Scenario: 3- Unsuccessful payment with missing required data
            Given the request URL is "${configuration.PaymentsConfig().checkout_prefix_code}.${CHECKOUT_PAYMENT_URL}"
            And the request header contains the authorization token "Bearer ${configuration.PaymentsConfig().checkout_secret_key}"
            And the request body contains missing data
            And the request json payload
            """
            {
                "source": {
                    "type": "card",
                    "number": "",
                    "cvv": "",
                    "expiry_month": 0,
                    "expiry_year": 0
                },
                "currency": "",
                "amount": 0,
                "processing_channel_id": ""
            }
            """
            When the request is sent
            Then the response status should be 400
            And the response JSON at "$.message" should be "Payment failed: Missing required data"
    
    Scenario: 4- Unsuccessful payment with an expired card
            Given the request URL is "${configuration.PaymentsConfig().checkout_prefix_code}.${CHECKOUT_PAYMENT_URL}"
            And the request header contains the authorization token "Bearer ${configuration.PaymentsConfig().checkout_secret_key}"
            And the request body contains expired card details
            And the request json payload
            """
            {
                "source": {
                    "type": "card",
                    "number": "4242424242424242",
                    "cvv": "123",
                    "expiry_month": 12,
                    "expiry_year": 2020
                },
                "currency": "USD",
                "amount": 1000,
                "processing_channel_id": "pc_test_123"
            }
            """
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

    Scenario: 6- Unsuccessful payment with an invalid CVV
            Given the request URL is "${configuration.PaymentsConfig().checkout_prefix_code}.${CHECKOUT_PAYMENT_URL}"
            And the request header contains the authorization token "Bearer ${configuration.PaymentsConfig().checkout_secret_key}"
            And the request body contains invalid card data
            And the request json payload
            """
            {
                "source": {
                    "type": "card",
                    "number": "4242424242424242",
                    "cvv": "11",
                    "expiry_month": 12,
                    "expiry_year": 2030
                },
                "currency": "USD",
                "amount": 1000,
                "processing_channel_id": "pc_test_123"
            }
            """
            When the request is sent
            Then the response status should be 400
            And the response JSON at "$.message" should be "Payment failed: Invalid cvv"
    
    Scenario: 7- Unsuccessful payment with a missing authorization token
            Given the request URL is "${configuration.PaymentsConfig().checkout_prefix_code}.${CHECKOUT_PAYMENT_URL}"
            And the request header does not contain an authorization token
            And the request body contains valid card details
            And the request json payload
            """
            {
                "source": {
                    "type": "card",
                    "number": "4242424242424242",
                    "cvv": "123",
                    "expiry_month": 12,
                    "expiry_year": 2030
                },
                "currency": "USD",
                "amount": 1000,
                "processing_channel_id": "pc_test_123"
            }
            """
            When the request is sent
            Then the response status should be 401
            And the response JSON at "$.message" should be "Unauthorized"

    Scenario: 08- Unsuccessful payment when Checkout Payment returns an internal server error
            Given the request URL is "${configuration.PaymentsConfig().checkout_prefix_code}.${CHECKOUT_PAYMENT_URL}"
            And the request header contains the authorization token "Bearer ${configuration.PaymentsConfig().checkout_secret_key}"
            And the Checkout Payment service returns status code 500
            And the request json payload
            """
            {
                "source": {
                    "type": "card",
                    "number": "2242424242424242",
                    "cvv": "100",
                    "expiry_month": 12,
                    "expiry_year": 2030
                },
                "currency": "USD",
                "amount": 1000,
                "processing_channel_id": "pc_test_123"
            }
            """
            When the request is sent
            Then the response status should be 500
            And the response JSON at "$.message" should be "Internal server error"