# 3078848524
# language:it
@PubblicazioneFdR_003
Funzionalità: Pubblicazione di un FdR

#======================================================
#======================================================

@PubblicazioneFdR_003_01
Scenario: Pubblicazione di un Fdr
  Dato I sistemi sono avviati
  E Il PSP PSPDEMO è correttamente censito a sistema
  E L’FDR 2025-01-01PSPDEMO-0001 è presente all’interno della flow table in stato INSERTED
  Quando Il PSP avvia una richiesta di pubblicazione flusso attraverso la post /psps/{pspId}/fdrs/{fdr}/publish 
  Allora Il parametro is_Latest viene settato a TRUE
  E La data corrente viene impostata come publish date
  E La data corrente viene impostata come last update dates
  E Lo stato dell’FDR viene impostato a PUBLISHED
  E Il PSP riceve un codice 200 OK


#======================================================
#======================================================

@PubblicazioneFdR_003_02
Scenario outline: Pubblicazione FdR KO
  Dato I sistemi sono avviati
  E Il PSP PSPDEMO correttamente censito a sistema
  E Il PSP vuole recuperare un FdR con identificativo diverso da {YYYY-MM-DD}{PSP_ID}-{suffisso}
  Quando Il PSP avvia una richiesta di pubblicazione flusso attraverso la post /psps/{pspId}/fdrs/{fdr}/publish 
  Allora il PSP riceve un errore 404 Not Found

  Esempi:
   | YYYY-MM-DD | PSP_ID      | suffisso  | 
   | 2025-13-01 | 60000000001 | 0001      |
   | 2025-01-01 | 6000000000/ | 0001      |
   | 2025-01-01 | 60000000001 | 000+      |
   
#======================================================
#======================================================

@PubblicazioneFdR_003_03
Scenario:  Pubblicazione di un FdR in stato  CREATED
  Dato I sistemi sono avviati
  E Il PSP PSPDEMO è correttamente censito a sistema
  E L’FDR 2025-01-01PSPDEMO-0001 è presente all’interno della flow table con stato CREATED
  Quando Il PSP avvia una richiesta di pubblicazione flusso attraverso la post /psps/{pspId}/fdrs/{fdr}/publish
  Allora il PSP riceve un errore 400 Bad Request

#======================================================
#======================================================

@PubblicazioneFdR_003_04
Scenario: Pubblicazione di un FdR in stato PUBLISHED
 Dato I sistemi sono avviati
 E Il PSP PSPDEMO è correttamente censito a sistema
 E L’FDR 2025-01-01PSPDEMO-0001 è presente all’interno della flow table con stato PUBLISHED
 Quando Il PSP avvia una richiesta di pubblicazione flusso attraverso la post /psps/{pspId}/fdrs/{fdr}/publish
 Allora il PSP riceve un errore 400 Bad Request

#======================================================
#======================================================

@PubblicazioneFdR_003_05
Scenario:  Pubblicazione del flusso per PSP non presente a sistema
 Dato I sistemi sono avviati
 E Il pspTest non è censito a sistema
 E Il PSP vuole pubblicare un flusso di rendicontazione con id 2016-08-16pspTest-1178
 Quando Il PSP avvia una richiesta di pubblicazione flusso attraverso la post /psps/{pspId}/fdrs/{fdr}/publish
 Allora Il  PSP riceve il codice di stato HTTP 400


#======================================================
#======================================================

@PubblicazioneFdR_003_06
Scenario: Il PSP è presente a sistema ma non è in stato ENABLED
 Dato I sistemi sono avviati
 E Il PSP pspTest è censito a sistema ma non è nello stato ENABLED
 E Il PSP vuole pubblicare un flusso di rendicontazione con id 2016-08-16pspTest-1178
 Quando Il PSP avvia una richiesta di pubblicazione flusso attraverso la post /psps/{pspId}/fdrs/{fdr}/publish
 Allora Il  PSP riceve il codice di stato HTTP 400