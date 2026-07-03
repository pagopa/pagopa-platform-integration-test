#3078946877
#language:it
@CancellazioneDiUnooPiuPagamentiFdR_004
Funzionalità: Cancellazione di uno o più pagamenti

#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_01
Scenario: Cancellazione di un pagamento all’interno dell’FdR
  Dato I sistemi sono avviati
  E Il PSP PSPDEMO è correttamente censito a sistema
  E L’FDR 2025-01-01PSPDEMO-0001 è presente all’interno della flow table e contiene totPayments pagamenti con amount sumPayments
  Quando Il PSP  invia una richiesta di cancellazione di n pagamenti  con amount a attraverso la put /psps/{pspId}/fdrs/{fdr}/payments/del indicando nel body una index list {indexList*: [integer]} con l’indice dei pagamenti da eliminare 
  Allora Il numero residuo di pagamenti nel flusso viene aggiornato con  totPayments-n
  E L’amount totale viene correttamente aggiornato con sumPayments-a
  E La data corrente viene impostata come last update dates
  E I pagamenti da eliminare non sono più associati all’fdr
  E Il PSP riceve un codice 200 OK

#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_02
Scenario: Cancellazione di tutti i pagamenti all’interno dell’FdR 
  Dato I sistemi sono avviati
  E Il PSP PSPDEMO è correttamente censito a sistema
  E L’FDR 2025-01-01PSPDEMO-0001 è presente all’interno della flow table e contiene m pagamenti
  Quando Il PSP  invia una richiesta di cancellazione di tutti gli m pagamenti attraverso la put /psps/{pspId}/fdrs/{fdr}/payments/del
  Allora Il numero residuo di pagamenti nel flusso è 0
  E L’amount totale viene correttamente aggiornato a 0
  E La data corrente viene impostata come last update dates
  E Lo stato dell’FDR viene impostato a CREATED
  E I pagamenti da eliminare non sono più associati all’fdr
  E Il PSP riceve un codice 200 OK

#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_03
Scenario: Cancellazione di pagamenti con FdR KO
  Dato I sistemi sono avviati
  E Il PSP PSPDEMO correttamente censito a sistema
  E L’FdR id su cui cancellare i pagamenti non è censito a sistema
  Quando Il PSP  invia una richiesta di cancellazione dei pagamenti attraverso la put /psps/{pspId}/fdrs/{fdr}/payments/del 
  Allora il PSP riceve un errore 404 Not Found


#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_04
Scenario:  Cancellazione di più pagamenti di quanti presenti nell' FdR
  Dato I sistemi sono avviati
  E Il PSP PSPDEMO è correttamente censito a sistema
  E L’FdR 2025-01-01PSPDEMO-0001 su cui cancellare i pagamenti è censito a sistema e contiene n pagamenti
  Quando Il PSP  invia una richiesta di cancellazione dei pagamenti attraverso la put /psps/{pspId}/fdrs/{fdr}/payments/del indicando nel body una index list {indexList*: [n+1]}
  Allora il PSP riceve un errore 400 Bad Request

#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_05
Scenario:  Cancellazione dei pagamenti di un FdR in stato  CREATED
  Dato I sistemi sono avviati
  E Il PSP PSPDEMO è correttamente censito a sistema
  E L’FDR 2025-01-01PSPDEMO-0001 è presente all’interno della flow table con stato CREATED
  Quando Il PSP  invia una richiesta di cancellazione dei pagamenti attraverso la put /psps/{pspId}/fdrs/{fdr}/payments/del
  Allora il PSP riceve un errore 400 Bad Request
     

#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_06
Scenario: Cancellazione dei pagamenti di un FdR in stato PUBLISHED
 Dato I sistemi sono avviati
 E Il PSP PSPDEMO è correttamente censito a sistema
 E L’FDR 2025-01-01PSPDEMO-0001 è presente all’interno della flow table con stato PUBLISHED
 Quando Il PSP  invia una richiesta di cancellazione dei pagamenti attraverso la put /psps/{pspId}/fdrs/{fdr}/payments/del 
 Allora il PSP riceve un errore 400 Bad Request


#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_07
Scenario:  Cancellazione dei pagamenti per PSP non presente a sistema
 Dato I sistemi sono avviati
 E Il pspTest non è censito a sistema
 E Il PSP vuole cancellare dei pagamenti per un flusso di rendicontazione con id 2016-08-16pspTest-1178
 Quando Il PSP  invia una richiesta di cancellazione dei pagamenti attraverso la put /psps/{pspId}/fdrs/{fdr}/payments/del
 Allora Il  PSP riceve il codice di stato HTTP 400


#======================================================
#======================================================

@CancellazioneDiUnooPiuPagamentiFdR_004_08
Scenario: Il PSP è presente a sistema ma non è in stato ENABLED
 Dato I sistemi sono avviati
 E Il PSP pspTest è censito a sistema ma non è nello stato ENABLED
 E Il PSP vuole cancellare dei pagamenti per un flusso di rendicontazione con id 2016-08-16pspTest-11788
 Quando Il PSP  invia una richiesta di cancellazione dei pagamenti attraverso la put /psps/{pspId}/fdrs/{fdr}/payments/del
 Allora Il  PSP riceve il codice di stato HTTP 400