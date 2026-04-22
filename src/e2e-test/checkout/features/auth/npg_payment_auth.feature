# Created by mpiccolo at 15/04/2026
Feature: # Enter feature name here
  # Enter feature description here

  Background:
    Given the checkout page is open
    And the language is set to "it"
    And the user is logged in

  Scenario: Should correctly execute a payment
    When I insert the payment notice details
    Then I should receive a successful payment message

