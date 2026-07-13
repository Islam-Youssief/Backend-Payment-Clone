Feature: Stripe Payment Processing

  Validate the Stripe payment endpoint for successful payments,
  declined cards, missing credentials, invalid credentials,
  server failures, and rate limiting.

  Scenario: 1. Successful create a stripe payment
    Given the Stripe API is available
    When the customer creates a payment
    Then the response status code is equal to 200
      And the response message is equal to "Payment Successful"
      And the payment status is equal to "succeeded"
      And the payment amount is equal to 100
      And the payment id is not empty

  Scenario: 2. Reject payment when the card is declined
    Given the Stipe API declines the payment
    When the customer creates a payment
    Then the response status code is equal to 402
      And the response message is equal to "Card declined"

  Scenario: 3. Return an error when the Stripe service is unavailable
    Given the Stripe API is unavailable
    When the customer creates a payment
    Then the response status code is equal to 500
      And the response message is equal to "Payment server unavailable"

  Scenario: 4. Return rate limit response when too many requests are sent
    Given the Stripe API is rate limiting requests
    When the customer creates a payment
    Then the response status code is equal to 429
      And the response message is equal to "Too Many Requests"

  Scenario: 6. Reject payment when the secret key is missing
    Given the Stripe secret key is missing
    When the customer creates a payment
    Then the response status code is equal to 401
      And the response message is equal to "Unauthorized"

  Scenario: 5. Reject payment when the secret key is invalid
    Given the Stripe secret key is invalid
    When the customer creates a payment
    Then the response status code is equal to 401
     And the response message is equal to "Unauthorized"

