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
            | X-Idempotency-Key | 46a71704-4040-4664-be11-6a146994bd06 |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123456",
              "customerProfileId": "CUST_987",
              "amount": 100.50,
              "customerEmail": "tester@test.com",
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



  Scenario: 2 - Payment fails due to missing amount
    The request fails with a 400 Bad Request if the amount field is missing from the payload.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
            | X-Idempotency-Key | 4f489a31-f386-42a7-85c6-22b84f9fd1be |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123456",
              "customerProfileId": "CUST_987",
              "customerEmail": "tester@test.com",
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

  Scenario: 3 - Payment fails due to missing cardNumber
    The request fails with a 400 Bad Request if the cardNumber field is missing from the payload.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
            | X-Idempotency-Key | 56f657c8-6d9c-41f8-a13d-6f25c1966075 |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123456",
              "customerProfileId": "CUST_987",
              "customerEmail": "tester@test.com",
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



  Scenario: 4 - Payment fails due to missing cvv
    The request fails with a 400 Bad Request if the cvv field is missing from the payload.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
            | X-Idempotency-Key | 2bad3b01-7e71-40e0-b9fa-67e07971cbdf |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123456",
              "customerProfileId": "CUST_987",
              "amount": 100.50,
              "customerEmail": "tester@test.com",
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

  Scenario: 5 - Payment fails due to invalid negative amount
    The request fails with a 400 Bad Request if the payment amount is negative or zero.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
            | X-Idempotency-Key | e4f94dfd-b81c-49e9-97b7-0e10d43e6e26 |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123460",
              "amount": -50.00,
              "customerEmail": "tester@test.com",
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

  Scenario: 6 - Payment fails due to zero amount
    The request fails with a 400 Bad Request if the payment amount is zero.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
            | X-Idempotency-Key | b0e5da2f-73a6-4799-9f46-f820f193ec2c |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123460",
              "amount": 0,
              "customerEmail": "tester@test.com",
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

  Scenario: 7 - Payment fails due to invalid card number
    The request fails with a 400 Bad Request if the card number is not exactly 16 digits or contains non-numeric characters.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
            | X-Idempotency-Key | 5d9c04ba-8e3a-44c6-8c7d-d859d14f06f3 |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123457",
              "amount": 100.50,
              "customerEmail": "tester@test.com",
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



  Scenario: 8 - Payment fails due to invalid CVV
    The request fails with a 400 Bad Request if the CVV is not exactly 3 digits or contains non-numeric characters.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
            | X-Idempotency-Key | 48f2702f-1541-413f-87b5-d05db0373932 |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123457",
              "amount": 100.50,
              "customerEmail": "tester@test.com",
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

  Scenario: 9 - Payment fails due to insufficient funds
    The request fails with a 402 Payment Required when the card does not have sufficient balance to complete the transaction.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
            | X-Idempotency-Key | b7e4a54d-2126-4f1a-87c3-c558b341ccf5 |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123458",
              "amount": 999999.00,
              "customerEmail": "tester@test.com",
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

  Scenario: 10 - Fawry service is currently unavailable or returns Bad Gateway
    The request fails with a 502 Bad Gateway if the external Fawry service is down or returns a connection error.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
            | X-Idempotency-Key | 08475dcb-0b4c-4e3a-a694-03d01a19cf8c |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123459",
              "amount": 100.50,
              "customerEmail": "tester@test.com",
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

  Scenario: 11 - Fawry service returns an internal server error
    The request fails with a 502 Bad Gateway if the external Fawry service encounters an internal server error.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
            | X-Idempotency-Key | 1bff152c-f9ac-4998-bf5a-db1696cbc7a8 |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123463",
              "amount": 100.50,
              "customerEmail": "tester@test.com",
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

  Scenario: 12 - Fawry service request times out
    The request fails with a 504 Gateway Timeout if the external Fawry service times out.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${VALID_TOKEN}  |
            | X-Idempotency-Key | 6c44763c-1c64-425c-a6d4-7bb905094eee |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123464",
              "amount": 100.50,
              "customerEmail": "tester@test.com",
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

  Scenario: 13 - Unauthorized access to the payment endpoint (Invalid token)
    The request fails with a 401 Unauthorized if the client provides an invalid authorization token.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${INVALID_TOKEN} |
            | X-Idempotency-Key | 256f920b-349f-4ead-87ac-f12adeda4e6a |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123461",
              "customerEmail": "tester@test.com",
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

  Scenario: 14 - Unauthorized access to the payment endpoint (Expired token)
    The request fails with a 401 Unauthorized if the client provides an expired authorization token.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                  |
            | Authorization | Bearer ${EXPIRED_TOKEN} |
            | X-Idempotency-Key | f2d4d318-e7eb-4b8d-96b1-f9aed5f5c20f |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123462",
              "customerEmail": "tester@test.com",
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

  Scenario: 15 - Unauthorized access to the payment endpoint (Token is missing permissions)
    The request fails with a 401 Unauthorized if the client provides a token that is missing permissions.

    Given a request url ${BASE_URL}/api/payments/fawry
        And request headers
            | param         | value                                |
            | Authorization | Bearer ${MISSING_PERMISSIONS_TOKEN} |
            | X-Idempotency-Key | 3c4cf697-0d7b-435d-8fbb-292c854fdfa4 |
        And a request json payload
            """
            {
              "merchantRefNum": "ORDER_123463",
              "customerEmail": "tester@test.com",
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
          And the response json at $.message is equal to "Token is missing permissions"

