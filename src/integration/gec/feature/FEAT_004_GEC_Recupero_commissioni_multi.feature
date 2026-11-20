#language: it
@integration
@gec_004_Recupero_commissioni_multi

Funzionalità: Recupero delle commissioni per più avvisi di pagamento

  Contesto:
    Dato che i sistemi sono operativi
    E la configurazione dei dati di test è caricata

  @positive
  @gec_004_01
  Scenario: Commissione superiore alla somma delle commissioni
    Dato una richiesta di recupero commissioni "commissioni_v2_superiore"
    Quando il client invia la richiesta di "Recupero commissioni V2"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "onUs" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | onUs  |
      | true  |
      | false |
    E i valori del campo "idsCiBundle" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | idCiBundle      |
      | int-test-cart-1 |
      | int-test-cart-9 |
    E per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC
    E i codici EC delle commissioni di ciascuna opzione bundle, in ordine alfabetico, corrispondono a:
      | codice_ec   |
      | 77777777777 |
      | 77777777777 |

  @positive
  @gec_004_02
  Scenario: Commissione superiore alla somma delle commissioni con un solo PSP richiesto
    Dato una richiesta di recupero commissioni "commissioni_v2_superiore_un_psp"
    Quando il client invia la richiesta di "Recupero commissioni V2"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "onUs" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | onUs |
      | true |
    E i valori del campo "idsCiBundle" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | idCiBundle      |
      | int-test-cart-1 |
    E per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC
    E i codici EC delle commissioni di ciascuna opzione bundle, in ordine alfabetico, corrispondono a:
      | codice_ec   |
      | 77777777777 |

  @positive
  @gec_004_03
  Scenario: Commissione inferiore alla somma delle commissioni
    Dato una richiesta di recupero commissioni "commissioni_v2_inferiore"
    Quando il client invia la richiesta di "Recupero commissioni V2"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "onUs" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | onUs  |
      | true  |
      | false |
    E i valori del campo "idsCiBundle" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | idCiBundle      |
      | int-test-cart-2 |
      | int-test-cart-9 |
    E per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC
    E i codici EC delle commissioni di ciascuna opzione bundle, in ordine alfabetico, corrispondono a:
      | codice_ec   |
      | 77777777777 |
      | 77777777777 |

  @positive
  @gec_004_04
  Scenario: Nessun bundle del creditore presente
    Dato una richiesta di recupero commissioni "commissioni_v2_senza_ci_bundle"
    Quando il client invia la richiesta di "Recupero commissioni V2"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "onUs" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | onUs  |
      | true  |
      | false |
    E le opzioni bundle non riportano valori per il campo "idsCiBundle"
    E le commissioni delle opzioni bundle non riportano codici EC

  @positive
  @gec_004_05
  Scenario: Bundle del creditore multipli con codice EC di un avviso non corrispondente
    Dato una richiesta di recupero commissioni "commissioni_v2_ec_non_corrispondente"
    Quando il client invia la richiesta di "Recupero commissioni V2"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "onUs" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | onUs  |
      | true  |
      | false |
    E le opzioni bundle non riportano valori per il campo "idsCiBundle"
    E le commissioni delle opzioni bundle non riportano codici EC

  @positive
  @gec_004_06
  Scenario: Bundle del creditore multipli con un solo avviso di pagamento
    Dato una richiesta di recupero commissioni "commissioni_v2_un_avviso"
    Quando il client invia la richiesta di "Recupero commissioni V2"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "onUs" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | onUs  |
      | true  |
      | false |
    E i valori del campo "idsCiBundle" delle prime opzioni bundle, nell'ordine restituito, corrispondono a:
      | idCiBundle      |
      | int-test-cart-6 |
    E per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC
    E i codici EC delle commissioni delle prime opzioni bundle, in ordine alfabetico, corrispondono a:
      | codice_ec   |
      | 88888888888 |

  @positive
  @gec_004_07
  Scenario: Bundle del creditore e avvisi di pagamento multipli
    Dato una richiesta di recupero commissioni "commissioni_v2_piu_avvisi"
    Quando il client invia la richiesta di "Recupero commissioni V2"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "onUs" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | onUs  |
      | true  |
      | false |
    E i valori del campo "idsCiBundle" delle prime opzioni bundle, nell'ordine restituito, corrispondono a:
      | idCiBundle_1    | idCiBundle_2    |
      | int-test-cart-5 | int-test-cart-6 |
    E per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC
    E i codici EC delle commissioni delle prime opzioni bundle, in ordine alfabetico, corrispondono a:
      | codice_ec_1 | codice_ec_2 |
      | 77777777777 | 88888888888 |

  @positive
  @gec_004_08
  Scenario: Bundle del creditore con più attributi e prodotto cartesiano restituito
    Dato una richiesta di recupero commissioni "commissioni_v2_prodotto_cartesiano"
    Quando il client invia la richiesta di "Recupero commissioni V2"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "onUs" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | onUs  |
      | true  |
      | false |
    E i valori del campo "idsCiBundle" delle prime opzioni bundle, nell'ordine restituito, corrispondono a:
      | idCiBundle_1    | idCiBundle_2    |
      | int-test-cart-7 | int-test-cart-8 |
    E per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC
    E i codici EC delle commissioni delle prime opzioni bundle, in ordine alfabetico, corrispondono a:
      | codice_ec_1 | codice_ec_2 |
      | 77777777777 | 88888888888 |

  @positive
  @gec_004_09
  Scenario: Più bundle disponibili ma ne viene restituito uno solo per PSP
    Dato una richiesta di recupero commissioni "commissioni_v2_un_bundle_per_psp"
    Quando il client invia la richiesta di "Recupero commissioni V2"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "onUs" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | onUs  |
      | true  |
      | false |
    E i valori del campo "idsCiBundle" delle opzioni bundle, nell'ordine restituito, corrispondono a:
      | idCiBundle       |
      | int-test-cart-10 |
      | int-test-cart-9  |
    E per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC
    E i codici EC delle commissioni di ciascuna opzione bundle, in ordine alfabetico, corrispondono a:
      | codice_ec   |
      | 77777777777 |
      | 77777777777 |
