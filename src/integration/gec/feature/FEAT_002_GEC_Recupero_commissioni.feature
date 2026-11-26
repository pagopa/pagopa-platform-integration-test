#language: it
@integration
@gec_002_Recupero_commissioni

Funzionalità: Recupero delle commissioni

  Contesto:
    Dato che i sistemi sono operativi
    E il bundle poste è configurato

  @runnable
  @happy_path
  @gec_002_01
  Scenario: Recupero delle commissioni per importo, metodo e touchpoint
    Dato una richiesta di recupero commissioni "commissioni_importo_metodo_touchpoint"
    E il parametro di richiesta "maxOccurrences" è "10"
    Quando il client invia la richiesta di "Recupero commissioni" con il payload "commissioni_importo_metodo_touchpoint" 
    Allora il sistema risponde con codice di stato 200
    E i valori del campo `onUs` delle opzioni bundle, dopo l'ordinamento previsto per l'API "V1", corrispondono ai seguenti:
      | onUs  |
      | true  |
      | false |
      | false |


  @runnable
  @happy_path
  @gec_002_02
  Scenario: Recupero delle commissioni per importo e metodo
    Dato una richiesta di recupero commissioni "commissioni_importo_metodo"
    E il parametro di richiesta "maxOccurrences" è "10"
    Quando il client invia la richiesta di "Recupero commissioni" con il payload "commissioni_importo_metodo" 
    Allora il sistema risponde con codice di stato 200
    E i valori del campo `onUs` delle opzioni bundle, dopo l'ordinamento previsto per l'API "V1", corrispondono ai seguenti:
      | onUs  |
      | true  |
      | true  |
      | false |
      | false |
      | false |
      | false |
      | false |
      | false |

  @runnable
  @happy_path
  @gec_002_03
  Scenario: Recupero delle commissioni per CI, importo, metodo e singolo PSP
    Dato una richiesta di recupero commissioni "commissioni_ci_importo_metodo_psp"
    E il parametro di richiesta "maxOccurrences" è "10"
    Quando il client invia la richiesta di "Recupero commissioni" con il payload "commissioni_ci_importo_metodo_psp" 
    Allora il sistema risponde con codice di stato 200
    E i valori del campo `onUs` delle opzioni bundle, dopo l'ordinamento previsto per l'API "V1", corrispondono ai seguenti:
      | onUs  |
      | true  |
      | false |

  @runnable
  @happy_path
  @gec_002_04
  Scenario: Recupero delle commissioni per CI, importo, touchpoint e singolo PSP
    Dato una richiesta di recupero commissioni "commissioni_ci_importo_touchpoint_psp"
    E il parametro di richiesta "maxOccurrences" è "10"
    Quando il client invia la richiesta di "Recupero commissioni" con il payload "commissioni_ci_importo_touchpoint_psp" 
    Allora il sistema risponde con codice di stato 200
    E i valori del campo `onUs` delle opzioni bundle, dopo l'ordinamento previsto per l'API "V1", corrispondono ai seguenti:
      | onUs  |
      | true  |
      | false |
      | false |

  @runnable
  @happy_path
  @gec_002_05
  Scenario: Recupero delle commissioni per CI, importo, touchpoint, singolo PSP e con timbro digitale su una richiesta
    Dato una richiesta di recupero commissioni "commissioni_ci_importo_touchpoint_timbro_digitale_singolo_psp"
    E il parametro di richiesta "maxOccurrences" è "10"
    Quando il client invia la richiesta di "Recupero commissioni" con il payload "commissioni_ci_importo_touchpoint_timbro_digitale_singolo_psp"
    Allora il sistema risponde con codice di stato 200
    E il corpo della risposta corrisponde al payload "commissioni_ci_importo_touchpoint_timbro_digitale_singolo_psp_response"
    
  @runnable
  @happy_path
  @gec_002_06
  Scenario: Recupero delle commissioni per CI, importo, touchpoint, singolo PSP e con timbro digitale
    Dato una richiesta di recupero commissioni "commissioni_ci_importo_touchpoint_timbro_digitale_psp"
    E il parametro di richiesta "maxOccurrences" è "10"
    Quando il client invia la richiesta di "Recupero commissioni" con il payload "commissioni_ci_importo_touchpoint_timbro_digitale_psp"
    Allora il sistema risponde con codice di stato 200
    E i valori del campo `onUs` delle opzioni bundle, dopo l'ordinamento previsto per l'API "V1", corrispondono ai seguenti:
      | onUs  |
      | false |
      | false |
    
  @runnable
  @happy_path
  @gec_002_07
  Scenario: Recupero delle commissioni oltre il limite
    Dato una richiesta di recupero commissioni "commissioni_oltre_limite"
    E il parametro di richiesta "maxOccurrences" è "10"
    Quando il client invia la richiesta di "Recupero commissioni" con il payload "commissioni_oltre_limite"
    Allora il sistema risponde con codice di stato 200
    E i valori del campo `onUs` delle opzioni bundle, dopo l'ordinamento previsto per l'API "V1", corrispondono ai seguenti:
      | onUs  |
      | true  |
      | true  |
      | false |
      | false |
      | false |
      | false |
      | false |
      | false |

  @runnable
  @happy_path
  @gec_002_08
  Scenario: Recupero delle commissioni con bin non esistente
    Dato una richiesta di recupero commissioni "commissioni_bin_non_esistente_2"
    E il parametro di richiesta "maxOccurrences" è "10"
    Quando il client invia la richiesta di "Recupero commissioni" con il payload "commissioni_bin_non_esistente_2"
    Allora il sistema risponde con codice di stato 200
    E la risposta non contiene opzioni bundle

  @runnable
  @happy_path
  @gec_002_09
  Scenario: Recupero delle commissioni con impostazione allCcp spenta
    Dato una richiesta di recupero commissioni "commissioni_ccp"
    E il parametro di richiesta "maxOccurrences" è "10"
    E l'impostazione allCcp è disabilitata
    Quando il client invia la richiesta di "Recupero commissioni" con il payload "commissioni_ccp"
    Allora il sistema risponde con codice di stato 200
    E nella risposta non è riportato il bundle delle Poste Italiane

  @runnable
  @happy_path
  @gec_002_10
  Scenario: Recupero delle commissioni con impostazione allCcp accesa
    Dato una richiesta di recupero commissioni "commissioni_ccp"
    E il parametro di richiesta "maxOccurrences" è "10"
    E l'impostazione allCcp è abilitata
    Quando il client invia la richiesta di "Recupero commissioni" con il payload "commissioni_ccp"
    Allora il sistema risponde con codice di stato 200
    E nella risposta è riportato il bundle delle Poste Italiane

  @runnable
  @happy_path
  @gec_002_11
  Scenario: Recupero delle commissioni per un pagamento AMEX
    Dato una richiesta di recupero commissioni "commissioni_amex"
    E il parametro di richiesta "maxOccurrences" è "10"
    Quando il client invia la richiesta di "Recupero commissioni" con il payload "commissioni_amex"
    Allora il sistema risponde con codice di stato 200
    E i valori del campo `onUs` delle opzioni bundle, dopo l'ordinamento previsto per l'API "V1", corrispondono ai seguenti:
      | onUs  |
      | true  |
