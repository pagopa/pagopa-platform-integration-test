# language: it
@FEAT_015_Checkout
Funzionalità: Servizio eCommerce CDC
  Valida il servizio eCommerce CDC (Change Data Capture) guidando l'intero
  flusso di pagamento Checkout

  Contesto:
    Date le variabili d'ambiente eCommerce CDC sono configurate

  # ---------------------------------------------------------------------------
  # Eliminazione transazione - verifica stato CANCELED
  # ---------------------------------------------------------------------------

  @cdc @transaction @cancel @positive
  @FEAT_015_Checkout_SCENARIO_01
  Scenario: La transazione ACTIVATED viene annullata e raggiunge lo stato CANCELED
    Dato viene generato un codice avviso CDC casuale
    Quando l'utente crea una transazione CDC con un order id statico
    E l'utente elimina la transazione CDC
    Allora la risposta CDC ha codice di stato 202
    E lo stato della transazione raggiunge "CANCELED" tramite polling

  # ---------------------------------------------------------------------------
  # Creazione sessione NPG
  # ---------------------------------------------------------------------------

  @cdc @session @positive
  @FEAT_015_Checkout_SCENARIO_02
  Scenario: La sessione carta NPG viene creata con i campi form carta attesi
    Dato l'id del metodo di pagamento carta di credito CDC e risolto
    Quando l'utente crea una sessione carta NPG CDC
    Allora la risposta CDC ha codice di stato 200
    E la sessione NPG contiene quattro campi del form carta
    E la sessione NPG ha il metodo di pagamento CARDS
    E la sessione NPG ha un order id valido

  # ---------------------------------------------------------------------------
  # Creazione transazione - verifica stato ACTIVATED
  # ---------------------------------------------------------------------------

  @cdc @transaction @activated @positive
  Scenario: Una nuova transazione raggiunge lo stato ACTIVATED
    Dato l'id del metodo di pagamento carta di credito CDC e risolto
    E una sessione NPG CDC e preparata
    E viene generato un codice avviso CDC casuale
    Quando l'utente crea una transazione CDC per la sessione corrente
    Allora la risposta CDC ha codice di stato 200
    E la risposta della transazione ha stato ACTIVATED
    E la risposta della transazione ha transactionId e authToken validi
    E i pagamenti della transazione hanno la struttura prevista
    E lo stato della transazione raggiunge "ACTIVATED" tramite polling

  # ---------------------------------------------------------------------------
  # Dettagli metodo di pagamento
  # ---------------------------------------------------------------------------

  @cdc @payment-methods @positive
  Scenario: I dettagli del metodo di pagamento carta di credito sono recuperati correttamente
    Dato l'id del metodo di pagamento carta di credito CDC e risolto
    Quando l'utente recupera i dettagli del metodo di pagamento CDC
    Allora la risposta CDC ha codice di stato 200
    E il metodo di pagamento ha nome "CARDS" e paymentTypeCode "CP"
    E il metodo di pagamento ha asset e ranges non vuoti

  # ---------------------------------------------------------------------------
  # Calcolo commissioni
  # ---------------------------------------------------------------------------

  @cdc @fees @positive
  Scenario: I bundle commissione PSP vengono recuperati per il pagamento con carta di credito
    Dato l'id del metodo di pagamento carta di credito CDC e risolto
    E una sessione NPG CDC e preparata
    E viene generato un codice avviso CDC casuale
    E una transazione CDC e creata per la sessione corrente
    Quando l'utente calcola la commissione CDC per il pagamento con carta di credito
    Allora la risposta CDC ha codice di stato 200
    E la risposta della commissione ha paymentMethodStatus "ENABLED"
    E la risposta della commissione ha belowThreshold false
    E la risposta della commissione ha bundles non vuoti

  # ---------------------------------------------------------------------------
  # Tutti i metodi di pagamento - asset brand
  # ---------------------------------------------------------------------------

  @cdc @payment-methods @positive
  Scenario: Tutti i metodi di pagamento v1 includono gli asset brand attesi
    Quando l'utente recupera tutti i metodi di pagamento CDC v1
    Allora la risposta CDC ha codice di stato 200
    E la lista dei metodi di pagamento non e vuota
    E i metodi carta di credito hanno gli asset brand VISA e Mastercard

  # ---------------------------------------------------------------------------
  # Flusso CDC completo - richiesta autorizzazione -> AUTHORIZATION_REQUESTED
  # ---------------------------------------------------------------------------

  @cdc @authorization @positive @e2e
  Scenario: Il flusso CDC completo termina con transazione in stato AUTHORIZATION_REQUESTED
    Dato l'id del metodo di pagamento carta di credito CDC e risolto
    E una sessione NPG CDC e preparata
    E i cookie NPG sono popolati
    E viene generato un codice avviso CDC casuale
    E una transazione CDC e creata per la sessione corrente
    E lo stato della transazione raggiunge "ACTIVATED" tramite polling
    E i dati carta corrispondono ai valori della carta di test dopo la compilazione dei campi NPG
    Quando l'utente richiede l'autorizzazione CDC per la transazione
    Allora la risposta CDC ha codice di stato 200
    E la risposta di autorizzazione ha un authorizationUrl valido
    E l'authorization requestId corrisponde all'order id corrente
    E lo stato della transazione raggiunge "AUTHORIZATION_REQUESTED" tramite polling
