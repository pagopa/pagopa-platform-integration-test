# language: it
@fdr3_010_Verifica_paginazione_PSP
Funzionalità: Verifica paginazione per le API PSP

  Contesto:
    Dato i sistemi sono operativi

  @fdr3_010_01
  Scenario: Creazione del flusso di rendicontazione per test paginazione PSP
    Dato un nome di flusso di rendicontazione univoco chiamato flow_name
    E una data di flusso di rendicontazione univoco chiamato flow_date
    E un payload di creazione FdR create_payload
    Quando il PSP invia la richiesta di "Creazione di una nuova struttura di flusso" con il payload "create_payload"
    Allora il PSP riceve il codice di stato HTTP 201

  @fdr3_010_02
  Scenario: Inserimento pagamenti per test paginazione PSP
    Dato che il PSP deve inviare 100 pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è 20
    E che lo scenario "Creazione del flusso di rendicontazione per test paginazione PSP" è stato eseguito con successo
    Quando il PSP aggiunge 100 pagamenti la cui somme è 20 al flusso di rendicontazione flow_name come payments_payload
    E il PSP invia la richiesta di "Aggiunta pagamenti" con il payload "payments_payload"
    Allora il PSP riceve il codice di stato HTTP 200

  @fdr3_010_03
  Scenario: Pubblicazione del flusso per test paginazione PSP
    Dato che lo scenario "Inserimento pagamenti per test paginazione PSP" è stato eseguito con successo
    Quando il PSP invia la richiesta di "Pubblicazione" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200

  @runnable
  @fdr3_010_04
  Scenario: Verifica paginazione pagamenti creati pagina 1
    Dato che lo scenario "Inserimento pagamenti per test paginazione PSP" è stato eseguito con successo
    E il PSP aggiunge $flow_date$ come createdGt nei parametri di query
    E il PSP aggiunge 1 come page nei parametri di query
    E il PSP aggiunge 99 come size nei parametri di query
    Quando il PSP invia la richiesta di "recupero pagamenti creati" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200
    E il PSP riceve pagina 1 con 99 elementi come risposta

  @runnable
  @fdr3_010_05
  Scenario: Verifica paginazione pagamenti creati pagina 2
    Dato che lo scenario "Inserimento pagamenti per test paginazione PSP" è stato eseguito con successo
    E il PSP aggiunge $flow_date$ come createdGt nei parametri di query
    E il PSP aggiunge 2 come page nei parametri di query
    E il PSP aggiunge 1 come size nei parametri di query
    Quando il PSP invia la richiesta di "Recupero pagamenti creati" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200
    E il PSP riceve pagina 2 con 1 elementi come risposta

  @runnable
  @fdr3_010_06
  Scenario: Verifica paginazione FdR creati pagina 1
    Dato che lo scenario "Inserimento pagamenti per test paginazione PSP" è stato eseguito con successo
    E il PSP aggiunge ieri come createdGt nei parametri di query
    E il PSP aggiunge 1 come page nei parametri di query
    E il PSP aggiunge 1 come size nei parametri di query
    Quando il PSP invia la richiesta di "Recupero di tutti i FdR creati dal PSP" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200
    E il PSP riceve pagina 1 con 1 elementi come risposta

  @runnable
  @fdr3_010_07
  Scenario: Verifica paginazione FdR creati pagina 2
    Dato che lo scenario "Inserimento pagamenti per test paginazione PSP" è stato eseguito con successo
    E il PSP aggiunge ieri come createdGt nei parametri di query
    E il PSP aggiunge 2 come page nei parametri di query
    E il PSP aggiunge 1 come size nei parametri di query
    Quando il PSP invia la richiesta di "Recupero di tutti i FdR creati dal PSP" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200
    E il PSP riceve pagina 2 con 1 elementi come risposta

  @runnable
  @fdr3_010_08
  Schema dello scenario: Verifica paginazione pagamenti pubblicati dal PSP
    Dato che lo scenario "Pubblicazione del flusso per test paginazione PSP" è stato eseguito con successo
    E la revisione del FdR è 1
    E il PSP aggiunge ieri come createdGt nei parametri di query
    E il PSP aggiunge <page_number> come page nei parametri di query
    E il PSP aggiunge <page_size> come size nei parametri di query
    Quando il PSP invia la richiesta di "Recupero pagamenti pubblicati dal PSP" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200
    E il PSP riceve pagina <page_number> con <page_size> elementi come risposta

    Esempi:
      | page_number | page_size |
      | 1           | 1         |
      | 2           | 50        |

  @runnable
  @fdr3_010_09
  Schema dello scenario: Verifica paginazione FdR pubblicati dal PSP
    Dato che lo scenario "Pubblicazione del flusso per test paginazione PSP" è stato eseguito con successo
    E la revisione del FdR è 1
    E la configurazione psp è valorizzata come pspId nei parametri di query
    E la configurazione organization è valorizzata come organizationId nei parametri di query
    E il PSP aggiunge ieri come publishedGt nei parametri di query
    E il PSP aggiunge <page_number> come page nei parametri di query
    E il PSP aggiunge <page_size> come size nei parametri di query
    Quando il PSP invia la richiesta di "Recupero di tutti i FdR pubblicati dal PSP" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200
    E il PSP riceve pagina <page_number> con <page_size> elementi come risposta

    Esempi:
      | page_number | page_size |
      | 1           | 1         |
      | 2           | 2         |
