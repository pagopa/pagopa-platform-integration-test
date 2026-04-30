# Created by mpiccolo at 16/04/2026
Feature: Login with SPID flow

  Background:
    Given The checkout page is open
    And The language is set to "it"

  Scenario: Successful SPID login
    When The user clicks on the login button
    Then AccountCircleRoundedIcon is visible

  Scenario: Succesful SPID logout
    Given The user is logged in with SPID
    When The user clicks on user button
    And The user clicks on exit submenu
    And The user confirm the logout action
    Then The login button is visible after logout