#3076030512
# language: it
@Fdr3_002
Funzionalità: Aggiunta di Pagamenti ad un Fdr esistente

Contesto:
    Dati i sistemi sono operativi

# ===============================================================================================
# ===============================================================================================


    @runnable
    @happy_path
    @Fdr3_002_01
    Schema dello scenario: Aggiunta con successo di una lista di pagamenti a un flusso di rendicontazione
        Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
        E che esiste un flusso di rendicontazione creato dal PSP con identificativo "2025-06-30ABI50004-1178"
        E il PSP ha una lista di <n> pagamenti da aggiungere al flusso la cui somma degli importi è <amount>
        Quando il PSP invia una richiesta di aggiunta pagamenti al flusso "2025-06-30ABI50004-1178" tramite la api "Add one or more payments to an existing flow" con un body valido
        Allora il sistema risponde con il codice di stato HTTP 200
        E la lista di pagamenti viene aggiunta al flusso di rendicontazione "2025-06-30ABI50004-1178"
        E il numero totale di pagamenti associati al flusso viene aggiornato con <n>
        E l'importo totale del flusso viene aggiornato con <amount>
        E il campo "last_update_date" è aggiornato all'ora corrente
        E lo stato del flusso diventa "INSERTED"
        E il blob object corrispondente viene aggiornato correttamente a sistema

        Esempi:
        | n    | amount |
        | 1    | 3      |
        | 1000 | 29999  | 


# ===============================================================================================
# ===============================================================================================

    @runnable 
    @negative_path
    @Fdr3_002_02
    Scenario: Tentativo di aggiunta di una lista di pagamenti che supera il limite massimo consentito
        Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
        E che esiste un flusso di rendicontazione creato dal PSP con identificativo "2025-06-30ABI50004-1178"
        E il PSP ha una lista di 1001 pagamenti da aggiungere al flusso la cui somma degli importi è 300
        E tale numero di pagamenti supera il limite massimo consentito per un singolo invio
        Quando il PSP invia una richiesta di aggiunta pagamenti al flusso "2025-06-30ABI50004-1178" tramite l'api "Add one or more payments to an existing flow" con un body valido
        Allora il sistema risponde con un errore di validazione e restituisce il codice di stato HTTP 400
        E la lista di pagamenti non viene aggiunta al flusso di rendicontazione


# ===============================================================================================
# ===============================================================================================

    @runnable 
    @negative_path
    @FEAT_002_03
    Scenario: Tentativo di aggiunta pagamenti con somma degli importi non corretta
        Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
        E che esiste un flusso di rendicontazione creato dal PSP con identificativo "2025-06-30ABI50004-1178"
        E il PSP ha una lista di 10 pagamenti da aggiungere al flusso
        Ma la somma degli importi 100 indicata nella richiesta non è corretta rispetto al totale dei singoli pagamenti
        Quando il PSP invia una richiesta di aggiunta pagamenti al flusso "2025-06-30ABI50004-1178" tramite l'api "Add one or more payments to an existing flow" con un body formalmente valido
        Allora il sistema risponde con un errore di validazione e restituisce il codice di stato HTTP 400
        E la lista di pagamenti non viene aggiunta al flusso di rendicontazione


# ===============================================================================================
# ===============================================================================================

    @runnable 
    @negative_path
    @Fdr3_002_04
    Scenario: Tentativo di aggiunta pagamenti a un flusso di rendicontazione non esistente a database
        Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
        E che non esiste alcun flusso di rendicontazione creato dal PSP con identificativo "2025-06-30ABI50004-1176"
        E il PSP ha una lista di 10 pagamenti da aggiungere con somma degli importi pari a 100
        Quando il PSP invia una richiesta di aggiunta pagamenti al flusso "2025-06-30ABI50004-1176" tramite l'api "Add one or more payments to an existing flow" con un body formalmente valido
        Allora il sistema risponde con un errore di risorsa non trovata e restituisce il codice di stato HTTP 404

# ===============================================================================================
# ===============================================================================================

  @runnable 
  @negative_path
  @Fdr3_002_05
  Scenario: Tentativo di aggiunta pagamenti a un flusso di rendicontazione già in stato PUBLISHED
     Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
    E che esiste un flusso di rendicontazione creato dal PSP con identificativo "2025-06-30ABI50004-1178"
    E il flusso si trova in stato "PUBLISHED"
    E il PSP ha una lista di 10 pagamenti da aggiungere con somma degli importi pari a 100
    Quando il PSP invia una richiesta di aggiunta pagamenti al flusso "flow_name" tramite l'api "Add one or more payments to an existing flow" con un body formalmente valido
    Allora il sistema risponde con il codice di stato HTTP 404
    E il flusso di rendicontazione in stato "PUBLISHED" non viene modificato a sistema

# ===============================================================================================
# ===============================================================================================


