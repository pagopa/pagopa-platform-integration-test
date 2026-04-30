Feature: Checkout eCommerce — NPG payment gateway
  Validate the eCommerce checkout API flows for NPG card data retrieval and validation.

  Background:
    Given that checkout host is configured through environment variable
    And the checkout NPG environment variables are configured

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
    When the user retrieves the card data for the current session
    Then the response has status code 200
    And the card data matches the test card values

  @checkout @npg @card @negative
  Scenario: Get card data returns 401 for mismatched order id
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    And a transaction is created for the current session
    When the user retrieves the card data with a wrong order id
    Then the response has status code 401

  @checkout @npg @card @negative
  Scenario: Get card data returns 401 for mismatched transaction id
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    And a transaction is created for the current session
    When the user retrieves the card data with a wrong transaction id
    Then the response has status code 401

  @checkout @npg @card @negative
  Scenario: Get card data returns 401 when auth token is missing
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    And a transaction is created for the current session
    When the user retrieves the card data without auth token
    Then the response has status code 401
