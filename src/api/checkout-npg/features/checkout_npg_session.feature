# language: it
@FEAT_013_Checkout
Funzionalità: Checkout eCommerce - gateway di pagamento NPG
  Valida i flussi API di checkout eCommerce per la creazione della sessione carta NPG per lingua.

  Contesto:
    Dato l'host di checkout configurato tramite variabile d'ambiente
    E le variabili d'ambiente NPG di checkout configurate

  # ---------------------------------------------------------------------------
  # Creazione sessione NPG (per lingua)
  # ---------------------------------------------------------------------------

  @checkout @npg @session @positive
  @FEAT_013_Checkout_SCENARIO_01
  Schema dello scenario: La sessione carta NPG viene creata con successo per ogni lingua
    Dato l'id del metodo di pagamento carta di credito e risolto
    Quando l'utente crea una sessione carta NPG con lingua "<lang>"
    Allora la risposta ha codice di stato 200
    E la risposta della sessione NPG contiene campi form carta validi con metodo di pagamento CARDS

    Esempi:
      | lang |
      | it   |
      | fr   |
      | de   |
      | sl   |
      | en   |
