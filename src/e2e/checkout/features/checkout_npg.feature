# language: it

@FEAT_003_Checkout
@e2e
@checkout
@ui
Funzionalità: Attivazione pagamento Checkout
  Un utente del sistema checkout
  vuole completare un pagamento con carta di credito/debito
  così da poter pagare un avviso tramite la piattaforma pagoPA

  Contesto:
    Dato La pagina di checkout è aperta
    E La lingua è impostata su "it"

  # =============================================
  # Happy path: flusso di pagamento completo
  # =============================================

  @smoke
  @positive
  @FEAT_003_Checkout_scenario_01
  Schema dello scenario: Un pagamento con configurazione carta "<testing_psp>" viene completato con successo
    Quando L'utente inserisce i dati dell'avviso con un codice avviso con prefisso "<notice_code_prefix>"
    E L'utente inserisce il codice fiscale del pagatore "<fiscal_code>"
    E L'utente clicca il pulsante verifica
    E L'utente clicca il pulsante paga
    E L'utente inserisce l'email "<email>"
    E L'utente conferma l'email "<email>"
    E L'utente seleziona il metodo di pagamento "CP"
    E L'utente inserisce il numero carta "<pan>"
    E L'utente inserisce la data di scadenza "<expiration_date>"
    E L'utente inserisce il codice di sicurezza "<cvv>"
    E L'utente inserisce il nome dell'intestatario carta "Test test"
    E L'utente seleziona il PSP con id "<pspId>"
    E L'utente conferma la selezione del PSP
    E L'utente clicca il pulsante paga finale
    Allora Viene mostrato un messaggio di pagamento completato con successo

    Esempi:
      | testing_psp | notice_code_prefix | fiscal_code | email                              | pan              | expiration_date | cvv | pspId       |
      | Postepay    | 30200              | 77777777777 | ecommerce-test-mailgroup@pagopa.it | 5255000260000014 | 12/30           | 123 | PPAYITR1XXX |
      | Wordline    | 30201              | 77777777777 | ecommerce-test-mailgroup@pagopa.it | 5255000260000014 | 12/30           | 123 | BNLIITRR    |
      | Worldpay    | 30201              | 77777777777 | ecommerce-test-mailgroup@pagopa.it | 4242424242424242 | 12/30           | 123 | WOLLNLB1    |

  # =============================================
  # Casi di errore: errori di verifica/attivazione pagamento
  # =============================================

  @negative
  @FEAT_003_Checkout_scenario_02
  Schema dello scenario: Viene mostrato l'errore <error_code> per codice avviso non valido nell'intervallo <range_start>-<range_end>
    Quando L'utente inserisce i dati dell'avviso con un codice avviso nell'intervallo "<range_start>" a "<range_end>"
    E L'utente inserisce il codice fiscale del pagatore "<fiscal_code>"
    E L'utente clicca il pulsante verifica
    Allora Viene mostrata una modale di errore dopo "<seconds>" secondi
    E L'intestazione della modale di errore contiene "<expected_header>"
    E Il corpo della modale di errore contiene "<expected_body>"

    Esempi:
      | error_code                  | range_start        | range_end          | fiscal_code | seconds | expected_header                                  | expected_body                                                                                  |
      | PAA_PAGAMENTO_SCONOSCIUTO   | 302400000000000000 | 302409999999999999 | 77777777777 | 5       | Non riusciamo a trovare l’avviso                 | L'avviso potrebbe essere stato già pagato. Per ricevere assistenza, contatta l’Ente Creditore. |
      | PAA_PAGAMENTO_SCADUTO       | 302990000000000000 | 302999999999999999 | 77777777777 | 60      | L’avviso è scaduto e non è più possibile pagarlo | Contatta l’Ente per maggiori informazioni.                                                     |
      | PPT_STAZIONE_INT_PA_TIMEOUT | 302980000000000000 | 302989999999999999 | 77777777777 | 60      | Si è verificato un errore imprevisto             | Riprova, oppure contatta l’assistenza                                                          |
      | PAA_PAGAMENTO_DUPLICATO     | 302950100443009424 | 302950100443009424 | 77777777777 | 5       | Questo avviso è stato già pagato!                |                                                                                                |

  @negative
  @FEAT_003_Checkout_scenario_03
  Schema dello scenario: Viene mostrato il codice di errore per ente creditore non raggiungibile
    Quando L'utente inserisce i dati dell'avviso con un codice avviso nell'intervallo "<range_start>" a "<range_end>"
    E L'utente inserisce il codice fiscale del pagatore "<fiscal_code>"
    E L'utente clicca il pulsante verifica
    Allora Viene mostrata una modale di errore
    E L'intestazione della modale di errore contiene "<expected_header>"
    E Il corpo della modale di errore contiene "<expected_body>"
    E Il codice di errore mostrato contiene "<error_code>"

    Esempi:
      | error_code                          | range_start        | range_end          | fiscal_code | expected_header                                     | expected_body                     |
      | PPT_STAZIONE_INT_PA_IRRAGGIUNGIBILE | 302970000000000000 | 302979999999999999 | 77777777777 | L’Ente Creditore sta avendo problemi nella risposta | Codice di errore per l'assistenza |
