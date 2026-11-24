#language: it
@fdr3_001_Aggiungi_pagamenti
Funzionalità: Aggiunta di pagamenti a un flusso di rendicontazione

  Contesto:
    Dato che i sistemi sono operativi

  @fdr3_001_01
  Scenario: Creazione del flusso di rendicontazione per il test di aggiunta pagamenti
    Dato un nome di flusso di rendicontazione univoco chiamato flow_name
    E una data di flusso di rendicontazione univoco chiamato flow_date
    E un payload di creazione FdR create_payload
    Quando il PSP invia la richiesta di "Creazione di una nuova struttura di flusso" con il payload "create_payload"
    Allora il PSP riceve il codice di stato HTTP 201

  @runnable
  @fdr3_001_02
  Schema dello scenario: Aggiunta di pagamenti al flusso
    Dato che il PSP deve inviare <n> pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è <amount>
    E che lo scenario "Creazione del flusso di rendicontazione per il test di aggiunta pagamenti" è stato eseguito con successo
    Quando il PSP aggiunge <n> pagamenti la cui somma è <amount> al flusso di rendicontazione flow_name come payments_payload
    E il PSP invia la richiesta di "Aggiunta pagamenti" con il payload "payments_payload"
    Allora il PSP riceve il codice di stato HTTP <code>

    Esempi:
      | n    | amount | code |
      | 1    | 3      | 200  |
      | 1000 | 29999  | 200  |
      | 1001 | 30000  | 400  |

