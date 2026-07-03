# language: it

@FEAT_004_Checkout
@e2e
@checkout
@ui
Funzionalità: Attivazione pagamento Checkout autenticato
  Un utente del sistema checkout
  vuole completare un pagamento con carta di credito/debito
  così da poter pagare un avviso tramite la piattaforma pagoPA

  Contesto:
    Dato La pagina di checkout è aperta
    E La lingua è impostata su "it"
    E L'utente è autenticato

  # =============================================
  # Happy path: flusso di pagamento completo
  # =============================================

  @smoke
  @positive
  @FEAT_004_Checkout_scenario_01
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