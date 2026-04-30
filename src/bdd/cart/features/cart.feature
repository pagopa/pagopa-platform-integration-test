# language: en
Feature: Payment cart creation
  As an Ente Creditore (EC)
  the system exposes the PagoPA Checkout cart endpoint
  so that a payment flow can be started and a checkout redirect is returned

  Background:
    Given that checkout host is configured through environment variable

  @cart @checkout @positive
  Scenario: Valid cart creation with one payment notice
    Given a valid random notice code generated from the prefix configured in "NOTICE_CODE_PREFIX"
    And a valid PA fiscal code configured in "VALID_FISCAL_CODE_PA"
    When the user submits a cart with email "test@test.it"
    Then the response has status code 302
    And the response contains the header "location"
    And the cart id is extracted from the header "location"

  @cart @checkout @positive
  Scenario: Cart creation with uppercase email
    Given a valid random notice code generated from the prefix configured in "NOTICE_CODE_PREFIX"
    And a valid PA fiscal code configured in "VALID_FISCAL_CODE_PA"
    When the user submits a cart with email "TEST@test.IT"
    Then the response has status code 302
    And the response contains the header "location"
    And the cart id is extracted from the header "location"

  @cart @checkout @negative
  Scenario: Cart creation fails with malformed body
    When the user submits a cart with an invalid body
    Then the response has status code 400

  @cart @checkout @negative
  Scenario: Cart creation fails when notices exceed maximum allowed
    When the user submits a cart with 6 payment notices
    Then the response has status code 400
