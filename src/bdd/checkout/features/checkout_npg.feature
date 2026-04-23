Feature: Checkout eCommerce API — NPG
  Validate the eCommerce checkout API flows with NPG payment gateway.
  Tests migrated from the Postman collection "Ecommerce for Checkout API - NPG".

  Background:
    Given that checkout host is configured through environment variable
    And the checkout NPG environment variables are configured

  # ---------------------------------------------------------------------------
  # Payment Verification
  # ---------------------------------------------------------------------------

  @checkout @npg @payment-verify @positive
  Scenario: Successful payment verification returns payment data
    Given a random valid notice code is generated
    When I verify the payment request for the valid notice code
    Then the response has status code 200
    And the payment verification response contains valid payment data

  @checkout @npg @payment-verify @negative
  Scenario: Payment verification returns 404 for unknown PA domain
    When I verify the payment request for the unknown domain notice code
    Then the response has status code 404
    And the fault code detail contains "PPT_DOMINIO_SCONOSCIUTO"

  @checkout @npg @payment-verify @negative
  Scenario: Payment verification returns 404 for unknown station
    When I verify the payment request for the unknown station notice code
    Then the response has status code 404
    And the fault code detail equals "PPT_STAZIONE_INT_PA_SCONOSCIUTA"

  # ---------------------------------------------------------------------------
  # Payment Methods
  # ---------------------------------------------------------------------------

  @checkout @npg @payment-methods @positive
  Scenario: All payment methods v1 are retrieved successfully
    When I get all payment methods v1
    Then the response has status code 200
    And the payment methods v1 response contains expected fields and brand assets

  @checkout @npg @payment-methods @positive
  Scenario: All payment methods v2 are retrieved successfully
    When I post all payment methods v2
    Then the response has status code 200
    And the payment methods v2 response contains expected fields

  @checkout @npg @payment-methods @positive
  Scenario: Credit card payment method details are retrieved
    Given the credit card payment method id is resolved
    When I get the credit card payment method details
    Then the response has status code 200
    And the payment method is CARDS with paymentTypeCode CP

  @checkout @npg @payment-methods @positive
  Scenario: Fee computation for credit card payment succeeds
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    And a transaction is created for the current session
    When I compute the fee for credit card payment
    Then the response has status code 200
    And the fee response contains an enabled method with bundles

  # ---------------------------------------------------------------------------
  # NPG Session Creation (by language)
  # ---------------------------------------------------------------------------

  @checkout @npg @session @positive
  Scenario Outline: NPG card session is created successfully for each language
    Given the credit card payment method id is resolved
    When I create an NPG card session with language "<lang>"
    Then the response has status code 200
    And the NPG session response contains valid card form fields with payment method CARDS

    Examples:
      | lang |
      | it   |
      | fr   |
      | de   |
      | sl   |
      | en   |

  # ---------------------------------------------------------------------------
  # Transactions
  # ---------------------------------------------------------------------------

  @checkout @npg @transaction @negative
  Scenario: Create transaction fails when order id is missing
    Given a random valid notice code is generated
    When I create a transaction without order id
    Then the response has status code 400

  @checkout @npg @transaction @positive
  Scenario: Create transaction with mixed case email succeeds
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    When I create a transaction with mixed case email
    Then the response has status code 200
    And the transaction response is in ACTIVATED status for checkout client

  @checkout @npg @transaction @positive
  Scenario: Create transaction with standard email succeeds and cached payment is still valid
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    When I create a transaction with standard email
    Then the response has status code 200
    And the transaction response is in ACTIVATED status for checkout client
    When I verify the cached payment request
    Then the response has status code 200
    And the cached payment verification returns valid payment data

  # ---------------------------------------------------------------------------
  # NPG Card Data
  # ---------------------------------------------------------------------------

  @checkout @npg @card @positive
  Scenario: Card data is retrieved successfully after filling NPG fields
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    And a transaction is created for the current session
    And the NPG card fields are filled with test card data
    When I get the card data for the current session
    Then the response has status code 200
    And the card data matches the test card values

  @checkout @npg @card @negative
  Scenario: Get card data returns 401 for mismatched order id
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    And a transaction is created for the current session
    When I get the card data with a wrong order id
    Then the response has status code 401

  @checkout @npg @card @negative
  Scenario: Get card data returns 401 for mismatched transaction id
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    And a transaction is created for the current session
    When I get the card data with a wrong transaction id
    Then the response has status code 401

  @checkout @npg @card @negative
  Scenario: Get card data returns 401 when auth token is missing
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    And a transaction is created for the current session
    When I get the card data without auth token
    Then the response has status code 401

  # ---------------------------------------------------------------------------
  # Authorization Requests
  # ---------------------------------------------------------------------------

  @checkout @npg @authorization @negative
  Scenario Outline: Authorization request returns 401 when JWT token is absent
    Given the credit card payment method id is resolved
    And an NPG session is created with language "<lang>"
    And a random valid notice code is generated
    And a transaction is created for the current session
    When I request authorization without JWT token using language "<lang>"
    Then the response has status code 401

    Examples:
      | lang |
      | it   |
      | fr   |
      | de   |
      | sl   |
      | en   |

  @checkout @npg @authorization @positive
  Scenario: Authorization request with JWT token returns authorization URL
    Given the credit card payment method id is resolved
    And an NPG session is created with language "it"
    And a random valid notice code is generated
    And a transaction is created for the current session
    And the NPG card fields are filled with test card data
    When I request authorization with JWT token using language "it"
    Then the response has status code 200
    And the authorization response contains a valid authorization URL
    And the authorization request id matches the order id

  # ---------------------------------------------------------------------------
  # Transaction Status after Authorization
  # ---------------------------------------------------------------------------

  @checkout @npg @transaction @positive
  Scenario: Get transaction v1 returns AUTHORIZATION_REQUESTED status
    Given the full NPG authorization flow is executed
    When I get the transaction by id v1
    Then the response has status code 200
    And the transaction v1 status is AUTHORIZATION_REQUESTED
    And the transaction v1 gateway is NPG

  @checkout @npg @transaction @positive
  Scenario: Get transaction outcomes v1 returns a valid outcome code
    Given the full NPG authorization flow is executed
    When I get the transaction outcomes v1
    Then the response has status code 200
    And the outcomes response contains a valid outcome code

  @checkout @npg @transaction @positive
  Scenario: Get transaction v2 returns AUTHORIZATION_REQUESTED status with gateway info
    Given the full NPG authorization flow is executed
    When I get the transaction by id v2
    Then the response has status code 200
    And the transaction v2 status is AUTHORIZATION_REQUESTED
    And the transaction v2 gatewayInfo is NPG

  # ---------------------------------------------------------------------------
  # Delete Transaction
  # ---------------------------------------------------------------------------

  @checkout @npg @transaction @positive
  Scenario: Transaction in ACTIVATED status is canceled successfully
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    And a transaction is created for the current session
    When I delete the transaction
    Then the response has status code 202
