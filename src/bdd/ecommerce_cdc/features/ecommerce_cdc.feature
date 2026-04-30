# language: en
Feature: eCommerce CDC service
  Validate the eCommerce CDC (Change Data Capture) service by driving the full Checkout
  payment flow and verifying that each transaction status change is correctly propagated
  through the CDC pipeline.

  Tests migrated from the Postman collection "eCommerce CDC service".

  The flow polls GET /transactions after each mutating operation to confirm async CDC
  propagation before moving to the next step.

  Background:
    Given the eCommerce CDC environment variables are configured

  # ---------------------------------------------------------------------------
  # Delete transaction — CANCELED status check
  # ---------------------------------------------------------------------------

  @cdc @transaction @cancel @positive
  Scenario: ACTIVATED transaction is canceled and reaches CANCELED status
    Given a random CDC notice code is generated
    When the user creates a CDC transaction with a static order id
    And the user deletes the CDC transaction
    Then the CDC response has status code 202
    And the transaction status reaches "CANCELED" via polling

  # ---------------------------------------------------------------------------
  # NPG session creation
  # ---------------------------------------------------------------------------

  @cdc @session @positive
  Scenario: NPG card session is created with expected card form fields
    Given the CDC credit card payment method id is resolved
    When the user creates a CDC NPG card session
    Then the CDC response has status code 200
    And the NPG session contains four card form fields
    And the NPG session has payment method CARDS
    And the NPG session has a valid order id

  # ---------------------------------------------------------------------------
  # Transaction creation — ACTIVATED status check
  # ---------------------------------------------------------------------------

  @cdc @transaction @activated @positive
  Scenario: New transaction reaches ACTIVATED status
    Given the CDC credit card payment method id is resolved
    And a CDC NPG session is prepared
    And a random CDC notice code is generated
    When the user creates a CDC transaction for the current session
    Then the CDC response has status code 200
    And the transaction response has status ACTIVATED
    And the transaction response has a valid transactionId and authToken
    And the transaction payments have the expected structure
    And the transaction status reaches "ACTIVATED" via polling

  # ---------------------------------------------------------------------------
  # Payment method details
  # ---------------------------------------------------------------------------

  @cdc @payment-methods @positive
  Scenario: Credit card payment method details are correctly retrieved
    Given the CDC credit card payment method id is resolved
    When the user retrieves the CDC payment method details
    Then the CDC response has status code 200
    And the payment method has name "CARDS" and paymentTypeCode "CP"
    And the payment method has a non-empty asset and ranges

  # ---------------------------------------------------------------------------
  # Fee computation
  # ---------------------------------------------------------------------------

  @cdc @fees @positive
  Scenario: PSP fee bundles are retrieved for credit card payment
    Given the CDC credit card payment method id is resolved
    And a CDC NPG session is prepared
    And a random CDC notice code is generated
    And a CDC transaction is created for the current session
    When the user computes the CDC fee for credit card payment
    Then the CDC response has status code 200
    And the fee response has paymentMethodStatus "ENABLED"
    And the fee response has belowThreshold false
    And the fee response has non-empty bundles

  # ---------------------------------------------------------------------------
  # All payment methods — brand assets
  # ---------------------------------------------------------------------------

  @cdc @payment-methods @positive
  Scenario: All payment methods v1 include expected brand assets
    When the user retrieves all CDC payment methods v1
    Then the CDC response has status code 200
    And the payment methods list is not empty
    And the credit card methods have VISA and Mastercard brand assets

  # ---------------------------------------------------------------------------
  # Full CDC flow — request authorization → AUTHORIZATION_REQUESTED
  # ---------------------------------------------------------------------------

  @cdc @authorization @positive @e2e
  Scenario: Full CDC flow ends with transaction in AUTHORIZATION_REQUESTED status
    Given the CDC credit card payment method id is resolved
    And a CDC NPG session is prepared
    And the NPG cookies are populated
    And a random CDC notice code is generated
    And a CDC transaction is created for the current session
    And the transaction status reaches "ACTIVATED" via polling
    And the card data matches the test card values after filling NPG fields
    When the user requests CDC authorization for the transaction
    Then the CDC response has status code 200
    And the authorization response has a valid authorizationUrl
    And the authorization requestId matches the current order id
    And the transaction status reaches "AUTHORIZATION_REQUESTED" via polling
