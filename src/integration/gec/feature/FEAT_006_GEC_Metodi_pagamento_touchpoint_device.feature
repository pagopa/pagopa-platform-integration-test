#language: it
@integration
@gec_006_Metodi_pagamento_touchpoint_device

Funzionalità: Ricerca dei metodi di pagamento per touchpoint e dispositivo utente

  Contesto:
    Dato che i sistemi sono operativi
    E la configurazione dei dati di test è caricata

  @runnable
  @happy_path
  @gec_006_01
  Scenario: Ricerca con touchpoint IO presente nella configurazione dei metodi di pagamento
    Dato la configurazione dei metodi di pagamento "payment-methods-user-touchpoint-ok"
    E una richiesta di ricerca dei metodi di pagamento "ricerca_metodi_touchpoint_io_ios"
    Quando il client invia la richiesta di "Ricerca metodi di pagamento"
    Allora il sistema risponde con codice di stato 200
    E la risposta contiene i metodi di pagamento di test configurati
    E il metodo "cart" è il primo della risposta
    E i metodi diversi da "cart" sono in ordine alfabetico

  @runnable
  @happy_path
  @gec_006_02
  Scenario: Ricerca con touchpoint IO non presente nella configurazione dei metodi di pagamento
    Dato la configurazione dei metodi di pagamento "payment-methods-user-touchpoint-ko"
    E una richiesta di ricerca dei metodi di pagamento "ricerca_metodi_touchpoint_io_ios"
    Quando il client invia la richiesta di "Ricerca metodi di pagamento"
    Allora il sistema risponde con codice di stato 200
    E la risposta non contiene i metodi di pagamento di test configurati

  @runnable
  @happy_path
  @gec_006_03
  Scenario: Ricerca con dispositivo utente WEB presente nella configurazione dei metodi di pagamento
    Dato la configurazione dei metodi di pagamento "payment-methods-user-device-ok"
    E una richiesta di ricerca dei metodi di pagamento "ricerca_metodi_device_web"
    Quando il client invia la richiesta di "Ricerca metodi di pagamento"
    Allora il sistema risponde con codice di stato 200
    E la risposta contiene i metodi di pagamento di test configurati
    E il metodo "cart" è il primo della risposta
    E i metodi diversi da "cart" sono in ordine alfabetico

  @runnable
  @happy_path
  @gec_006_04
  Scenario: Ricerca senza indicare il dispositivo utente
    Dato la configurazione dei metodi di pagamento "payment-methods-user-device-ok"
    E una richiesta di ricerca dei metodi di pagamento "ricerca_metodi_senza_device"
    Quando il client invia la richiesta di "Ricerca metodi di pagamento"
    Allora il sistema risponde con codice di stato 200
    E la risposta contiene i metodi di pagamento di test configurati
    E il metodo "cart" è il primo della risposta
    E i metodi diversi da "cart" sono in ordine alfabetico

  @runnable
  @happy_path
  @gec_006_05
  Scenario: Ricerca con dispositivo utente WEB non presente nella configurazione dei metodi di pagamento
    Dato la configurazione dei metodi di pagamento "payment-methods-user-device-ko"
    E una richiesta di ricerca dei metodi di pagamento "ricerca_metodi_device_web"
    Quando il client invia la richiesta di "Ricerca metodi di pagamento"
    Allora il sistema risponde con codice di stato 200
    E la risposta non contiene i metodi di pagamento di test configurati

  @runnable
  @negative
  @gec_006_06
  Schema dello scenario: Ricerca rifiutata per touchpoint o dispositivo utente con valore non valido
    Dato la configurazione dei metodi di pagamento "<configurazione>"
    E una richiesta di ricerca dei metodi di pagamento "<richiesta>"
    Quando il client invia la richiesta di "Ricerca metodi di pagamento"
    Allora il sistema risponde con codice di stato 400
    E il corpo della risposta corrisponde al payload "ricerca_metodi_input_non_valido_response"

    Esempi:
      | configurazione                     | richiesta                            |
      | payment-methods-user-touchpoint-ko | ricerca_metodi_touchpoint_non_valido |
      | payment-methods-user-device-ko     | ricerca_metodi_device_non_valido     |
