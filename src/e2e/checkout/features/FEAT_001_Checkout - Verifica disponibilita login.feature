# qa-hub: FEAT_001_Checkout
# language: it
@CHECKOUT_001 @e2e
Funzionalità: Verifica disponibilità login
  L'utente checkout vuole verificare che l'opzione di login sia disponibile nelle varie fasi del flusso di pagamento

  Contesto:
    Dato La pagina di checkout è aperta
    E La lingua è impostata su "it"

  @checkout @e2e @smoke @ui @runnable @positive
  @CHECKOUT_001_01
  Scenario: Opzione login disponibile durante l'inserimento dei dati avviso
    Quando L'utente inserisce i dati dell'avviso
    Allora Il pulsante di login è visibile e abilitato
    E Il titolo del pulsante di login è "Accedi"

  @checkout @e2e @smoke @ui @runnable @positive
  @CHECKOUT_001_02
  Scenario: Opzione login disponibile durante l'inserimento dei dati di pagamento
    Dato L'utente inserisce i dati dell'avviso
    Quando L'utente inserisce i dati di pagamento
    Allora Il pulsante di login è visibile e abilitato
    E Il titolo del pulsante di login è "Accedi"

  @checkout @e2e @smoke @ui @runnable @positive
  @CHECKOUT_001_03
  Scenario: Opzione login disponibile durante l'inserimento dell'email
    Dato L'utente inserisce i dati dell'avviso
    E L'utente inserisce i dati di pagamento
    Quando L'utente inserisce l'email
    Allora Il pulsante di login è visibile e abilitato
    E Il titolo del pulsante di login è "Accedi"

  @checkout @e2e @smoke @ui @runnable @positive
  @CHECKOUT_001_04
  Scenario: Opzione login disponibile durante la selezione del metodo di pagamento
    Dato L'utente inserisce i dati dell'avviso
    E L'utente inserisce i dati di pagamento
    E L'utente inserisce l'email
    Quando L'utente seleziona il metodo di pagamento
    Allora Il pulsante di login è visibile e abilitato
    E Il titolo del pulsante di login è "Accedi"
