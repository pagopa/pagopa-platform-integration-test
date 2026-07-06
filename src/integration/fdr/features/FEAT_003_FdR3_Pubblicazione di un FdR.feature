# 3078848524
# language:it
@PubblicazioneFdR_003
Funzionalità: Pubblicazione di un FdR

  Contesto:
    Dati i sistemi sono operativi

#======================================================
#======================================================

@PubblicazioneFdR_003_01
@Crea_FdR(id_fdr="2025-01-01PSPDEMO-0001",id_psp="PSPDEMO")
@Inserisci_Pagamenti(totPayments=3,sumPayments=3000)
Scenario: Pubblicazione di un Fdr
  Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" esiste in stato "INSERTED"
  Quando il PSP avvia una richiesta di pubblicazione flusso attraverso l'API "Publish an existing flow in draft status"
  Allora il sistema risponde con il codice di stato HTTP 200
  E il parametro is_Latest viene settato a "TRUE"
  E La data corrente viene impostata come publish date
  E La data corrente viene impostata come last update dates
  E Lo stato dell’FDR viene impostato a "PUBLISHED"


#======================================================
#======================================================

@PubblicazioneFdR_003_02
Scenario outline: Pubblicazione FdR KO
  Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
  E il PSP vuole recuperare un FdR con identificativo diverso da "<data_regolamento><istituto_mittente>-<flusso>"
  Quando il PSP avvia una richiesta di pubblicazione flusso attraverso l'API "Publish an existing flow in draft status"
  Allora il sistema risponde con il codice di stato HTTP 404

  Esempi:
   | data_regolamento | istituto_mittente | flusso | 
   | 2025-13-01       | 60000000001       | 0001   |
   | 2025-01-01       | 6000000000/       | 0001   |
   | 2025-01-01       | 60000000001       | 000+   |
   
#======================================================
#======================================================

@PubblicazioneFdR_003_03
@Crea_FdR(id_fdr="2025-01-01PSPDEMO-0001")
Scenario:  Pubblicazione di un FdR in stato  CREATED
  Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" esiste in stato "CREATED"
  Quando il PSP avvia una richiesta di pubblicazione flusso attraverso l'API "Publish an existing flow in draft status"
  Allora il sistema risponde con il codice di stato HTTP 400

#======================================================
#======================================================

@PubblicazioneFdR_003_04
@Crea_FdR(id_fdr="2025-01-01PSPDEMO-0001",id_psp="PSPDEMO")
@Inserisci_Pagamenti(totPayments=3,sumPayments=3000)
@Pubblica_FdR
Scenario: Pubblicazione di un FdR in stato PUBLISHED
  Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" esiste in stato "PUBLISHED"
  Quando il PSP avvia una richiesta di pubblicazione flusso attraverso l'API "Publish an existing flow in draft status"
  Allora il sistema risponde con il codice di stato HTTP 400

#======================================================
#========== NON APPLICABILI ===========================
#======================================================
#Non è possibile creare FdR per PSP non censito a sistema. Il test non è riproducibile senza un FdR già censito a sistema.
#@PubblicazioneFdR_003_05
#Scenario:  Pubblicazione del flusso per PSP non presente a sistema
# Dato il PSP "pspTest" con pspId "pspTest" non è censito a sistema
# E il PSP vuole pubblicare un flusso di rendicontazione con id "2016-08-16pspTest-1178"
# Quando il PSP avvia una richiesta di pubblicazione flusso attraverso l'API "Publish an existing flow in draft status"
# Allora il sistema risponde con il codice di stato HTTP 400

#Non è possibile creare FdR per PSP in stato non ENABLED. Il test non è riproducibile senza un FdR già censito a sistema.
#@PubblicazioneFdR_003_06
#@Crea_FdR(id_fdr="2016-08-16pspTest-1178",id_psp="pspTest")
#Scenario: Il PSP è presente a sistema ma non è in stato ENABLED
# Dato il PSP "pspTest" con pspId "pspTest" è censito a sistema ma non è nello stato "ENABLED"
# E il PSP vuole pubblicare un flusso di rendicontazione con id "2016-08-16pspTest-1178"
# Quando il PSP avvia una richiesta di pubblicazione flusso attraverso l'API "Publish an existing flow in draft status"
# Allora il sistema risponde con il codice di stato HTTP 400