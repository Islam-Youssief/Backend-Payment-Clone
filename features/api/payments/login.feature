Feature: Login Authentication

  Test the login endpoint under different authentication scenarios,
  including successful login, invalid credentials,
  invalid tokens, and expired tokens.

   Scenario: 1. Successful login request when valid credential
     Verify that the application authenticates the user successfully
     after valid login credentials are provided.

     Given a request url ${BASE_URL}/api/payments/login
        And request headers
           |param                  |value                    |
           |Authorization          |Bearer VALID_TOKEN     |
        And a request json payload
        """
        {
        "email":"${VALID_EMAIL}",
        "password":"${VALID_PASSWORD}"
        }
        """
     When the request sends POST
     Then the response status is CREATED
        And the response json at $.message is equal to "You have successful login"
        And the response json at $.status is equal to "success"

   Scenario: 2. Reject login request when the access token is invalid
     Verify that the application rejects the request When an invalid
     access token is provided

     Given a request url ${BASE_URL}/api/payments/login
        And request headers
           |param                  |value                    |
           |Authorization          |Bearer INVALID_TOKEN     |
        And a request json payload
        """
        {
        "email":"${VALID_EMAIL}",
        "password":"${VALID_PASSWORD}"
        }
        """
     When the request sends POST
     Then the response status is UNAUTHORIZED
        And the response json at $.message is equal to "Unauthorized"
        And the response json at $.status is equal to "invalid_token"

   Scenario: 3. Reject login request when the access token has expired
    Verify that the application rejects the request when an
    expired access token is provided.

    Given a request url ${BASE_URL}/api/payments/login
      And request headers
        | param         | value                |
        | Authorization | Bearer EXPIRED_TOKEN |
      And a request json payload
        """
        {
          "email": "${VALID_EMAIL}",
          "password": "${VALID_PASSWORD}"
        }
        """
    When the request sends POST
    Then the response status is UNAUTHORIZED
      And the response json at $.message is equal to "Token expired"
      And the response json at $.status is equal to "expired_token"

   Scenario: 4. Reject login request when  credentials are invalid
     Verify that the application returns a 401 Unauthorized response
      after invalid login credentials are used.

     Given a request url ${BASE_URL}/api/payments/login
        And request headers
           |param                  |value                    |
           |Authorization          |Bearer VALID_TOKEN     |
        And a request json payload
        """
        {
        "email":"${VALID_EMAIL}",
        "password":"${INVALID_PASSWORD}"
        }
        """
     When the request sends POST
     Then the response status is UNAUTHORIZED
        And the response json at $.message is equal to "password or Email is wrong"
        And the response json at $.status is equal to "invalid_credentials"

   Scenario: 5. Reject login request when the permission token is missing
      Verify that the application rejects the login request
      after the authorization token is missing.

     Given a request url ${BASE_URL}/api/payments/login
        And request headers
           |param                  |value                    |
           |Authorization          |                         |
        And a request json payload
        """
        {
        "email":"${VALID_EMAIL}",
        "password":"${VALID_PASSWORD}"
        }
        """
     When the request sends POST
     Then the response status is FORBIDDEN
        And the response json at $.message is equal to "Permission token is missing"
        And the response json at $.status is equal to "missing_permission_token"

   Scenario: 6. Reject login request when the access token is invalid for the user
      Verify that the application rejects the login request
      after invalid access token is provided for the user.

     Given a request url ${BASE_URL}/api/payments/login
        And request headers
           |param                  |value                           |
           |Authorization          |Bearer INVALID_USER_TOKEN       |
        And a request json payload
        """
        {
        "email":"${VALID_EMAIL}",
        "password":"${VALID_PASSWORD}"
        }
        """
     When the request sends POST
     Then the response status is UNAUTHORIZED
        And the response json at $.message is equal to "Invalid user token"
        And the response json at $.status is equal to "invalid_user_token"


