Feature: PSP Unavailable Error Handling in Checkout
  As a checkout user
  I want to receive a clear error message when no PSP is available for the selected payment method
  So that I can choose a different payment method and complete the payment

  Background:
    Given the checkout page is open
    And the language is set to "it"

  Scenario: Should fail to calculate fee with 404 and show a dedicated error message
    # Notice code with prefix "30226" triggers a PSP not found (404) error
    # according to Mock EC: amount changes from 3000€ (verification) to 3010€ (actualization)
    Given a random notice code with prefix "30226" is generated
    When I enter only the notice data with the generated notice code
    And I enter the taxpayer fiscal code from env "VALID_FISCAL_CODE"
    And I click the verify button
    And I click the pay button on the summary page
    And I enter and confirm the email
    And I select the payment method "BPAY"
    Then a PSP not found error page should be displayed
    And the error title should contain "Il metodo di pagamento selezionato non è disponibile"
    And the CTA button should contain "Scegli un altro metodo"
    And the error description should contain "Può succedere quando l'importo da pagare è particolarmente elevato, o se stai cercando di pagare una marca da bollo digitale."
    When I click the PSP not found CTA button
    Then the current URL should contain "/scegli-metodo"
