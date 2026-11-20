#language: it
@integration
@gec_007_Metodi_pagamento_importo

Funzionalità: Ricerca dei metodi di pagamento per importo

  Contesto:
    Dato che i sistemi sono operativi
    E la configurazione dei dati di test è caricata

  @positive
  @gec_007_01
  Scenario: Ricerca con importo fuori intervallo solo per il metodo PAYPAL-test
    Dato la configurazione dei metodi di pagamento "payment-methods-range-amount"
    E una richiesta di ricerca dei metodi di pagamento "ricerca_metodi_importo_1200"
    Quando il client invia la richiesta di "Ricerca metodi di pagamento"
    Allora il sistema risponde con codice di stato 200
    E la risposta contiene i metodi di pagamento di test configurati
    E solo il metodo "PAYPAL-test" è disabilitato per AMOUNT_OUT_OF_BOUND
    E il metodo "cart" è il primo della risposta
    E i metodi diversi da "cart" sono in ordine alfabetico

  @positive
  @gec_007_02
  Scenario: Ricerca con importo fuori intervallo per entrambi i metodi di pagamento di test
    Dato la configurazione dei metodi di pagamento "payment-methods-total-amount"
    E una richiesta di ricerca dei metodi di pagamento "ricerca_metodi_importo_200"
    Quando il client invia la richiesta di "Ricerca metodi di pagamento"
    Allora il sistema risponde con codice di stato 200
    E la risposta contiene i metodi di pagamento di test configurati
    E entrambi i metodi di pagamento di test sono disabilitati per AMOUNT_OUT_OF_BOUND

  @positive
  @gec_007_03
  Scenario: Ricerca con importo negativo per entrambi i metodi di pagamento di test
    Dato la configurazione dei metodi di pagamento "payment-methods-total-amount"
    E una richiesta di ricerca dei metodi di pagamento "ricerca_metodi_importo_negativo"
    Quando il client invia la richiesta di "Ricerca metodi di pagamento"
    Allora il sistema risponde con codice di stato 200
    E la risposta contiene i metodi di pagamento di test configurati
    E entrambi i metodi di pagamento di test sono disabilitati per AMOUNT_OUT_OF_BOUND
    E il metodo "cart" è il primo della risposta
    E i metodi diversi da "cart" sono in ordine alfabetico

  @positive
  @gec_007_04
  Scenario: Ricerca con importo in intervallo per entrambi i metodi di pagamento di test
    Dato la configurazione dei metodi di pagamento "payment-methods-total-amount"
    E una richiesta di ricerca dei metodi di pagamento "ricerca_metodi_importo_5"
    Quando il client invia la richiesta di "Ricerca metodi di pagamento"
    Allora il sistema risponde con codice di stato 200
    E la risposta contiene i metodi di pagamento di test configurati
    E entrambi i metodi di pagamento di test sono abilitati
    E il metodo "cart" è il primo della risposta
    E i metodi diversi da "cart" sono in ordine alfabetico
