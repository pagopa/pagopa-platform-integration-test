#3223846950
#language:it
@RecuperoFdR1_010
Funzionalità: Recupero degli fdr su FdR1 da parte dell'EC

  Contesto:
    Dati i sistemi sono operativi

#======================================================
#======================================================

@RecuperoFdR1_010_01
Scenario: Richiesta singolo flusso
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E  l'fdr "2025-01-01PSPDEMO-0001" è presente su FdR1
  Quando il PSP invia una richiesta di recupero tramite la nodoChiediFlussoRendicontazione per l'fdr "2025-01-01PSPDEMO-0001"
  Allora il sistema risponde con il codice di stato HTTP 200
  E Il PSP riceve l'XML relativo all' FdR "2025-01-01PSPDEMO-0001"


#======================================================
#======================================================

@RecuperoFdR1_010_02
Scenario: Richiesta elenco di flussi
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  Quando il PSP invia una richiesta di recupero massivo tramite nodoChiediElencoFlussiRendicontazione per il PSP con pspId "PSPDEMO"
  Allora il sistema risponde con il codice di stato HTTP 200
  E Il PSP riceve l'XML relativo all' insieme dei FdR relativi al psp con pspId "PSPDEMO"


#======================================================
#======================================================

@RecuperoFdR1_010_03
Scenario: Richiesta singolo flusso per flusso non presente
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E  l'fdr "2025-01-01PSPDEMO-0001" non è presente su FdR1
  Quando il PSP invia una richiesta di recupero tramite la nodoChiediFlussoRendicontazione per l'fdr "2025-01-01PSPDEMO-0001"
  Allora il sistema risponde con il codice di stato HTTP 200
  E nella risposta è riportato il codice di errore 404



#======================================================
#======================================================

@RecuperoFdR1_010_04
Scenario: Richiesta elenco di flussi non presenti
  Dato Il PSP "PSPDEMO" con pspId "PSPDEMO" è correttamente censito a sistema
  E non sono presenti flussi per il PSP con pspId "PSPDEMO" su FdR1
  Quando il PSP invia una richiesta di recupero massivo tramite nodoChiediElencoFlussiRendicontazione per il PSP con pspId "PSPDEMO"
  Allora il sistema risponde con il codice di stato HTTP 200
  E nella risposta è riportato il codice di errore 404


#======================================================
#======================================================