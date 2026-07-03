#3087794384
#language:it
@CancellazioneDiUnFdR_006
Funzionalità: Cancellazione del flusso completo

#======================================================
#======================================================

@CancellazioneDiUnFdR_006_01
Scenario: Cancellazione di un flusso completo FdR 
  Dato I sistemi sono avviati
  E Il PSP PSPDEMO è correttamente censito a sistema
  E L’FDR 2025-01-01PSPDEMO-0001 è presente all’interno della flow table
  Quando Il PSP  invia una richiesta di cancellazione di un flusso attraverso la chiamata delete /psps/{pspId}/fdrs/{fdr} 
  Allora Il PSP riceve un codice 200 OK
  E L’fdr non è più presente

#======================================================
#======================================================

@CancellazioneDiUnFdR_006_02
Scenario: Cancellazione di un FdR inesistente
  Dato I sistemi sono avviati
  E Il PSP PSPDEMO correttamente censito a sistema
  Quando Il PSP  invia una richiesta di cancellazione di un flusso attraverso la delete /psps/{pspId}/fdrs/{fdr}  inserendo un valore di {fdr} inesistente
  Allora il PSP riceve un errore 404 Not Found


#======================================================
#======================================================

@CancellazioneDiUnFdR_006_03
Scenario:  Cancellazione di un FdR in stato  CREATED
  Dato I sistemi sono avviati
  E Il PSP PSPDEMO è correttamente censito a sistema
  E L’FDR 2025-01-01PSPDEMO-0001 è presente all’interno della flow table con stato CREATED
  Quando Il PSP  invia una richiesta di cancellazione di un flusso attraverso la chiamata delete /psps/{pspId}/fdrs/{fdr}
  Allora il PSP riceve un errore 400 Bad Request
     

#======================================================
#======================================================

@CancellazioneDiUnFdR_006_04
Scenario: Cancellazione di un FdR in stato PUBLISHED
 Dato I sistemi sono avviati
 E Il PSP PSPDEMO è correttamente censito a sistema
 E L’FDR 2025-01-01PSPDEMO-0001 è presente all’interno della flow table con stato PUBLISHED
 Quando Il PSP  invia una richiesta di cancellazione di un flusso attraverso la chiamata delete /psps/{pspId}/fdrs/{fdr}
 Allora il PSP riceve un errore 400 Bad Request


#======================================================
#======================================================

@CancellazioneDiUnFdR_006_05
Scenario:  Cancellazione di un FdR per PSP non presente a sistema
 Dato I sistemi sono avviati
 E Il pspTest non è censito a sistema
 E Il PSP vuole cancellare un flusso di rendicontazione con id 2016-08-16pspTest-1178
 Quando Il PSP  invia una richiesta di cancellazione di un flusso attraverso la chiamata delete /psps/{pspId}/fdrs/{fdr}
 Allora il PSP riceve un errore 400 Bad Request


#======================================================
#======================================================

@CancellazioneDiUnFdR_006_06
Scenario: Il PSP è presente a sistema ma non è in stato ENABLED
 Dato I sistemi sono avviati
 E Il PSP pspTest è censito a sistema ma non è nello stato ENABLED
 E Il PSP vuole cancellare un flusso di rendicontazione con id 2016-08-16pspTest-11788
 Quando Il PSP  invia una richiesta di cancellazione di un flusso attraverso la chiamata delete /psps/{pspId}/fdrs/{fdr}
 Allora il PSP riceve un errore 400 Bad Request