Feature: Stripe Payment Processing

  Validate the Stripe payment endpoint for successful payments,
  declined cards, missing credentials, invalid credentials,
  server failures, and rate limiting.

  Scenario: 1. Successful retrieve payment invoice after a successful payment
    customer can retrieve their payment invoice after a successful payment
    if he has valid secret key,valid payment information, and the payment is successful
    from the Stripe Server side

    Given a request url ${BASE_URL}/api/payments/stripe
        And request headers
            | param         | value         |
            | Authorization | Bearer STRIPE_SECRET_KEY |
            | X-Test-Scenario | successful-payment |
        And a request json payload
          """
          {
              "cardHolder":"${VALID_CARD_HOLDER}",
              "cardNumber":"${VALID_CARD_NUMBER}",
              "amount":100,
              "cardExpiryYear":"25",
              "cardExpiryMonth":"12",
              "cvv":"123"
          }
          """
    When the request sends POST
    Then the response status is CREATED
      And the response json at $.message is equal to "You have successfully paid with visa"
      And the response json at $.status is equal to "success"
      And the response json at $.transaction_id is equal to "1234567890"
      And the response json at $.amount is equal to "100.00"
      And the response json at $.currency is equal to "USD"
      And the response json at $.payment_method is equal to "visa"

  Scenario: 2. Return a declined payment response when the card is declined
    The customer receives a declined payment response
    after using a declined card and a valid Stripe secret key.

    Given a request url ${BASE_URL}/api/payments/stripe
        And request headers
            | param         | value         |
            | Authorization | Bearer STRIPE_SECRET_KEY |
            | X-Test-Scenario | declined-payment |
        And a request json payload
          """
          {
              "cardHolder":"${VALID_CARD_HOLDER}",
              "cardNumber":"${INVALID_CARD_NUMBER}",
              "amount":100,
              "cardExpiryYear":"25",
              "cardExpiryMonth":"12",
              "cvv":"123"
          }
          """
    When the request sends POST
    Then the response status is PAYMENT_REQUIRED
      And the response json at $.message is equal to "Reject The Payment Card Declined"
      And the response json at $.status is equal to "declined"

  Scenario: 3. Return an error when the Stripe service is unavailable
    Test the application's behavior when the Stripe API cannot be reached
    or returns an internal server error.

    Given a request url ${BASE_URL}/api/payments/stripe
        And request headers
            | param         | value         |
            | Authorization | Bearer STRIPE_SECRET_KEY |
            | X-Test-Scenario | error-stripe-service |

        And a request json payload
          """
          {
              "cardHolder":"${VALID_CARD_HOLDER}",
              "cardNumber":"${SERVER_ERROR_CARD_NUMBER}",
              "amount":100,
              "cardExpiryYear":"25",
              "cardExpiryMonth":"12",
              "cvv":"123"
          }
          """
    When the request sends POST
    Then the response status is INTERNAL_SERVER_ERROR
      And the response json at $.message is equal to "Payment server unavailable"
      And the response json at $.status is equal to "server_error"


  Scenario: 4 Reject request when the rate limit is exceeded
    Verify that the application rejects requests
    after the client exceeds the allowed request limit.

  Given a request url ${BASE_URL}/api/payments/stripe
    And request headers
      | param           | value                    |
      | Authorization | Bearer STRIPE_SECRET_KEY   |
      | X-Test-Scenario | RATE_LIMIT               |
    And a request json payload
    """
    {
        "cardHolder":"${VALID_CARD_HOLDER}",
        "cardNumber":"${RATE_LIMIT}",
        "amount":100,
        "cardExpiryYear":"25",
        "cardExpiryMonth":"12",
        "cvv":"123"
    }
    """
  When the client sends 6 POST requests
  Then the response status is TOO_MANY_REQUESTS
    And the response json at $.message is equal to "Too many requests"

  Scenario: 5. Reject payment when the secret key is invalid
    Verify that the application rejects the payment request
    after an invalid Stripe secret key is provided.

  Given a request url ${BASE_URL}/api/payments/stripe
    And request headers
      | param         | value                        |
      | Authorization | Bearer INVALID_SECRET_KEY    |
      | X-Test-Scenario | secret-key-is-invalid |
    And a request json payload
      """
      {
          "cardHolder": "${VALID_CARD_HOLDER}",
          "cardNumber": "${VALID_CARD_NUMBER}",
          "amount": 100,
          "cardExpiryYear": "25",
          "cardExpiryMonth": "12",
          "cvv": "123"
      }
      """
    When the request sends POST
      Then the response status is UNAUTHORIZED
        And the response json at $.message is equal to "Unauthorized"
        And the response json at $.status is equal to "invalid_secret"

  Scenario: 6. Reject payment when the secret key is missing
    Verify that the application rejects the payment request
    after the Stripe secret key is missing.

  Given a request url ${BASE_URL}/api/payments/stripe
    And request headers
      | param         | value                        |
      | Authorization | Bearer None                  |
      | X-Test-Scenario | secret-key-is-missing |
    And a request json payload
      """
      {
          "cardHolder": "${VALID_CARD_HOLDER}",
          "cardNumber": "${VALID_CARD_NUMBER}",
          "amount": 100,
          "cardExpiryYear": "25",
          "cardExpiryMonth": "12",
          "cvv": "123"
      }
      """
  When the request sends POST
  Then the response status is UNAUTHORIZED
    And the response json at $.message is equal to "Unauthorized"
    And the response json at $.status is equal to "unauthorized"

