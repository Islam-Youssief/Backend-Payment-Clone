Feature: Checkout Payment API

    Test possible scenarios for processing card payments through Checkout API endpoints.
        Scenarios include:
        - Valid, invalid, expired, and missing card data.
        - Valid, invalid, and missing authorization tokens.
        - Missing required payment fields such as amount and currency.
        - Checkout API error responses such as 400 Bad Request and 500 Internal Server Error.

    Scenario: 1- Successful payment with a valid card
            Given the request URL is ${BASE_URL}/api/payments/checkout
                And the request headers
                    | parameter | value |
                    | Authorization | Bearer ${configuration.PaymentsConfig().checkout_secret_key} |
                And the request body contains valid card details
                And the request json payload
                    """
                    {
                        "cardHolder": "${VALID_CARD_HOLDER}",
                        "cardNumber": "${VALID_CARD_NUMBER}",
                        "amount": 1000,
                        "cardExpiryYear": "27",
                        "cardExpiryMonth": "12",
                        "cvv": "123"
                    }
                    """
            When the request is sent
            Then the response status should be 200
                And the response JSON at "$.message" should be "you have successfully paid with card"
                And the response JSON at "$.amount" should be 1000
                And the response JSON at "$.status" should be "success"


    Scenario: 2- Unsuccessful payment with an invalid card number
            Given the request URL is ${BASE_URL}/api/payments/checkout
                And the request headers
                    | parameter | value |
                    | Authorization | Bearer ${configuration.PaymentsConfig().checkout_secret_key} |
                And the request body contains invalid card number
                And the request json payload
                    """
                    {
                        "cardHolder": "${VALID_CARD_HOLDER}",
                        "cardNumber": "${INVALID_CARD_NUMBER}",
                        "amount": 100,
                        "cardExpiryYear": "27",
                        "cardExpiryMonth": "12",
                        "cvv": "123"
                    }
                    """
            When the request is sent
            Then the response status should be 400
                And the response JSON at "$.message" should be "Payment failed: Invalid card number"
                And the response JSON at "$.amount" should be 1000
                And the response JSON at "$.status" should be "bad_request"

    
    Scenario: 3- Unsuccessful payment with missing required data
            Given the request URL is ${BASE_URL}/api/payments/checkout
                And the request headers
                    | parameter | value |
                    | Authorization | Bearer ${configuration.PaymentsConfig().checkout_secret_key} |            
                And the request body contains missing data
                And the request json payload
                    """
                    {
                        "cardNumber": "${VALID_CARD_NUMBER}",
                        "cardHolder": "",
                        "amount": 1000,
                        "cardExpiryYear": "27",
                        "cardExpiryMonth": "12",
                        "cvv": "123"
                    }
                    """
            When the request is sent
            Then the response status should be 400
                And the response JSON at "$.message" should be "Payment failed: Missing required data"
                And the response JSON at "$.amount" should be 1000
                And the response JSON at "$.status" should be "bad_request"
    
    Scenario: 4- Unsuccessful payment with an expired card
            Given the request URL is ${BASE_URL}/api/payments/checkout
                And the request headers
                        | parameter | value |
                        | Authorization | Bearer ${configuration.PaymentsConfig().checkout_secret_key} |
                And the request body contains expired card details
                And the request json payload
                    """
                    {
                        "cardNumber": "${VALID_CARD_NUMBER}",
                        "cardHolder": "${VALID_CARD_HOLDER}",
                        "amount": 1000,
                        "cardExpiryYear": "20",
                        "cardExpiryMonth": "12",
                        "cvv": "123"
                    }
                    """
            When the request is sent
            Then the response status should be 400
                And the response JSON at "$.message" should be "Payment failed: Card expired"
                And the response JSON at "$.amount" should be 1000
                And the response JSON at "$.status" should be "bad_request"

    Scenario: 5- Unsuccessful payment with an invalid authorization token
            Given the request URL is ${BASE_URL}/api/payments/checkout
                And the request headers
                        | parameter | value |
                        | Authorization | Bearer invalid_secret_key |
                And the request body contains valid card details
                And the request json payload
                    """
                    {
                        "cardNumber": "${VALID_CARD_NUMBER}",
                        "cardHolder": "${VALID_CARD_HOLDER}",
                        "amount": 1000,
                        "cardExpiryYear": "27",
                        "cardExpiryMonth": "12",
                        "cvv": "123"
                    }
                    """
            When the request is sent
            Then the response status should be 401
                And the response JSON at "$.message" should be "Unauthorized"
                And the response JSON at "$.amount" should be 1000
                And the response JSON at "$.status" should be "unauthorized"

    Scenario: 6- Unsuccessful payment with an invalid CVV
            Given the request URL is ${BASE_URL}/api/payments/checkout
                And the request headers
                        | parameter | value |
                        | Authorization | Bearer ${configuration.PaymentsConfig().checkout_secret_key} |
                And the request body contains invalid card cvv
                And the request json payload
                    """
                    {
                        "cardNumber": "${VALID_CARD_NUMBER}",
                        "cardHolder": "${VALID_CARD_HOLDER}",
                        "amount": 1000,
                        "cardExpiryYear": "27",
                        "cardExpiryMonth": "12",
                        "cvv": "${INVALID_CARD_CVV}"
                    }
                    """
            When the request is sent
            Then the response status should be 400
                And the response JSON at "$.message" should be "Payment failed: Invalid cvv"
                And the response JSON at "$.amount" should be 1000
                And the response JSON at "$.status" should be "bad_request"

    Scenario: 7- Unsuccessful payment with a missing authorization token
            Given the request URL is ${BASE_URL}/api/payments/checkout
                And the request does not contain authorization header
                And the request body contains valid card details
                And the request json payload
                    """
                    {
                        "cardNumber": "${VALID_CARD_NUMBER}",
                        "cardHolder": "${VALID_CARD_HOLDER}",
                        "amount": 100,
                        "cardExpiryYear": "27",
                        "cardExpiryMonth": "12",
                        "cvv": "123"
                    }
                    """
            When the request is sent
            Then the response status should be 401
                And the response JSON at "$.message" should be "Unauthorized"
                And the response JSON at "$.amount" should be 1000
                And the response JSON at "$.status" should be "unauthorized"

    Scenario: 08- Unsuccessful payment when Checkout Payment returns an internal server error
            Given the request URL is ${BASE_URL}/api/payments/checkout
                And the request headers
                    | parameter | value |
                    | Authorization | Bearer ${configuration.PaymentsConfig().checkout_secret_key} |
                And the Checkout Payment service returns status code 500
            When the request is sent
            Then the response status should be 500
                And the response JSON at "$.message" should be "Internal server error"
                And the response JSON at "$.status" should be "Internal_server_error"
