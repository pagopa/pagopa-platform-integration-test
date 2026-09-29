# language: it
@Fdr3_002_CreaRevisione
Funzionalità: Workflow di creazione e gestione delle revisioni di un flusso di rendicontazione

  Contesto:
    Dato i sistemi sono operativi

  @runnable
  @positive
  Scenario: Creazione del flusso iniziale utilizzato per i test di revisione
    Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
    E un nome di flusso di rendicontazione univoco chiamato flow_name
    E una data del flusso univoca chiamata flow_date
    E un payload di creazione FdR
      """
        { "fdr": "$flow_name$", "fdrDate": "$flow_date$", "totPayments": $number_of_payments$, "sumPayments": $payments_amount$ }
      """
    Quando il PSP invia la richiesta di creazione flusso tramite l'API "Create a new flow structure"
    Allora il PSP riceve il codice di stato HTTP 201

  Scenario: Aggiunta di 3 pagamenti alla revisione iniziale
    Dato che il flusso iniziale è stato creato con successo
    E che il PSP deve inviare 3 pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è 300
    Quando il PSP invia la richiesta di aggiunta pagamenti (API "Add payments") con 3 pagamenti per il flusso "flow_name"
    Allora il PSP riceve il codice di stato HTTP 200

  Scenario: Pubblicazione della prima revisione
    Dato che sono stati aggiunti 3 pagamenti con successo
    Quando il PSP invia la richiesta di pubblicazione (API "Publish")
    Allora il PSP riceve il codice di stato HTTP 200

  Scenario: Verifica revisione dopo prima pubblicazione
    Dato che la pubblicazione della prima revisione è avvenuta con successo
    E la revisione del FdR è 1
    Quando il PSP richiede i dettagli del flusso pubblicato (API "Get published FdR")
    Allora il PSP riceve il codice di stato HTTP 200
    E la risposta contiene revision = 1

  Scenario: Creazione di una nuova versione (revisione 2) dello stesso FdR
    Dato una nuova data del flusso univoca chiamata flow_date
    E un payload di creazione FdR
      """
        { "fdr": "$flow_name$", "fdrDate": "$flow_date$", "totPayments": $number_of_payments$, "sumPayments": $payments_amount$ }
      """
    Quando il PSP invia la richiesta di creazione flusso tramite l'API "Create a new flow structure"
    Allora il PSP riceve il codice di stato HTTP 201

  Scenario: Creazione della revisione 2 confermata
    Dato che la prima revisione è stata pubblicata con successo
    E che il PSP deve inviare 2 pagamenti al flusso
    Quando il PSP richiede i dettagli del flusso creato (API "Get created FdR")
    Allora il PSP riceve il codice di stato HTTP 200
    E la risposta contiene revision = 2
    E lo stato del flusso è "CREATED"

  Scenario: Aggiunta di 2 pagamenti alla revisione 2
    Dato che la revisione 2 è stata creata con successo
    Quando il PSP invia la richiesta di aggiunta pagamenti (API "Add payments") con 2 pagamenti per il flusso "flow_name"
    Allora il PSP riceve il codice di stato HTTP 200

  Scenario: Pubblicazione della revisione 2
    Dato che sono stati aggiunti 2 pagamenti alla revisione 2
    Quando il PSP invia la richiesta di pubblicazione (API "Publish")
    Allora il PSP riceve il codice di stato HTTP 200

  Scenario: Verifica revisione dopo seconda pubblicazione
    Dato che la pubblicazione della revisione 2 è avvenuta con successo
    Quando il PSP richiede i dettagli del flusso pubblicato (API "Get published FdR")
    Allora il PSP riceve il codice di stato HTTP 200
    E la risposta contiene revision = 2
    E la risposta contiene totPayments = 2

  Scenario: Creazione della revisione 3
    Dato una nuova data del flusso univoca chiamata flow_date
    E che la revisione 2 è stata pubblicata con successo
    E che il PSP deve inviare 1 pagamento al flusso
    Quando il PSP richiede i dettagli del flusso creato (API "Get created FdR")
    Allora il PSP riceve il codice di stato HTTP 200
    E la risposta contiene revision = 3
    E lo stato del flusso è "CREATED"

  Scenario: Aggiunta di 2 pagamenti invece di 1 nella revisione 3
    Dato che la revisione 3 è stata creata con successo
    Quando il PSP invia la richiesta di aggiunta pagamenti (API "Add payments") con 2 pagamenti per il flusso "flow_name"
    Allora il PSP riceve il codice di stato HTTP 200

  @runnable
  Scenario: Tentativo di pubblicazione della revisione 3 non valido
    Dato che sono stati aggiunti 2 pagamenti invece di 1 alla revisione 3
    Quando il PSP invia la richiesta di pubblicazione (API "Publish")
    Allora il PSP riceve il codice di stato HTTP 400
