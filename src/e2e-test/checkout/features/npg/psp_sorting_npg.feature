Feature: PSP List Sorting in Checkout
  As a checkout user
  I want the PSP (Payment Service Provider) list to be sortable
  So that I can choose the most convenient provider by fee or name

  Background:
    Given The checkout page is open
    And The language is set to "it"
    And The user enters a valid notice code with prefix "30202"
    And The user enters a valid taxpayer fiscal code

  # ──────────────────────────────────────────────
  # Summary Page sorting
  # ──────────────────────────────────────────────

  Scenario: The PSP list is sorted by fee in ascending order on the summary page
    When The user enters the notice information
    And The user clicks the verify button
    And The user clicks the pay button on the summary page
    And The user enters and confirm the email
    And The user selects the payment method "PPAL"
    And The user selects the PSP with radio id "BCITITMM"
    And The user clicks the PSP list continue button
    And The user clicks the PSP edit button on the summary page
    Then The PSP fee list is sorted in ascending order
    And The user cancels the payment
    
  Scenario: The PSP list is sorted by fee in descending order on the summary page
    When The user enters the notice information
    And The user clicks the verify button
    And The user clicks the pay button on the summary page
    And The user enters and confirm the email
    And The user selects the payment method "PPAL"
    And The user selects the PSP with radio id "BCITITMM"
    And The user clicks the PSP list continue button
    And The user clicks the PSP edit button on the summary page
    And The user clicks the "sort by fee" button
    Then The PSP fee list is sorted in descending order
    And The user cancels the payment

  Scenario: The PSP list is sorted by name in descending order on the summary page
    When The user enters the notice information
    And The user clicks the verify button
    And The user clicks the pay button on the summary page
    And The user enters and confirm the email
    And The user selects the payment method "PPAL"
    And The user selects the PSP with radio id "BCITITMM"
    And The user clicks the PSP list continue button
    And The user clicks the PSP edit button on the summary page
    And The user clicks the "sort by name" button
    Then The PSP name list is sorted in descending alphabetical order
    And The user cancels the payment

  Scenario: The PSP list is sorted by name in ascending order on the summary page
    When The user enters the notice information
    And The user clicks the verify button
    And The user clicks the pay button on the summary page
    And The user enters and confirm the email
    And The user selects the payment method "PPAL"
    And The user selects the PSP with radio id "BCITITMM"
    And The user clicks the PSP list continue button
    And The user clicks the PSP edit button on the summary page
    Then The PSP name list is sorted in ascending alphabetical order
    And The user cancels the payment
  # ──────────────────────────────────────────────
  # PSP Selection Page sorting
  # ──────────────────────────────────────────────

  Scenario: The PSP list is sorted by name on the PSP selection page
    When The user enters the notice information
    And The user clicks the verify button
    And The user clicks the pay button on the summary page
    And The user enters and confirm the email
    And The user selects the payment method "PPAL"
    And The PSP selection page is loaded
    And The user clicks the sort PSP list button
    And The user selects the "order by name" radio option
    And The user clicks the show results button
    Then The PSP name list is sorted in ascending alphabetical order

  Scenario: The PSP list is sorted by fee on the PSP selection page
    When The user enters the notice information
    And The user clicks the verify button
    And The user clicks the pay button on the summary page
    And The user enters and confirm the email
    And The user selects the payment method "PPAL"
    And The PSP selection page is loaded
    And The user clicks the sort PSP list button
    And The user selects the "order by amount" radio option
    And The user clicks the show results button
    Then The PSP fee list is sorted in ascending order
