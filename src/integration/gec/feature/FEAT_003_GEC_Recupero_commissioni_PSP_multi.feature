#language: it
@integration
@gec_003_Recupero_commissioni_PSP_multi

Funzionalità: Recupero delle commissioni del PSP per più avvisi di pagamento

  Contesto:
    Dato che i sistemi sono operativi
    E la configurazione dei dati di test è caricata

  @runnable
  @happy_path
  @gec_003_01
  Scenario: Commissione superiore alla somma delle commissioni con PSP specificato
    Dato una richiesta di recupero commissioni "commissioni_v2_psp_superiore"
    Quando il client invia la richiesta di "Recupero commissioni V2" per il PSP "PPAYITR1XXX"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "idsCiBundle" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | idCiBundle      |
      | int-test-cart-1 |
    E per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC
    E i codici EC delle commissioni di ciascuna opzione bundle, in ordine alfabetico, corrispondono a:
      | codice_ec   |
      | 77777777777 |

  @runnable
  @happy_path
  @gec_003_02
  Scenario: Commissione inferiore alla somma delle commissioni con PSP specificato
    Dato una richiesta di recupero commissioni "commissioni_v2_psp_inferiore"
    Quando il client invia la richiesta di "Recupero commissioni V2" per il PSP "PPAYITR1XXX"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "idsCiBundle" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | idCiBundle      |
      | int-test-cart-2 |
    E per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC
    E i codici EC delle commissioni di ciascuna opzione bundle, in ordine alfabetico, corrispondono a:
      | codice_ec   |
      | 77777777777 |

  @runnable
  @happy_path
  @gec_003_03
  Scenario: Nessun bundle del creditore presente con PSP specificato
    Dato una richiesta di recupero commissioni "commissioni_v2_psp_senza_ci_bundle"
    Quando il client invia la richiesta di "Recupero commissioni V2" per il PSP "PPAYITR1XXX"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E le opzioni bundle non riportano valori per il campo "idsCiBundle"
    E le commissioni delle opzioni bundle non riportano codici EC

  @runnable
  @happy_path
  @gec_003_04
  Scenario: Bundle del creditore multipli con codice EC di un avviso non corrispondente e PSP specificato
    Dato una richiesta di recupero commissioni "commissioni_v2_psp_ec_non_corrispondente"
    Quando il client invia la richiesta di "Recupero commissioni V2" per il PSP "PPAYITR1XXX"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E le opzioni bundle non riportano valori per il campo "idsCiBundle"
    E le commissioni delle opzioni bundle non riportano codici EC

  @runnable
  @happy_path
  @gec_003_05
  Scenario: Bundle del creditore multipli con un solo avviso di pagamento e PSP specificato
    Dato una richiesta di recupero commissioni "commissioni_v2_psp_un_avviso"
    Quando il client invia la richiesta di "Recupero commissioni V2" per il PSP "PPAYITR1XXX"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "idsCiBundle" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | idCiBundle      |
      | int-test-cart-6 |
    E per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC
    E i codici EC delle commissioni di ciascuna opzione bundle, in ordine alfabetico, corrispondono a:
      | codice_ec   |
      | 88888888888 |

  @runnable
  @happy_path
  @gec_003_06
  Scenario: Bundle del creditore e avvisi di pagamento multipli con PSP specificato
    Dato una richiesta di recupero commissioni "commissioni_v2_psp_piu_avvisi"
    Quando il client invia la richiesta di "Recupero commissioni V2" per il PSP "PPAYITR1XXX"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "idsCiBundle" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | idCiBundle_1    | idCiBundle_2    |
      | int-test-cart-5 | int-test-cart-6 |
    E per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC
    E i codici EC delle commissioni di ciascuna opzione bundle, in ordine alfabetico, corrispondono a:
      | codice_ec_1 | codice_ec_2 |
      | 77777777777 | 88888888888 |

  @runnable
  @happy_path
  @gec_003_07
  Scenario: Bundle del creditore con più attributi e prodotto cartesiano con PSP specificato
    Dato una richiesta di recupero commissioni "commissioni_v2_psp_prodotto_cartesiano"
    Quando il client invia la richiesta di "Recupero commissioni V2" per il PSP "PPAYITR1XXX"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "idsCiBundle" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | idCiBundle_1    | idCiBundle_2    |
      | int-test-cart-7 | int-test-cart-8 |
    E per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC
    E i codici EC delle commissioni di ciascuna opzione bundle, in ordine alfabetico, corrispondono a:
      | codice_ec_1 | codice_ec_2 |
      | 77777777777 | 88888888888 |

  @runnable
  @happy_path
  @gec_003_08
  Scenario: Più bundle disponibili ma ne viene restituito uno solo con PSP specificato
    Dato una richiesta di recupero commissioni "commissioni_v2_psp_un_solo_bundle"
    Quando il client invia la richiesta di "Recupero commissioni V2" per il PSP "PPAYITR1XXX"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "onUs" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | onUs |
      | true |
    E i valori del campo "idsCiBundle" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | idCiBundle       |
      | int-test-cart-10 |
    E per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC
    E i codici EC delle commissioni di ciascuna opzione bundle, in ordine alfabetico, corrispondono a:
      | codice_ec   |
      | 77777777777 |
