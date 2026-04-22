# language: en
Feature: Cart API - Payment cart creation
  As a content creditor (EC)
  I want to create a payment cart through the PagoPA Checkout API
  In order to start the payment flow and get a checkout redirect

  Background:
    Given that checkout host is configured through environment variable

  Scenario: Post cart OK - Valid cart creation with one payment notice
    Given a valid random notice code generated from the prefix configured in "NOTICE_CODE_PREFIX"
    And a valid PA fiscal code configured in "VALID_FISCAL_CODE_PA"
    When I send a POST to "/checkout/ec/v1/carts" with cart data and email "test@test.it"
    Then the response has status code 302
    And the response contains the header "location"
    And the CART_ID is extracted from the header "location"

  Scenario: Post cart OK - Cart creation with uppercase email
    Given a valid random notice code generated from the prefix configured in "NOTICE_CODE_PREFIX"
    And a valid PA fiscal code configured in "VALID_FISCAL_CODE_PA"
    When I send a POST to "/checkout/ec/v1/carts" with cart data and email "TEST@test.IT"
    Then the response has status code 302
    And the response contains the header "location"
    And the CART_ID is extracted from the header "location"

  Scenario: Post cart KO - Invalid request (malformed body)
    When I send a POST to "/checkout/ec/v1/carts" with invalid body
    Then the response has status code 400

  Scenario: Post cart KO - Number of payment notices exceeds maximum allowed
    When I send a POST to "/checkout/ec/v1/carts" with 6 payment notices
    Then the response has status code 400
