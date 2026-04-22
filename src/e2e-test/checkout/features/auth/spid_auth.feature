# Created by mpiccolo at 16/04/2026
Feature: Login with SPID flow

  Background:
    Given the checkout page is open
    And the language is set to "it"

  Scenario: Should perform login and logout operation successfully
    When I click on the login button
    Then AccountCircleRoundedIcon should be visible
    When I click on user button
    And I click on exit submenu
    And I confirm the logout action
    Then the login button should be visible after logout