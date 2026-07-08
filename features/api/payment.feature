Feature: Stripe Payment

  Scenario: Successful payment
    Given the Stripe API is available
    When the customer creates a payment
    Then the response status code is equal to 200
    And the response message is equal to "Payment Successful"

  Scenario: Card declined
    Given the Stipe API declines the payment
    When the customer creates a payment
    Then the response status code is equal to 402
    And the response message is equal to "Card declined"

  Scenario: Stripe server error
    Given the Stripe API is unavailable
    When the customer creates a payment
    Then the response status code is equal to 500
    And the response message is equal to "Payment server unavailable"

  Scenario: Missing secret key
    Given the Stripe secret key is missing
    When the customer creates a payment
    Then the response status code is equal to 401
    And the response message is equal to "Unauthorized"

  Scenario: Invalid secret key
    Given the Stripe secret key is invalid
    When the customer creates a payment
    Then the response status code is equal to 401
    And the response message is equal to "Unauthorized"

  Scenario: Too many requests from Stripe
    Given the Stripe API is rate limiting requests
    When the customer creates a payment
    Then the response status code is equal to 429
    And the response message is equal to "Too Many Requests"
