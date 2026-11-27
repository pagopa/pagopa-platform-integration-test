#language: it
@integration
@gec_001_Recupera_commissioni_PSP

Funzionalità: Recupero delle commissioni del PSP

  Contesto:
    Dato che i sistemi sono operativi

  @runnable
  @happy_path
  @gec_001_01
  Scenario: Recupero delle commissioni per CI, importo, metodo, touchpoint e singolo PSP
    Dato una richiesta di recupero commissioni "commissioni_ci_importo_metodo_touchpoint"
    Quando il client invia la richiesta di "Recupero commissioni" per il PSP "PPAYITR1XXX" con il payload "commissioni_ci_importo_metodo_touchpoint" 
    Allora il sistema risponde con codice di stato 200
    E il corpo della risposta corrisponde al payload "commissioni_ci_importo_metodo_touchpoint_response"
  
  @runnable
  @happy_path
  @gec_001_02
  Scenario: Recupero delle commissioni per CI, importo, metodo e singolo PSP
    Dato una richiesta di recupero commissioni "commissioni_ci_importo_metodo"
    Quando il client invia la richiesta di "Recupero commissioni" per il PSP "PPAYITR1XXX" con il payload "commissioni_ci_importo_metodo" 
    Allora il sistema risponde con codice di stato 200
    E i valori del campo `onUs` delle opzioni bundle, dopo l'ordinamento previsto per l'API "V1", corrispondono ai seguenti:
      | onUs  |
      | false |
      | false |

  @runnable
  @happy_path
  @gec_001_03
  Scenario: Recupero delle commissioni per CI, importo e singolo PSP
    Dato una richiesta di recupero commissioni "commissioni_ci_importo"
    Quando il client invia la richiesta di "Recupero commissioni" per il PSP "BPPIITRRXXX" con il payload "commissioni_ci_importo" 
    Allora il sistema risponde con codice di stato 200
    E i valori del campo `onUs` delle opzioni bundle, dopo l'ordinamento previsto per l'API "V1", corrispondono ai seguenti:
      | onUs  |
      | true  |
      | false |
      | false |
      | false |
      | false |

  @runnable
  @happy_path
  @gec_001_04
  Scenario: Recupero delle commissioni per CI, importo, touchpoint e singolo PSP
    Dato una richiesta di recupero commissioni "commissioni_ci_importo_touchpoint"
    Quando il client invia la richiesta di "Recupero commissioni" per il PSP "BPPIITRRXXX" con il payload "commissioni_ci_importo_touchpoint" 
    Allora il sistema risponde con codice di stato 200
    E i valori del campo `onUs` delle opzioni bundle, dopo l'ordinamento previsto per l'API "V1", corrispondono ai seguenti:
      | onUs  |
      | true  |
      | false |
      | false |
      | false |
      | false |

  @runnable
  @happy_path
  @gec_001_05
  Scenario: Recupero delle commissioni per CI, importo, touchpoint, singolo PSP e con timbro digitale
    Dato una richiesta di recupero commissioni "commissioni_ci_importo_touchpoint_timbro_digitale"
    Quando il client invia la richiesta di "Recupero commissioni" per il PSP "BPPIITRRXXX" con il payload "commissioni_ci_importo_touchpoint_timbro_digitale"
    Allora il sistema risponde con codice di stato 200
    E il corpo della risposta corrisponde al payload "commissioni_ci_importo_touchpoint_timbro_digitale_response"

  @runnable
  @happy_path
  @gec_001_06
  Scenario: Recupero delle commissioni per CI, importo, touchpoint, singolo PSP oltre il limite di importo
    Dato una richiesta di recupero commissioni "commissioni_ci_importo_touchpoint_oltre_limite"
    Quando il client invia la richiesta di "Recupero commissioni" per il PSP "BPPIITRRXXX" con il payload "commissioni_ci_importo_touchpoint_oltre_limite"
    Allora il sistema risponde con codice di stato 200
    E i valori del campo `onUs` delle opzioni bundle, dopo l'ordinamento previsto per l'API "V1", corrispondono ai seguenti:
      | onUs  |
      | true  |
      | false |
      | false |
      | false |
      | false |
  
  @runnable
  @happy_path
  @gec_001_07
  Scenario: Recupero delle commissioni per PSP con bin non esistente
    Dato una richiesta di recupero commissioni "commissioni_bin_non_esistente"
    Quando il client invia la richiesta di "Recupero commissioni" per il PSP "BPPIITRRXXX" con il payload "commissioni_bin_non_esistente"
    Allora il sistema risponde con codice di stato 200
    E il corpo della risposta corrisponde al payload "commissioni_bin_non_esistente_response"

  @runnable
  @happy_path
  @gec_001_08
  Scenario: Recupero delle commissioni per CI, importo, touchpoint, singolo PSP per pagamenti AMEX
    Dato una richiesta di recupero commissioni "commissioni_ci_importo_touchpoint_amex"
    Quando il client invia la richiesta di "Recupero commissioni" per il PSP "UNCRITMM" con il payload "commissioni_ci_importo_touchpoint_amex"
    Allora il sistema risponde con codice di stato 200
    E il corpo della risposta corrisponde al payload "commissioni_ci_importo_touchpoint_amex_response"

  @runnable
  @happy_path
  @gec_001_09
  Scenario: Recupero delle commissioni per CI, importo, touchpoint, singolo PSP e con timbro digitale su entrambi i trasferimenti
    Dato una richiesta di recupero commissioni "commissioni_ci_importo_touchpoint_timbro_digitale_entrambi"
    Quando il client invia la richiesta di "Recupero commissioni" per il PSP "BPPIITRRXXX" con il payload "commissioni_ci_importo_touchpoint_timbro_digitale_entrambi"
    Allora il sistema risponde con codice di stato 200
    E i valori del campo `onUs` delle opzioni bundle, dopo l'ordinamento previsto per l'API "V1", corrispondono ai seguenti:
      | onUs  |
      | false |
      | false |
