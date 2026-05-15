# Created by mpiccolo at 16/04/2026
@FEAT_002_Checkout @e2e @checkout @ui
Feature: Login with SPID flow

  Background:
    Given The checkout page is open
    And The language is set to "it"

  @checkout @positive
  @FEAT_002_Checkout_scenario_01
  Scenario: Successful SPID login
    When The user clicks on the login button
    Then The user is logged in

  @checkout @positive
  @FEAT_002_Checkout_scenario_02
  Scenario: Succesful SPID logout
    Given The user is logged in with SPID
    When The user clicks on user button
    And The user clicks on exit submenu
    And The user confirm the logout action
    Then The user is succesfully logged out