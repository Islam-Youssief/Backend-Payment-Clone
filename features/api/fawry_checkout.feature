Feature: Fawry Payment Integration
  As a client of the payment API
  I want to process payments using the Fawry service
  So that I can complete checkout transactions securely

  Scenario: 1 - Successful Fawry payment processing
    Given a request url ${BASE_URL}/fawry/pay_with_visa
    And the request sends header Authorization with value "Bearer ${VALID_TOKEN}"
    And a request json payload
      """
      {
        "merchantRefNum": "ORDER_123456",
        "customerProfileId": "CUST_987",
        "amount": 100.50,
        "cardNumber": "4111111111111111",
        "cardExpiryYear": "25",
        "cardExpiryMonth": "12",
        "cvv": "123"
      }
      """
    When the request sends POST
    Then the response status is OK
    And the response json at $.statusCode is equal to 200
    And the response json at $.message is equal to "Operation done successfully"
    And the response json at $.orderStatus is equal to "PAID"

  Scenario: 2 - Payment fails due to missing required fields
    Given a request url ${BASE_URL}/fawry/pay_with_visa
    And the request sends header Authorization with value "Bearer ${VALID_TOKEN}"
    And a request json payload
      """
      {
        "amount": 100.50
      }
      """
    When the request sends POST
    Then the response status is BAD REQUEST
    And the response json at $.statusCode is equal to 400
    And the response json at $.message is equal to "Missing fields: ['merchantRefNum', 'cardNumber', 'cardExpiryYear', 'cardExpiryMonth', 'cvv']"

  Scenario: 3 - Payment fails due to invalid negative amount
    Given a request url ${BASE_URL}/fawry/pay_with_visa
    And the request sends header Authorization with value "Bearer ${VALID_TOKEN}"
    And a request json payload
      """
      {
        "merchantRefNum": "ORDER_123460",
        "amount": -50.00,
        "cardNumber": "4111111111111111",
        "cardExpiryYear": "25",
        "cardExpiryMonth": "12",
        "cvv": "123"
      }
      """
    When the request sends POST
    Then the response status is BAD REQUEST
    And the response json at $.statusCode is equal to 400
    And the response json at $.message is equal to "Amount must be greater than zero"

  Scenario: 4 - Payment fails due to invalid card number
    Given a request url ${BASE_URL}/fawry/pay_with_visa
    And the request sends header Authorization with value "Bearer ${VALID_TOKEN}"
    And a request json payload
      """
      {
        "merchantRefNum": "ORDER_123457",
        "amount": 100.50,
        "cardNumber": "4111",
        "cardExpiryYear": "25",
        "cardExpiryMonth": "12",
        "cvv": "123"
      }
      """
    When the request sends POST
    Then the response status is BAD REQUEST
    And the response json at $.statusCode is equal to 400
    And the response json at $.message is equal to "Invalid card number"

  Scenario: 5 - Payment fails due to invalid card expiry date
    Given a request url ${BASE_URL}/fawry/pay_with_visa
    And the request sends header Authorization with value "Bearer ${VALID_TOKEN}"
    And a request json payload
      """
      {
        "merchantRefNum": "ORDER_123457",
        "amount": 100.50,
        "cardNumber": "4111111111111111",
        "cardExpiryYear": "19",
        "cardExpiryMonth": "13",
        "cvv": "123"
      }
      """
    When the request sends POST
    Then the response status is BAD REQUEST
    And the response json at $.statusCode is equal to 400
    And the response json at $.message is equal to "Invalid card expiry date"

  Scenario: 6 - Payment fails due to invalid CVV
    Given a request url ${BASE_URL}/fawry/pay_with_visa
    And the request sends header Authorization with value "Bearer ${VALID_TOKEN}"
    And a request json payload
      """
      {
        "merchantRefNum": "ORDER_123457",
        "amount": 100.50,
        "cardNumber": "4111111111111111",
        "cardExpiryYear": "25",
        "cardExpiryMonth": "12",
        "cvv": "12A"
      }
      """
    When the request sends POST
    Then the response status is BAD REQUEST
    And the response json at $.statusCode is equal to 400
    And the response json at $.message is equal to "Invalid CVV"

  Scenario: 7 - Payment fails due to insufficient funds
    Given a request url ${BASE_URL}/fawry/pay_with_visa
    And the request sends header Authorization with value "Bearer ${VALID_TOKEN}"
    And a request json payload
      """
      {
        "merchantRefNum": "ORDER_123458",
        "amount": 999999.00,
        "cardNumber": "4111111111111111",
        "cardExpiryYear": "25",
        "cardExpiryMonth": "12",
        "cvv": "123"
      }
      """
    When the request sends POST
    Then the response status is PAYMENT REQUIRED
    And the response json at $.statusCode is equal to 402
    And the response json at $.message is equal to "Insufficient Balance"

  Scenario: 8 - Fawry service is currently unavailable or times out
    Given a request url ${BASE_URL}/fawry/pay_with_visa
    And the request sends header Authorization with value "Bearer ${VALID_TOKEN}"
    And a request json payload
      """
      {
        "merchantRefNum": "ORDER_123459",
        "amount": 100.50,
        "cardNumber": "5000000000000000",
        "cardExpiryYear": "25",
        "cardExpiryMonth": "12",
        "cvv": "123"
      }
      """
    When the request sends POST
    Then the response status is BAD GATEWAY
    And the response json at $.statusCode is equal to 502
    And the response json at $.message is equal to "External service unavailable"

  Scenario: 9 - Unauthorized access to the payment endpoint (Invalid token)
    Given a request url ${BASE_URL}/fawry/pay_with_visa
    And the request sends header Authorization with value "Bearer ${INVALID_TOKEN}"
    And a request json payload
      """
      {
        "merchantRefNum": "ORDER_123461",
        "amount": 100.50,
        "cardNumber": "4111111111111111",
        "cardExpiryYear": "25",
        "cardExpiryMonth": "12",
        "cvv": "123"
      }
      """
    When the request sends POST
    Then the response status is UNAUTHORIZED
    And the response json at $.statusCode is equal to 401
    And the response json at $.message is equal to "Unauthorized access."

  Scenario: 10 - Unauthorized access to the payment endpoint (Expired token)
    Given a request url ${BASE_URL}/fawry/pay_with_visa
    And the request sends header Authorization with value "Bearer ${EXPIRED_TOKEN}"
    And a request json payload
      """
      {
        "merchantRefNum": "ORDER_123461",
        "amount": 100.50,
        "cardNumber": "4111111111111111",
        "cardExpiryYear": "25",
        "cardExpiryMonth": "12",
        "cvv": "123"
      }
      """
    When the request sends POST
    Then the response status is UNAUTHORIZED
    And the response json at $.statusCode is equal to 401
    And the response json at $.message is equal to "Token has expired."
