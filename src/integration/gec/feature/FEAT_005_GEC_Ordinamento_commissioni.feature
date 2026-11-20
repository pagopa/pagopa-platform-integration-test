#language: it
@integration
@gec_005_Ordinamento_commissioni

Funzionalità: Ordinamento delle opzioni bundle nel recupero delle commissioni

  Contesto:
    Dato che i sistemi sono operativi
    E la configurazione dei dati di test è caricata

  @positive
  @gec_005_01
  Schema dello scenario: Ordinamento delle opzioni bundle per criterio e priorità onUsFirst
    Dato una richiesta di recupero commissioni "commissioni_v2_ordinamento"
    E il parametro di richiesta "orderBy" è "<criterio>"
    E il parametro di richiesta "onUsFirst" è "<on_us_first>"
    Quando il client invia la richiesta di "Recupero commissioni V2"
    Allora il sistema risponde con codice di stato 200
    E il sistema risponde con un solo bundle per ciascun PSP
    E i valori del campo "idBundle" delle prime opzioni bundle, nell'ordine restituito, corrispondono a:
      | id         |
      | <bundle_1> |
      | <bundle_2> |
      | <bundle_3> |

    Esempi:
      | criterio | on_us_first | bundle_1              | bundle_2              | bundle_3              |
      | fee      | false       | int-test-cart-cart-7  | int-test-cart-cart-11 | int-test-cart-cart-10 |
      | fee      | true        | int-test-cart-cart-11 | int-test-cart-cart-7  | int-test-cart-cart-10 |
      | pspname  | false       | int-test-cart-cart-10 | int-test-cart-cart-11 | int-test-cart-cart-7  |
      | pspname  | true        | int-test-cart-cart-11 | int-test-cart-cart-10 | int-test-cart-cart-7  |
