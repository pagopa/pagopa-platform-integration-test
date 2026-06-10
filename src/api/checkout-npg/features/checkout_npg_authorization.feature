# language: it
@FEAT_009_Checkout
Funzionalità: Checkout eCommerce - gateway di pagamento NPG
  Valida i flussi API di checkout eCommerce per le richieste di autorizzazione via NPG.

  Contesto:
    Dato l'host di checkout configurato tramite variabile d'ambiente
    E le variabili d'ambiente NPG di checkout configurate

  # ---------------------------------------------------------------------------
  # Richieste di autorizzazione
  # ---------------------------------------------------------------------------

  @checkout @npg @authorization @negative
  @FEAT_009_Checkout_SCENARIO_01
  Schema dello scenario: La richiesta di autorizzazione restituisce 401 quando il token JWT e assente
    Dato l'id del metodo di pagamento carta di credito e risolto
    E viene creata una sessione NPG con lingua "<lang>"
    E viene generato un codice avviso valido casuale
    E viene creata una transazione per la sessione corrente
    Quando l'utente richiede l'autorizzazione senza token JWT usando la lingua "<lang>"
    Allora la risposta ha codice di stato 401

    Esempi:
      | lang |
      | it   |
      | fr   |
      | de   |
      | sl   |
      | en   |

  @checkout @npg @authorization @positive
  @FEAT_009_Checkout_SCENARIO_02
  Scenario: La richiesta di autorizzazione con token JWT restituisce URL di autorizzazione
    Dato l'id del metodo di pagamento carta di credito e risolto
    E viene creata una sessione NPG con lingua "it"
    E viene generato un codice avviso valido casuale
    E viene creata una transazione per la sessione corrente
    E i campi carta NPG sono compilati con dati carta di test
    Quando l'utente richiede l'autorizzazione con token JWT usando la lingua "it"
    Allora la risposta ha codice di stato 200
    E la risposta di autorizzazione contiene un URL di autorizzazione valido
    E l'id della richiesta di autorizzazione corrisponde all'order id
