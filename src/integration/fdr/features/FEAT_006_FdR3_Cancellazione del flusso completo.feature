#3087794384
#language:it
@CancellazioneDiUnFdR_006
Funzionalità: Cancellazione del flusso completo

  Contesto:
    Dati i sistemi sono operativi

#======================================================
#======================================================

@CancellazioneDiUnFdR_006_01
@Crea_FdR(id_fdr="2025-01-01PSPDEMO-0001",id_psp="PSPDEMO")
@Inserisci_Pagamenti(totPayments=3,sumPayments=3000)
Scenario: Cancellazione di un flusso completo FdR 
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" esiste in stato "INSERTED" 
  Quando Il PSP invia una richiesta di cancellazione di un flusso attraverso l'API "Delete an existing draft flow and all related payments"
  Allora il sistema risponde con il codice di stato HTTP 200
  E L’fdr non è più presente

#======================================================
#======================================================

@CancellazioneDiUnFdR_006_02
Scenario: Cancellazione di un FdR inesistente
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-9999" non esiste a sistema
  Quando Il PSP invia una richiesta di cancellazione di un flusso attraverso l'API "Delete an existing draft flow and all related payments"
  Allora il sistema risponde con il codice di stato HTTP 404


#======================================================
#======================================================

@CancellazioneDiUnFdR_006_03
@Crea_FdR(id_fdr="2025-01-01PSPDEMO-0001",id_psp="PSPDEMO")
Scenario:  Cancellazione di un FdR in stato  CREATED
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" esiste in stato "CREATED"
  Quando Il PSP invia una richiesta di cancellazione di un flusso attraverso l'API "Delete an existing draft flow and all related payments"
  Allora il sistema risponde con il codice di stato HTTP 400

#======================================================
#======================================================

@CancellazioneDiUnFdR_006_04
@Crea_FdR(id_fdr="2025-01-01PSPDEMO-0001",id_psp="PSPDEMO")
@Inserisci_Pagamenti(totPayments=3,sumPayments=3000)
@Pubblica_FdR
Scenario: Cancellazione di un FdR in stato PUBLISHED
 Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
 E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" esiste in stato "PUBLISHED"
 Quando Il PSP invia una richiesta di cancellazione di un flusso attraverso l'API "Delete an existing draft flow and all related payments"
 Allora il sistema risponde con il codice di stato HTTP 400


#======================================================
#======================================================
#Da controllare. Non è possibile creare FdR per PSP non censito a sistema. Il test non è riproducibile senza un FdR già censito a sistema.
@CancellazioneDiUnFdR_006_05
Scenario:  Cancellazione di un FdR per PSP non presente a sistema
 Dato Il PSP "pspTest" con pspId "pspTest" non è censito a sistema
 Quando Il PSP invia una richiesta di cancellazione di un flusso attraverso l'API "Delete an existing draft flow and all related payments"
 Allora il sistema risponde con il codice di stato HTTP 400


#======================================================
#======================================================
#Da controllare. Non è possibile creare FdR per PSP in stato non ENABLED. Il test non è riproducibile senza un FdR già censito a sistema.
@CancellazioneDiUnFdR_006_06
Scenario: Il PSP è presente a sistema ma non è in stato ENABLED
 Dato Il PSP "pspTest" con pspId "pspTest" è censito a sistema 
 E il PSP non è nello stato "ENABLED"
 E che il flusso di rendicontazione "2016-08-16pspTest-11788" esiste a sistema
 Quando Il PSP invia una richiesta di cancellazione di un flusso attraverso l'API "Delete an existing draft flow and all related payments"
 Allora il sistema risponde con il codice di stato HTTP 400