Feature: Checkout Payment Activation
  As a user of the checkout system
  I want to complete a payment using a credit/debit card
  So that I can pay a notice through the pagoPA platform

  Background:
    Given the checkout page is open
    And the language is set to "it"

  # ──────────────────────────────────────────────
  # Happy path: full payment flow
  # ──────────────────────────────────────────────

  Scenario Outline: Should correctly execute a payment with card configuration "<testingPsp>"
    When I enter the notice data with a random notice code for fiscal code prefix "<fiscalCodePrefix>"
    And I enter the taxpayer fiscal code "<fiscalCode>"
    And I click the verify button
    And I click the pay button
    And I enter the email "<email>"
    And I confirm the email "<email>"
    And I select the payment method "CP"
    And I fill in the card number "<pan>"
    And I fill in the expiration date "<expirationDate>"
    And I fill in the security code "<cvv>"
    And I fill in the cardholder name "Test test"
    And I select the PSP with id "<pspId>"
    And I confirm the PSP selection
    And I click the final pay button
    Then the result page should show "Hai pagato"

    Examples:
      | testingPsp | fiscalCodePrefix | fiscalCode  | email                              | pan              | expirationDate | cvv | pspId       |
      | Postepay   | 30200            | 77777777777 | ecommerce-test-mailgroup@pagopa.it | 5255000260000014 | 12/30          | 123 | PPAYITR1XXX |
      | Wordline   | 30201            | 77777777777 | ecommerce-test-mailgroup@pagopa.it | 5255000260000014 | 12/30          | 123 | BNLIITRR    |
      | Worldpay   | 30201            | 77777777777 | ecommerce-test-mailgroup@pagopa.it | 4242424242424242 | 12/30          | 123 | WOLLNLB1    |

  # ──────────────────────────────────────────────
  # Error cases: verify/activate payment errors
  # ──────────────────────────────────────────────

  Scenario Outline: Should throw error <errorCode> for invalid notice code in range <rangeStart>-<rangeEnd>
    When I enter the notice data with a notice code in range "<rangeStart>" to "<rangeEnd>"
    And I enter the taxpayer fiscal code "<fiscalCode>"
    And I click the verify button
    Then an error modal should be displayed after "<seconds>" seconds
    And the error modal header should contain "<expectedHeader>"
    And the error modal body should contain "<expectedBody>"

    Examples:
      | errorCode                      | rangeStart           | rangeEnd             | fiscalCode  | seconds | expectedHeader                                         | expectedBody                                                                              |
      | PAA_PAGAMENTO_SCONOSCIUTO      | 302400000000000000   | 302409999999999999   | 77777777777 |  5      | Non riusciamo a trovare l’avviso                       | L'avviso potrebbe essere stato già pagato. Per ricevere assistenza, contatta l’Ente Creditore. |
      | PAA_PAGAMENTO_SCADUTO          | 302990000000000000   | 302999999999999999   | 77777777777 | 60      | L’avviso è scaduto e non è più possibile pagarlo       | Contatta l’Ente per maggiori informazioni.                                                |
      | PPT_STAZIONE_INT_PA_TIMEOUT    | 302980000000000000   | 302989999999999999   | 77777777777 | 60      | Si è verificato un errore imprevisto                   | Riprova, oppure contatta l’assistenza                                                     |
      | PAA_PAGAMENTO_DUPLICATO        | 302950100443009424   | 302950100443009424   | 77777777777 |  5      | Questo avviso è stato già pagato!                      |                                                                                           |

  Scenario Outline: Should show error code for unreachable creditor institution
    When I enter the notice data with a notice code in range "<rangeStart>" to "<rangeEnd>"
    And I enter the taxpayer fiscal code "<fiscalCode>"
    And I click the verify button
    Then an error modal should be displayed
    And the error modal header should contain "<expectedHeader>"
    And the error modal body should contain "<expectedBody>"
    And the error code shown should contain "<errorCode>"

    Examples:
      | errorCode                          | rangeStart         | rangeEnd           | fiscalCode  | expectedHeader                                      | expectedBody                          |
      | PPT_STAZIONE_INT_PA_IRRAGGIUNGIBILE | 302970000000000000 | 302979999999999999 | 77777777777 | L’Ente Creditore sta avendo problemi nella risposta | Codice di errore per l'assistenza     |
