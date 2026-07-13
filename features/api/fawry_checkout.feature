Feature: Fawry Payment API
  Test different scenarios where the customers has valid and invalid responses for different reasons.
  Some scenarios include:
    - Successful payment processing with valid card information and authorization token.
    - Validation failures due to missing required fields (merchantRefNum, amount, cardNumber, cardExpiryYear, cardExpiryMonth, cvv).
    - Validation failures due to invalid inputs (negative amount, invalid card number, invalid expiry date, invalid CVV).
    - Payment failure due to insufficient funds.
    - External service integration issues (e.g. Fawry service unavailable, Fawry service internal server error, or request timeout).
    - Authorization issues (e.g. invalid token, expired token).

  Scenario: 1 - Successful Fawry payment processing
    Customers can successfully process a payment using Fawry when they provide a valid authentication token and valid checkout details (including card details and a positive amount).

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123456",
              "customerProfileId": "CUST_987",
              "amount": 100.50,
              "cardHolder": "${VALID_CARD_HOLDER}",
              "cardNumber": "${VALID_CARD_NUMBER}",
              "cardExpiryYear": "25",
              "cardExpiryMonth": "12",
              "cvv": "123"
            }
            """
        When the request sends POST
        Then the response status is created
          And the response json at $.status_code is equal to 200
          And the response json at $.status_description is equal to "Operation done successfully"
          And the response json at $.order_status is equal to "PAID"



  Scenario: 3 - Payment fails due to missing amount
    The request fails with a 400 Bad Request if the amount field is missing from the payload.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123456",
              "customerProfileId": "CUST_987",
              "cardHolder": "${VALID_CARD_HOLDER}",
              "cardNumber": "${VALID_CARD_NUMBER}",
              "cardExpiryYear": "25",
              "cardExpiryMonth": "12",
              "cvv": "123"
            }
            """
        When the request sends POST
        Then the response status is BAD REQUEST
          And the response json at $.status is equal to 400
          And the response json at $.message is equal to "Input <amount> is required"

  Scenario: 4 - Payment fails due to missing cardNumber
    The request fails with a 400 Bad Request if the cardNumber field is missing from the payload.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123456",
              "customerProfileId": "CUST_987",
              "cardHolder": "${VALID_CARD_HOLDER}",
              "amount": 100.50,
              "cardExpiryYear": "25",
              "cardExpiryMonth": "12",
              "cvv": "123"
            }
            """
        When the request sends POST
        Then the response status is BAD REQUEST
          And the response json at $.status is equal to 400
          And the response json at $.message is equal to "Input <cardNumber> is required"



  Scenario: 7 - Payment fails due to missing cvv
    The request fails with a 400 Bad Request if the cvv field is missing from the payload.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123456",
              "customerProfileId": "CUST_987",
              "amount": 100.50,
              "cardHolder": "${VALID_CARD_HOLDER}",
              "cardNumber": "${VALID_CARD_NUMBER}",
              "cardExpiryYear": "25",
              "cardExpiryMonth": "12"
            }
            """
        When the request sends POST
        Then the response status is BAD REQUEST
          And the response json at $.status is equal to 400
          And the response json at $.message is equal to "Input <cvv> is required"

  Scenario: 8 - Payment fails due to invalid negative amount
    The request fails with a 400 Bad Request if the payment amount is negative or zero.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123460",
              "amount": -50.00,
              "cardHolder": "${VALID_CARD_HOLDER}",
              "cardNumber": "${VALID_CARD_NUMBER}",
              "cardExpiryYear": "25",
              "cardExpiryMonth": "12",
              "cvv": "123"
            }
            """
        When the request sends POST
        Then the response status is BAD REQUEST
          And the response json at $.status is equal to 400
          And the response json at $.message is equal to "Amount must be valid number"

  Scenario: 9 - Payment fails due to invalid card number
    The request fails with a 400 Bad Request if the card number is not exactly 16 digits or contains non-numeric characters.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123457",
              "amount": 100.50,
              "cardHolder": "${VALID_CARD_HOLDER}",
              "cardNumber": "411",
              "cardExpiryYear": "25",
              "cardExpiryMonth": "12",
              "cvv": "123"
            }
            """
        When the request sends POST
        Then the response status is BAD REQUEST
          And the response json at $.status is equal to 400
          And the response json at $.message is equal to "Card number must be 16 digits long"



  Scenario: 11 - Payment fails due to invalid CVV
    The request fails with a 400 Bad Request if the CVV is not exactly 3 digits or contains non-numeric characters.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123457",
              "amount": 100.50,
              "cardHolder": "${VALID_CARD_HOLDER}",
              "cardNumber": "${VALID_CARD_NUMBER}",
              "cardExpiryYear": "25",
              "cardExpiryMonth": "12",
              "cvv": "12A"
            }
            """
        When the request sends POST
        Then the response status is BAD REQUEST
          And the response json at $.status is equal to 400
          And the response json at $.message is equal to "CVV must be 3 or 4 digits long"

  Scenario: 12 - Payment fails due to insufficient funds
    The request fails with a 402 Payment Required when the card does not have sufficient balance to complete the transaction.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123458",
              "amount": 999999.00,
              "cardHolder": "${VALID_CARD_HOLDER}",
              "cardNumber": "${VALID_CARD_NUMBER}",
              "cardExpiryYear": "25",
              "cardExpiryMonth": "12",
              "cvv": "123"
            }
            """
        When the request sends POST
        Then the response status is PAYMENT REQUIRED
          And the response json at $.status is equal to 402
          And the response json at $.message is equal to "Insufficient Balance"

  Scenario: 13 - Fawry service is currently unavailable or returns Bad Gateway
    The request fails with a 502 Bad Gateway if the external Fawry service is down or returns a connection error.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123459",
              "amount": 100.50,
              "cardHolder": "${VALID_CARD_HOLDER}",
              "cardNumber": "${VALID_CARD_NUMBER}",
              "cardExpiryYear": "25",
              "cardExpiryMonth": "12",
              "cvv": "123"
            }
            """
        When the request sends POST
        Then the response status is BAD GATEWAY
          And the response json at $.status is equal to 502
          And the response json at $.message is equal to "External service unavailable"

  Scenario: 14 - Fawry service returns an internal server error
    The request fails with a 502 Bad Gateway if the external Fawry service encounters an internal server error.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123463",
              "amount": 100.50,
              "cardHolder": "${VALID_CARD_HOLDER}",
              "cardNumber": "${VALID_CARD_NUMBER}",
              "cardExpiryYear": "25",
              "cardExpiryMonth": "12",
              "cvv": "123"
            }
            """
        When the request sends POST
        Then the response status is BAD GATEWAY
          And the response json at $.status is equal to 502
          And the response json at $.message is equal to "External service error"

  Scenario: 15 - Fawry service request times out
    The request fails with a 504 Gateway Timeout if the external Fawry service times out.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123464",
              "amount": 100.50,
              "cardHolder": "${VALID_CARD_HOLDER}",
              "cardNumber": "${VALID_CARD_NUMBER}",
              "cardExpiryYear": "25",
              "cardExpiryMonth": "12",
              "cvv": "123"
            }
            """
        When the request sends POST
        Then the response status is GATEWAY TIMEOUT
          And the response json at $.status is equal to 504
          And the response json at $.message is equal to "External service timeout"

  Scenario: 16 - Unauthorized access to the payment endpoint (Invalid token)
    The request fails with a 401 Unauthorized if the client provides an invalid authorization token.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${INVALID_TOKEN} |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123461",
              "cardHolder": "${VALID_CARD_HOLDER}",
              "cardNumber": "${VALID_CARD_NUMBER}",
              "amount": 100.50,
              "cardExpiryYear": "25",
              "cardExpiryMonth": "12",
              "cvv": "123"
            }
            """
        When the request sends POST
        Then the response status is UNAUTHORIZED
          And the response json at $.status is equal to 401
          And the response json at $.message is equal to "Unauthorized access."

  Scenario: 17 - Unauthorized access to the payment endpoint (Expired token)
    The request fails with a 401 Unauthorized if the client provides an expired authorization token.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${EXPIRED_TOKEN} |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123462",
              "cardHolder": "${VALID_CARD_HOLDER}",
              "cardNumber": "${VALID_CARD_NUMBER}",
              "amount": 100.50,
              "cardExpiryYear": "25",
              "cardExpiryMonth": "12",
              "cvv": "123"
            }
            """
        When the request sends POST
        Then the response status is UNAUTHORIZED
          And the response json at $.status is equal to 401
          And the response json at $.message is equal to "Token has expired."
