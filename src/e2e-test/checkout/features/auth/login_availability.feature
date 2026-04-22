# language: en
Feature: Login Availability during Payment Flow
  As a checkout user
  I want to verify that the login option is available at various stages of the payment flow

  Background:
    Given the checkout page is open
    And the language is set to "it"

  Scenario: Should show login option when entering notice data
    When I enter the notice data
    Then the login button should be visible
    And the login button title should be "Accedi"

  Scenario: Should show login option after entering payment data
    When I enter the notice data
    And I enter the payment data
    Then the login button should be visible
    And the login button title should be "Accedi"

  Scenario: Should show login option after entering email
    When I enter the notice data
    And I enter the payment data
    And I enter the email
    Then the login button should be visible
    And the login button title should be "Accedi"

  Scenario: Should show login option after selecting payment method
    When I enter the notice data
    And I enter the payment data
    And I enter the email
    And I select the payment method
    Then the login button should be visible
    And the login button title should be "Accedi"
