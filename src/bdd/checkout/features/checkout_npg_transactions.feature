Feature: Checkout eCommerce — NPG payment gateway
  Validate the eCommerce checkout API flows for transaction lifecycle management.

  Background:
    Given that checkout host is configured through environment variable
    And the checkout NPG environment variables are configured

  # ---------------------------------------------------------------------------
  # Transactions
  # ---------------------------------------------------------------------------

  @checkout @npg @transaction @negative
  Scenario: Create transaction fails when order id is missing
    Given a random valid notice code is generated
    When the user creates a transaction without order id
    Then the response has status code 400

  @checkout @npg @transaction @positive
  Scenario: Create transaction with mixed case email succeeds
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    When the user creates a transaction with mixed case email
    Then the response has status code 200
    And the transaction response is in ACTIVATED status for checkout client

  @checkout @npg @transaction @positive
  Scenario: Create transaction with standard email succeeds and cached payment is still valid
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    When the user creates a transaction with standard email
    Then the response has status code 200
    And the transaction response is in ACTIVATED status for checkout client
    When the user verifies the cached payment
    Then the response has status code 200
    And the cached payment verification returns valid payment data

  @checkout @npg @transaction @positive
  Scenario: Transaction in ACTIVATED status is canceled successfully
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    And a transaction is created for the current session
    When the user deletes the transaction
    Then the response has status code 202

  @checkout @npg @transaction @positive
  Scenario: Get transaction v1 returns AUTHORIZATION_REQUESTED status
    Given the full NPG authorization flow is executed
    When the user retrieves the transaction by id v1
    Then the response has status code 200
    And the transaction v1 status is AUTHORIZATION_REQUESTED
    And the transaction v1 gateway is NPG

  @checkout @npg @transaction @positive
  Scenario: Get transaction outcomes v1 returns a valid outcome code
    Given the full NPG authorization flow is executed
    When the user retrieves the transaction outcomes v1
    Then the response has status code 200
    And the outcomes response contains a valid outcome code

  @checkout @npg @transaction @positive
  Scenario: Get transaction v2 returns AUTHORIZATION_REQUESTED status with gateway info
    Given the full NPG authorization flow is executed
    When the user retrieves the transaction by id v2
    Then the response has status code 200
    And the transaction v2 status is AUTHORIZATION_REQUESTED
    And the transaction v2 gatewayInfo is NPG
