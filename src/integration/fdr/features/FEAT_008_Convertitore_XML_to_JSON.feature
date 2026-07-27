#3212745173
#language:it
@ConversioneDaXMLaJSON_008
Funzionalità: Ccnversione da XML a JSON di un Fdr

  Contesto:
    Dati i sistemi sono operativi

#======================================================
#======================================================

@ConversioneDaXMLaJSON_008_01
Scenario: Conversione da XML a JSON
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" si trova all'interno di fdr1-flows
  Quando Viene attivato il convertitore XML to JSON tramite la post /internal/psps/PSPDEMO/fdrs/2025-01-01PSPDEMO-0001
  Allora su Fdr3 è presente il flusso di rendicontazione "2025-01-01PSPDEMO-0001" in formato JSON
  E il flusso di rendicontazione "2025-01-01PSPDEMO-0001" SU FdR3 è in stato PUBLISHED
  


  

  
