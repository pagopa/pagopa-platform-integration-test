#3203367024
#language:it
@ConversioneDaJSONaXML_007
Funzionalità: Ccnversione da JSON a XML di un Fdr

  Contesto:
    Dati i sistemi sono operativi

#======================================================
#======================================================

@ConversioneDaJSONaXML_007_01
Scenario: Conversione da Json a XML
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" è in stato PUBLISHED
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" si trova all'interno di fdr3-flows
  Quando Viene attivato il convertitore JSON to XML tramite la post /notify/fdr
  Allora su Fdr1 è presente il flusso di rendicontazione "2025-01-01PSPDEMO-0001" in formato XML
  

#======================================================
#======================================================

@ConversioneDaJSONaXML_007_02
Scenario: Recovery manuale singolo
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" è in stato PUBLISHED
  E che il flusso di rendicontazione "2025-01-01PSPDEMO-0001" si trova all'interno di fdr3-flows
  E che la conversione del flusso di rendicontazione "2025-01-01PSPDEMO-0001" è andata in errore
  Quando Viene chiamato il servizio di retry singolo tramite la GET /errors/{blobName}/retry 
  Allora su Fdr1 è presente il flusso di rendicontazione "2025-01-01PSPDEMO-0001" in formato XML
  
#======================================================
#======================================================

@ConversioneDaJSONaXML_007_03
Scenario: Recovery massivo
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E che X flussi di rendicontazione sono in stato PUBLISHED
  E che X flussi di rendicontazione sono all'interno di fdr3-flows
  E che la conversione dei flussi di rendicontazione è andata in errore
  Quando Viene chiamato il servizio di retry massivo tramite la GET /errors/retry
  Allora su Fdr1 sono presenti tutti gli X flussi di rendicontazione in formato XML
  

  
