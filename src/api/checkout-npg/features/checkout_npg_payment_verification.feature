# language: it
@FEAT_012_Checkout
Funzionalità: Checkout eCommerce - gateway di pagamento NPG
  Valida i flussi API di checkout eCommerce per la verifica del pagamento.

  Contesto:
    Dato l'host di checkout configurato tramite variabile d'ambiente
    E le variabili d'ambiente NPG di checkout configurate

  # ---------------------------------------------------------------------------
  # Verifica pagamento
  # ---------------------------------------------------------------------------

  @checkout @npg @payment-verify @positive
  @FEAT_012_Checkout_SCENARIO_01
  Scenario: La verifica pagamento riuscita restituisce dati di pagamento
    Dato viene generato un codice avviso valido casuale
    Quando l'utente verifica il pagamento per il codice avviso valido
    Allora la risposta ha codice di stato 200
    E la risposta di verifica pagamento contiene dati di pagamento validi

  @checkout @npg @payment-verify @negative
  @FEAT_012_Checkout_SCENARIO_02
  Scenario: La verifica pagamento restituisce 404 per dominio PA sconosciuto
    Quando l'utente verifica il pagamento per il codice avviso con dominio sconosciuto
    Allora la risposta ha codice di stato 404
    E il dettaglio fault code contiene "PPT_DOMINIO_SCONOSCIUTO"

  @checkout @npg @payment-verify @negative
  @FEAT_012_Checkout_SCENARIO_03
  Scenario: La verifica pagamento restituisce 404 per stazione sconosciuta
    Quando l'utente verifica il pagamento per il codice avviso con stazione sconosciuta
    Allora la risposta ha codice di stato 404
    E il dettaglio fault code e uguale a "PPT_STAZIONE_INT_PA_SCONOSCIUTA"
