
Feature: PayPal Payment API
  Test possible scenarios for paying with visa via PayPal endpoints,
  Some scenarios include having payments with
    - Valid credentials, invalid credentials, expired credentials, and missing credentials.
    - Missing the amount, missing the currency, and missing the payment method.
    - PayPal API errors, such as 400 Bad Request, 401 Unauthorized, and 500 Internal Server Error.

  Scenario: 1 - Successfully retrieve payment invoice after a successful payment
    Customers can retrieve their payment invoice after a successful payment if he has valid token, 
    valid payment information, and the payment is successful from the PayPal Server side.
    
    Given a request url ${BASE_URL}/api/payments/paypal
        And request headers
            | param         | value         |
            | Authorization | DUMMY-FOR-NOW |
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
        Then the response status is CREATED
          And the response json at $.message is equal to "You have successfully paid with visa"
          And the response json at $.status is equal to "success"
          And the response json at $.transaction_id is equal to "1234567890"
          And the response json at $.amount is equal to "100.00"
          And the response json at $.currency is equal to "USD"
          And the response json at $.payment_method is equal to "visa"
    

    # TODO: Add the other scenarios