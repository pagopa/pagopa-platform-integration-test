# language: en
Feature: Login option availability at all stages of the payment flow.
  As a checkout user
  I want to verify that the login option is available at various stages of the payment flow

  Background:
    Given The checkout page is open
    And The language is set to "it"

  Scenario: Login option available when entering notice data
    When The user enters the notice data
    Then The login button is visible and enabled
    And The login button title is “Accedi”

  Scenario: Login option available when entering payment data
    When The user enters the notice data
    And The user enters the payment data
    Then The login button is visible and enabled
    And The login button title is “Accedi”

  Scenario: Login option available when entering entering email
    When The user enters the notice data
    And The user enters the payment data
    And The user enters the email
    Then The login button is visible and enabled
    And The login button title is “Accedi”

  Scenario: login option available when selecting payment method
    When The user enters the notice data
    And The user enters the payment data
    And The user enters the email
    And The user select the payment method
    Then The login button is visible and enabled
    And The login button title is “Accedi”
