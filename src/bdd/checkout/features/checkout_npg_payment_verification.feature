Feature: Checkout eCommerce — NPG payment gateway
  Validate the eCommerce checkout API flows for payment verification.

  Background:
    Given that checkout host is configured through environment variable
    And the checkout NPG environment variables are configured

  # ---------------------------------------------------------------------------
  # Payment Verification
  # ---------------------------------------------------------------------------

  @checkout @npg @payment-verify @positive
  Scenario: Successful payment verification returns payment data
    Given a random valid notice code is generated
    When the user verifies the payment for the valid notice code
    Then the response has status code 200
    And the payment verification response contains valid payment data

  @checkout @npg @payment-verify @negative
  Scenario: Payment verification returns 404 for unknown PA domain
    When the user verifies the payment for the unknown domain notice code
    Then the response has status code 404
    And the fault code detail contains "PPT_DOMINIO_SCONOSCIUTO"

  @checkout @npg @payment-verify @negative
  Scenario: Payment verification returns 404 for unknown station
    When the user verifies the payment for the unknown station notice code
    Then the response has status code 404
    And the fault code detail equals "PPT_STAZIONE_INT_PA_SCONOSCIUTA"
