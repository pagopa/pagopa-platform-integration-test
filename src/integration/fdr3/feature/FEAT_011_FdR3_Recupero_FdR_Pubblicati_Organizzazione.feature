#language: it
@integration
@FDR3_011
Funzionalità: Recupero FdR pubblicati per organizzazione

  Contesto:
    Dato che i sistemi sono operativi

  @runnable
  @FDR3_011_01
  @positive
  Scenario: Recupero di tutti i FdR pubblicati
    Quando l'organizzazione invia la richiesta di "recupero di tutti i fdr pubblicati dall'organizzazione" con il payload "None"
    Allora l'organizzazione riceve il codice di stato HTTP 200

  @runnable
  @FDR3_011_02
  @positive
  Scenario: Recupero di tutti i FdR pubblicati filtrati per PSP
    Dato la configurazione psp è valorizzata come pspId nei parametri di query
    Quando l'organizzazione invia la richiesta di "recupero di tutti i fdr pubblicati dall'organizzazione" con il payload "None"
    Allora l'organizzazione riceve il codice di stato HTTP 200
    E l'organizzazione riceve tutti i FdR con lo stesso pspId
    
  @runnable
  @FDR3_011_03
  @positive
  Scenario: Recupero di tutti i FdR pubblicati da ieri
    Dato la configurazione psp è valorizzata come pspId nei parametri di query
    E l'organizzazione aggiunge ieri come publishedGt nei parametri di query
    Quando l'organizzazione invia la richiesta di "recupero di tutti i fdr pubblicati dall'organizzazione" con il payload "None"
    Allora l'organizzazione riceve il codice di stato HTTP 200
    E l'organizzazione riceve tutti i FdR con pspId uguale al valore di pspId nei parametri di query
    E l'organizzazione riceve tutti i FdR con published > publishedGt
