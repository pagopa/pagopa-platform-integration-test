# QUESTO SCENARIO NON E' APPLICABILE
####
# Feature: PSP Unavailable Error Handling in Checkout
# As a checkout user
#  I want to receive a clear error message when no PSP is available for the selected payment method
#  So that I can choose a different payment method and complete the payment
#
#  Background:
#    Given The checkout page is open
#    And The language is set to "it"
#
#  Scenario: Should fail to calculate fee with 404 and show a dedicated error message
#    # Notice code with prefix "30226" triggers a PSP not found (404) error
#    # according to Mock EC: amount changes from 3000€ (verification) to 3010€ (actualization)
#    Given The user eneters a notice code with prefix "30226"
#    When The user enters only the notice data with the generated notice code
#    And The user enters the taxpayer fiscal code from env "VALID_FISCAL_CODE"
#    And The user clicks the verify button
#    And The user clicks the pay button on the summary page
#    And The user enters and confirm the email
#    And The user selects the payment method "BPAY"
#    Then A PSP not found error page is displayed
#    And The error title should contain "Il metodo di pagamento selezionato non è disponibile"
#    And The CTA button should contain "Scegli un altro metodo"
#    And The error description should contain "Può succedere quando l'importo da pagare è particolarmente elevato, o se stai cercando di pagare una marca da bollo digitale."
#    When The user clicks the PSP not found CTA button
#    Then The current URL should contain "/scegli-metodo"
