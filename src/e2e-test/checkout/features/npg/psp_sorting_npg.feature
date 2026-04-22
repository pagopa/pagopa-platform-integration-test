Feature: PSP List Sorting in Checkout
  As a checkout user
  I want the PSP (Payment Service Provider) list to be sortable
  So that I can choose the most convenient provider by fee or name

  Background:
    Given the checkout page is open
    And the language is set to "it"
    And a random notice code with prefix "30202" is generated
    And the taxpayer fiscal code is "<VALID_FISCAL_CODE>"

  # ──────────────────────────────────────────────
  # Summary Page sorting
  # ──────────────────────────────────────────────

  Scenario: Should show PSP list sorted by fee ascending on the summary page
    When I enter the notice data with the generated notice code and the taxpayer fiscal code
    And I click the verify button
    And I click the pay button on the summary page
    And I enter and confirm the email
    And I select the payment method "PPAL"
    And I select the PSP with radio id "BCITITMM"
    And I click the PSP list continue button
    And I click the PSP edit button on the summary page
    Then the PSP fee list should be sorted in ascending order
    When I click the "sort by fee" button
    Then the PSP fee list should be sorted in descending order
    And I cancel the payment

  Scenario: Should show PSP list sorted by name on the summary page
    When I enter the notice data with the generated notice code and the taxpayer fiscal code
    And I click the verify button
    And I click the pay button on the summary page
    And I enter and confirm the email
    And I select the payment method "PPAL"
    And I select the PSP with radio id "BCITITMM"
    And I click the PSP list continue button
    And I click the PSP edit button on the summary page
    And I click the "sort by name" button
    Then the PSP name list should be sorted in descending alphabetical order
    When I click the "sort by name" button again
    Then the PSP name list should be sorted in ascending alphabetical order
    And I cancel the payment

  # ──────────────────────────────────────────────
  # PSP Selection Page sorting
  # ──────────────────────────────────────────────

  Scenario: Should show PSP list sorted by name on the PSP selection page
    When I enter the notice data with the generated notice code and the taxpayer fiscal code
    And I click the verify button
    And I click the pay button on the summary page
    And I enter and confirm the email
    And I select the payment method "PPAL"
    And the PSP selection page is loaded
    And I click the sort PSP list button
    And I select the "order by name" radio option
    And I click the show results button
    Then the PSP name list should be sorted in ascending alphabetical order

  Scenario: Should show PSP list sorted by fee on the PSP selection page
    When I enter the notice data with the generated notice code and the taxpayer fiscal code
    And I click the verify button
    And I click the pay button on the summary page
    And I enter and confirm the email
    And I select the payment method "PPAL"
    And the PSP selection page is loaded
    And I click the sort PSP list button
    And I select the "order by amount" radio option
    And I click the show results button
    Then the PSP fee list should be sorted in ascending order
