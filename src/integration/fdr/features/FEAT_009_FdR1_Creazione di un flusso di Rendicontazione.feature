#3223257554
#language:it
@FdR1CreazioneFdR_009
Funzionalità: Creazione di un flusso di rendicontazione su FdR1

  Contesto:
    Dati i sistemi sono operativi

#======================================================
#======================================================


@FdR1CreazioneFdR_009_01
Scenario: Creazione FdR per EC non configurato come sFTP
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  Quando Il PSP invia l'fdr "2025-01-01PSPDEMO-0001" tramite la nodoInviaFlussoRendicontazione verso FDR1
  Allora il sistema risponde con il codice di stato HTTP 200 
  E viene ricevuto tramite response l'XML del flusso di rendicontazione
  E su FdR1 è presente l'fdr "2025-01-01PSPDEMO-0001" in formato XML
  

#======================================================
#======================================================


  