@FEAT_003_checkout @e2e @checkout @ui
Feature: Attivazione pagamento Checkout
  Un utente del sistema checkout
  vuole completare un pagamento con carta di credito/debito
  cosi da poter pagare un avviso tramite la piattaforma pagoPA

  Background:
    Given La pagina di checkout e aperta
    And La lingua e impostata su "it"

  # ──────────────────────────────────────────────
  # Happy path: flusso di pagamento completo
  # ──────────────────────────────────────────────

  @positive
  @FEAT_003_checkout_scenario_01
  Scenario Outline: Un pagamento con configurazione carta "<testing_psp>" viene completato con successo
    When L'utente inserisce i dati dell'avviso con un codice avviso con prefisso "<notice_code_prefix>"
    And L'utente inserisce il codice fiscale del pagatore "<fiscal_code>"
    And L'utente clicca il pulsante verifica
    And L'utente clicca il pulsante paga
    And L'utente inserisce l'email "<email>"
    And L'utente conferma l'email "<email>"
    And L'utente seleziona il metodo di pagamento "CP"
    And L'utente inserisce il numero carta "<pan>"
    And L'utente inserisce la data di scadenza "<expiration_date>"
    And L'utente inserisce il codice di sicurezza "<cvv>"
    And L'utente inserisce il nome dell'intestatario carta "Test test"
    And L'utente seleziona il PSP con id "<pspId>"
    And L'utente conferma la selezione del PSP
    And L'utente clicca il pulsante paga finale
    Then Viene mostrato un messaggio di pagamento completato con successo

    Examples:
      | testing_psp | notice_code_prefix | fiscal_code | email                              | pan              | expiration_date | cvv | pspId       |
      | Postepay    | 30200              | 77777777777 | ecommerce-test-mailgroup@pagopa.it | 5255000260000014 | 12/30           | 123 | PPAYITR1XXX |
      | Wordline    | 30201              | 77777777777 | ecommerce-test-mailgroup@pagopa.it | 5255000260000014 | 12/30           | 123 | BNLIITRR    |
      | Worldpay    | 30201              | 77777777777 | ecommerce-test-mailgroup@pagopa.it | 4242424242424242 | 12/30           | 123 | WOLLNLB1    |

  # ──────────────────────────────────────────────
  # Casi di errore: errori di verifica/attivazione pagamento
  # ──────────────────────────────────────────────

  @negative
  @FEAT_003_checkout_scenario_02
  Scenario Outline: Viene mostrato l'errore <error_code> per codice avviso non valido nell'intervallo <range_start>-<range_end>
    When L'utente inserisce i dati dell'avviso con un codice avviso nell'intervallo "<range_start>" a "<range_end>"
    And L'utente inserisce il codice fiscale del pagatore "<fiscal_code>"
    And L'utente clicca il pulsante verifica
    Then Viene mostrata una modale di errore dopo "<seconds>" secondi
    And L'intestazione della modale di errore contiene "<expected_header>"
    And Il corpo della modale di errore contiene "<expected_body>"

    Examples:
      | error_code                  | range_start        | range_end          | fiscal_code | seconds | expected_header                                  | expected_body                                                                                  |
      | PAA_PAGAMENTO_SCONOSCIUTO   | 302400000000000000 | 302409999999999999 | 77777777777 | 5       | Non riusciamo a trovare l’avviso                 | L'avviso potrebbe essere stato già pagato. Per ricevere assistenza, contatta l’Ente Creditore. |
      | PAA_PAGAMENTO_SCADUTO       | 302990000000000000 | 302999999999999999 | 77777777777 | 60      | L’avviso è scaduto e non è più possibile pagarlo | Contatta l’Ente per maggiori informazioni.                                                     |
      | PPT_STAZIONE_INT_PA_TIMEOUT | 302980000000000000 | 302989999999999999 | 77777777777 | 60      | Si è verificato un errore imprevisto             | Riprova, oppure contatta l’assistenza                                                          |
      | PAA_PAGAMENTO_DUPLICATO     | 302950100443009424 | 302950100443009424 | 77777777777 | 5       | Questo avviso è stato già pagato!                |                                                                                                |

  @negative
  @FEAT_003_checkout_scenario_03
  Scenario Outline: Viene mostrato il codice di errore per ente creditore non raggiungibile
    When L'utente inserisce i dati dell'avviso con un codice avviso nell'intervallo "<range_start>" a "<range_end>"
    And L'utente inserisce il codice fiscale del pagatore "<fiscal_code>"
    And L'utente clicca il pulsante verifica
    Then Viene mostrata una modale di errore
    And L'intestazione della modale di errore contiene "<expected_header>"
    And Il corpo della modale di errore contiene "<expected_body>"
    And Il codice di errore mostrato contiene "<error_code>"

    Examples:
      | error_code                          | range_start        | range_end          | fiscal_code | expected_header                                     | expected_body                     |
      | PPT_STAZIONE_INT_PA_IRRAGGIUNGIBILE | 302970000000000000 | 302979999999999999 | 77777777777 | L’Ente Creditore sta avendo problemi nella risposta | Codice di errore per l'assistenza |
