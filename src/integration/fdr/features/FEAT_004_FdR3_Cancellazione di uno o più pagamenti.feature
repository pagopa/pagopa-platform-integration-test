#3078946877
#language:it
@CancellazioneDiUnooPiuPagamentiFdR_004
Funzionalità: Cancellazione di uno o più pagamenti

  Contesto:
    Dati i sistemi sono operativi

#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_01
@Crea_FdR(id_fdr="2025-01-01PSPDEMO-0001",id_psp="PSPDEMO")
@Inserisci_Pagamenti(totPayments=3,sumPayments=3000)
Scenario: Cancellazione di un pagamento all’interno dell’FdR
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" esiste in stato "INSERTED"
  E contiene totPayments pagamenti con amount sumPayments
  Quando si vuole cancellare n pagamenti con amount a
  E Il PSP invia una richiesta di cancellazione attraverso l'API "Delete one or more payments from an existing flow"
  Allora il sistema risponde con il codice di stato HTTP 200
  E Il numero residuo di pagamenti nel flusso viene aggiornato con totPayments-n
  E L’amount totale viene correttamente aggiornato con sumPayments-a
  E La data corrente viene impostata come last update dates
  E I pagamenti da eliminare non sono più associati all’fdr


#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_02
@Crea_FdR(id_fdr="2025-01-01PSPDEMO-0001",id_psp="PSPDEMO")
@Inserisci_Pagamenti(totPayments=3,sumPayments=3000)
Scenario: Cancellazione di tutti i pagamenti all’interno dell’FdR 
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" esiste in stato "INSERTED"
  E contiene m pagamenti
  Quando si vuole cancellare tutti gli m pagamenti
  E Il PSP invia una richiesta di cancellazione attraverso l'API "Delete one or more payments from an existing flow"
  Allora il sistema rispone con il codice di stato HTTP 200
  E Il numero residuo di pagamenti nel flusso è 0
  E L’amount totale viene correttamente aggiornato a 0
  E La data corrente viene impostata come last update dates
  E Lo stato dell’FDR viene impostato a "CREATED"
  E I pagamenti da eliminare non sono più associati all’fdr

#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_03
Scenario: Cancellazione di pagamenti con FdR KO
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-9999" non esiste a sistema
  Quando Il PSP invia una richiesta di cancellazione attraverso l'API "Delete one or more payments from an existing flow"
  Allora il sistema rispone con il codice di stato HTTP 404


#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_04
@Crea_FdR(id_fdr="2025-01-01PSPDEMO-0001",id_psp="PSPDEMO")
@Inserisci_Pagamenti(totPayments=3,sumPayments=3000)
Scenario:  Cancellazione di più pagamenti di quanti presenti nell' FdR
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" esiste in stato "INSERTED"
  E contiene totPayments pagamenti
  Quando si vuole cancellare n pagamenti con n>totPayments
  E Il PSP invia una richiesta di cancellazione dei pagamenti attraverso l'API "Delete one or more payments from an existing flow"
  Allora il PSP riceve un errore 400 Bad Request

#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_05
@Crea_FdR(id_fdr="2025-01-01PSPDEMO-0001",id_psp="PSPDEMO")
Scenario:  Cancellazione dei pagamenti di un FdR in stato  CREATED
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" esiste in stato "CREATED"
  Quando Il PSP invia una richiesta di cancellazione dei pagamenti attraverso l'API "Delete one or more payments from an existing flow"
  Allora il PSP riceve un errore 400 Bad Request
     

#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_06
@Crea_FdR(id_fdr="2025-01-01PSPDEMO-0001",id_psp="PSPDEMO")
@Inserisci_Pagamenti(totPayments=3,sumPayments=3000)
@Pubblica_FdR
Scenario: Cancellazione dei pagamenti di un FdR in stato PUBLISHED
 Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
 E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" esiste in stato "PUBLISHED"
 Quando Il PSP invia una richiesta di cancellazione dei pagamenti attraverso l'API "Delete one or more payments from an existing flow"
 Allora il PSP riceve un errore 400 Bad Request


#======================================================
#======================================================
#Da controllare. Non è possibile creader FdR per PSP non censito a sistema. Il test non è corretto.
@CancellazioneDiUnooPiuPagamentiFdR_004_07
@Crea_FdR(id_fdr="2016-08-16pspTest-1178",id_psp="pspTest")
Scenario:  Cancellazione dei pagamenti per PSP non presente a sistema
 Dato Il PSP "pspTest" con pspId "pspTest" non è censito a sistema
 E che il flusso di rendicontazione "2016-08-16pspTest-1178" esiste in stato "INSERTED"
 Quando Il PSP invia una richiesta di cancellazione dei pagamenti attraverso l'API "Delete one or more payments from an existing flow"
 Allora Il PSP riceve il codice di stato HTTP 400


#======================================================
#======================================================
#======================================================
#Da controllare. Non è possibile creare FdR per PSP in stato non ENABLED. Il test non è riproducibile senza un FdR già censito a sistema.
@CancellazioneDiUnooPiuPagamentiFdR_004_08
Scenario: Il PSP è presente a sistema ma non è in stato ENABLED
 Dato Il PSP "pspTest" con pspId "pspTest" è censito a sistema
 E il PSP non è nello stato "ENABLED"
 E che il flusso di rendicontazione "2016-08-16pspTest-1178" esiste in stato "INSERTED"
 Quando Il PSP invia una richiesta di cancellazione dei pagamenti attraverso l'API "Delete one or more payments from an existing flow"
 Allora Il PSP riceve il codice di stato HTTP 400