Feature: Checkout Payment Activation
  As a user of the checkout system
  The user want to complete a payment using a credit/debit card
  So that The user can pay a notice through the pagoPA platform

  Background:
    Given The checkout page is open
    And The language is set to "it"

  # ──────────────────────────────────────────────
  # Happy path: full payment flow
  # ──────────────────────────────────────────────

  Scenario Outline: A payment with card configuration "<testing_psp>" is successfully completed
    When The user enters the notice data with a notice code with fiscal code prefix "<fiscal_code_prefix>"
    And The user enters the taxpayer fiscal code "<fiscal_code>"
    And The user clicks the verify button
    And The user clicks the pay button
    And The user enters the email "<email>"
    And The user confirms the email "<email>"
    And The user selects the payment method "CP"
    And The user fills in the card number "<pan>"
    And The user fills in the expiration date "<expiration_date>"
    And The user fills in the security code "<cvv>"
    And The user fills in the cardholder name "Test test"
    And The user selects the PSP with id "<pspId>"
    And The user confirms the PSP selection
    And The user clicks the final pay button
    Then A successful payment message is shown

    Examples:
      | testing_psp | fiscal_code_prefix | fiscal_code | email                              | pan              | expiration_date | cvv | pspId       |
      | Postepay    | 30200              | 77777777777 | ecommerce-test-mailgroup@pagopa.it | 5255000260000014 | 12/30           | 123 | PPAYITR1XXX |
      | Wordline    | 30201              | 77777777777 | ecommerce-test-mailgroup@pagopa.it | 5255000260000014 | 12/30           | 123 | BNLIITRR    |
      | Worldpay    | 30201              | 77777777777 | ecommerce-test-mailgroup@pagopa.it | 4242424242424242 | 12/30           | 123 | WOLLNLB1    |

  # ──────────────────────────────────────────────
  # Error cases: verify/activate payment errors
  # ──────────────────────────────────────────────

  Scenario Outline: Error <error_code> for invalid notice code in range <range_start>-<range_end> is shown on verify
    When The user enters the notice data with a notice code in range "<range_start>" to "<range_end>"
    And The user enters the taxpayer fiscal code "<fiscal_code>"
    And The user clicks the verify button
    Then An error modal is displayed after "<seconds>" seconds
    And The error modal header contains "<expected_header>"
    And The error modal body contains "<expected_body>"

    Examples:
      | error_code                  | range_start        | range_end          | fiscal_code | seconds | expected_header                                  | expected_body                                                                                  |
      | PAA_PAGAMENTO_SCONOSCIUTO   | 302400000000000000 | 302409999999999999 | 77777777777 | 5       | Non riusciamo a trovare l’avviso                 | L'avviso potrebbe essere stato già pagato. Per ricevere assistenza, contatta l’Ente Creditore. |
      | PAA_PAGAMENTO_SCADUTO       | 302990000000000000 | 302999999999999999 | 77777777777 | 60      | L’avviso è scaduto e non è più possibile pagarlo | Contatta l’Ente per maggiori informazioni.                                                     |
      | PPT_STAZIONE_INT_PA_TIMEOUT | 302980000000000000 | 302989999999999999 | 77777777777 | 60      | Si è verificato un errore imprevisto             | Riprova, oppure contatta l’assistenza                                                          |
      | PAA_PAGAMENTO_DUPLICATO     | 302950100443009424 | 302950100443009424 | 77777777777 | 5       | Questo avviso è stato già pagato!                |                                                                                                |

  Scenario Outline: Error code for unreachable creditor institution is shown on verify
    When The user enters the notice data with a notice code in range "<range_start>" to "<range_end>"
    And The user enters the taxpayer fiscal code "<fiscal_code>"
    And The user clicks the verify button
    Then An error modal is displayed
    And The error modal header contains "<expected_header>"
    And The error modal body contains "<expected_body>"
    And The error code shown contains "<error_code>"

    Examples:
      | error_code                          | range_start        | range_end          | fiscal_code | expected_header                                     | expected_body                     |
      | PPT_STAZIONE_INT_PA_IRRAGGIUNGIBILE | 302970000000000000 | 302979999999999999 | 77777777777 | L’Ente Creditore sta avendo problemi nella risposta | Codice di errore per l'assistenza |
