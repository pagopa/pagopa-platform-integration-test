# Created by mpiccolo at 15/04/2026
Feature: Payment completed successfully after login with

  Background:
    Given The checkout page is open
    And The language is set to "it"
    And The user is logged in

  Scenario: The payment is completed successfully
    When The user insert the payment notice details
    Then A successful payment message is shown

