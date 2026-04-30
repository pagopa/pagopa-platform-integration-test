Feature: Checkout eCommerce — NPG payment gateway
  Validate the eCommerce checkout API flows for payment methods retrieval and fee computation.

  Background:
    Given that checkout host is configured through environment variable
    And the checkout NPG environment variables are configured

  # ---------------------------------------------------------------------------
  # Payment Methods
  # ---------------------------------------------------------------------------

  @checkout @npg @payment-methods @positive
  Scenario: All payment methods v1 are retrieved successfully
    When the user retrieves all payment methods v1
    Then the response has status code 200
    And the payment methods v1 response contains expected fields and brand assets

  @checkout @npg @payment-methods @positive
  Scenario: All payment methods v2 are retrieved successfully
    When the user retrieves all payment methods v2
    Then the response has status code 200
    And the payment methods v2 response contains expected fields

  @checkout @npg @payment-methods @positive
  Scenario: Credit card payment method details are retrieved
    Given the credit card payment method id is resolved
    When the user retrieves the credit card payment method details
    Then the response has status code 200
    And the payment method is CARDS with paymentTypeCode CP

  @checkout @npg @payment-methods @positive
  Scenario: Fee computation for credit card payment succeeds
    Given the credit card payment method id is resolved
    And an NPG session is created
    And a random valid notice code is generated
    And a transaction is created for the current session
    When the user computes the fee for credit card payment
    Then the response has status code 200
    And the fee response contains an enabled method with bundles
