# Guida al porting dei test API: da Newman a Gherkin (Behave)

Questa guida descrive il processo step-by-step per trasformare test API scritti in formato Newman/Postman (file JSON) in scenari Gherkin per il framework Behave.  
Gli esempi sono tratti dalla suite `cart-tests` presente in `pagopa-checkout-tests/api-tests/cart-tests`.

---

## Indice

1. [Panoramica del processo](#1-panoramica-del-processo)
2. [Passo 1 — Individuazione dei file Newman](#2-passo-1--individuazione-dei-file-newman)
3. [Passo 2 — Individuazione delle configurazioni e variabili di ambiente](#3-passo-2--individuazione-delle-configurazioni-e-variabili-di-ambiente)
4. [Passo 3 — Analisi della struttura di un test Newman](#4-passo-3--analisi-della-struttura-di-un-test-newman)
5. [Passo 4 — Mappatura Newman → Gherkin](#5-passo-4--mappatura-newman--gherkin)
6. [Passo 5 — Struttura del file `.feature`](#6-passo-5--struttura-del-file-feature)
7. [Passo 6 — Esempi pratici completi](#7-passo-6--esempi-pratici-completi)
8. [Validazione e check finale](#8-validazione-e-check-finale)

---

## 1. Panoramica del processo

Il porting segue questa sequenza:

```
File JSON Newman  →  Variabili d'ambiente  →  Pre-request script  →  Request  →  Test assertions
       ↓                      ↓                       ↓                  ↓                ↓
  Feature name          Background /           Given (setup)          When           Then (verify)
                         .env file
```

Ogni **item** nella collezione Newman diventa uno **Scenario** nel file `.feature`.  
Le **variabili di ambiente** diventano chiavi in un file `.env` per ambiente.  
I **pre-request script** diventano step `Given` di setup.  
La **request** diventa uno step `When`.  
Le **assertions** (script di test) diventano step `Then`.

---

## 2. Passo 1 — Individuazione dei file Newman

### Struttura tipica di una collezione Newman

Una suite di test Newman è organizzata in una cartella con:

```
cart-tests/
├── cart-api-dev.tests.json       ← collezione per ambiente DEV (v1)
├── cart-api-dev-v2.tests.json    ← collezione per ambiente DEV (v2)
├── cart-api-uat.tests.json       ← collezione per ambiente UAT (v1)
└── cart-api-uat-v2.tests.json    ← collezione per ambiente UAT (v2)
```

> **Nota sul multi-ambiente**: le collezioni `dev` e `uat` spesso contengono gli stessi test logici, differenziati solo dall'host base. In Gherkin si usa un unico file `.feature` e si gestisce l'ambiente tramite file `.env`.

### File separati per versione API

Se esistono file `v1` e `v2`, valutare:
- Se i test delle due versioni differiscono per endpoint o payload → creare Feature o Scenario separati (es. `Scenario: Post cart OK` vs `Scenario: Post cart OK (v2)`).
- Se cambiano solo alcuni campi del body → usare `Scenario Outline` con una tabella `Examples`.

---

## 3. Passo 2 — Individuazione delle configurazioni e variabili di ambiente

### Nel file Newman

Le variabili di ambiente sono definite in un file JSON separato (`dev.envs.json`, `uat.envs.json`):

```json
// dev.envs.json (estratto)
{
  "name": "Checkout Tests DEV",
  "values": [
    { "key": "CHECKOUT_HOST",        "value": "https://api.dev.platform.pagopa.it", "enabled": true },
    { "key": "NOTICE_CODE_PREFIX",   "value": "3020",          "enabled": true },
    { "key": "VALID_FISCAL_CODE_PA", "value": "77777777777",   "enabled": true },
    { "key": "CART_ID",              "value": "",              "enabled": true },
    { "key": "AMOUNT",               "value": "12000",         "enabled": true }
  ]
}
```

Le variabili si usano nella request con la sintassi `{{NOME_VARIABILE}}`:

```
"url": "{{CHECKOUT_HOST}}/checkout/ec/v1/carts"
"body": { "noticeNumber": {{VALID_NOTICE_CODE}}, "fiscalCode": {{VALID_FISCAL_CODE_PA}} }
```

### In Gherkin / Behave

Le stesse variabili vengono memorizzate in file `.env` per ambiente all'interno di `config/api-test/`:

```
config/
└── api-test/
    ├── .env.dev    ← sostituisce dev.envs.json
    └── .env.uat    ← sostituisce uat.envs.json
```

**Contenuto di `.env.dev`** (estratto):

```ini
# Ambiente DEV — cart-tests
CHECKOUT_HOST=https://api.dev.platform.pagopa.it
NOTICE_CODE_PREFIX=3020
VALID_FISCAL_CODE_PA=77777777777
```

### Tabella di mappatura variabili

| Variabile Newman (`dev.envs.json`) | File `.env.dev` (Behave) | Note |
|---|---|---|
| `CHECKOUT_HOST` | `CHECKOUT_HOST` | URL base dell'API |
| `NOTICE_CODE_PREFIX` | `NOTICE_CODE_PREFIX` | Prefisso per generazione notice code casuale |
| `VALID_FISCAL_CODE_PA` | `VALID_FISCAL_CODE_PA` | Codice fiscale PA valido |
| `CART_ID` | stato di scenario (`context.cart_id`) | Valore dinamico, non in `.env` |
| `AMOUNT` | `AMOUNT` o costante nel test | Importo in centesimi |

> **Regola**: le variabili con valore fisso vanno nel file `.env`; quelle calcolate o estratte dalla risposta diventano attributi di `context` nello scenario.

---

## 4. Passo 3 — Analisi della struttura di un test Newman

### Anatomia di un item Newman

Ogni test nella collezione JSON è un oggetto con questa struttura:

```json
{
  "name": "Post cart OK",
  "event": [
    {
      "listen": "prerequest",
      "script": { "exec": [ "...codice JS..." ] }
    },
    {
      "listen": "test",
      "script": { "exec": [ "...asserzioni JS..." ] }
    }
  ],
  "request": {
    "method": "POST",
    "header": [],
    "body": { "mode": "raw", "raw": "{ ... JSON body ... }" },
    "url": { "raw": "https://api.dev.platform.pagopa.it/checkout/ec/v1/carts" }
  }
}
```

Le tre sezioni da analizzare:

| Sezione Newman | Contenuto | Corrisponde a |
|---|---|---|
| `prerequest` → `script.exec` | Setup dinamico (es. generazione dati casuali) | Step `Given` |
| `request` | Metodo HTTP, URL, headers, body | Step `When` |
| `test` → `script.exec` | Asserzioni sulla risposta | Step `Then` |

### Esempio reale — `Post cart OK`

**Pre-request script:**
```javascript
const noticeCodePrefix = pm.environment.get("NOTICE_CODE_PREFIX");
const min = Number(noticeCodePrefix.concat("10000000000000"));
const max = Number(noticeCodePrefix.concat("19999999999999"));
const randomNoticeCode = _.random(min, max);
pm.environment.set("VALID_NOTICE_CODE", randomNoticeCode);
```
→ *Genera un notice code casuale nel range del prefisso configurato.*

**Request:**
```
POST https://api.dev.platform.pagopa.it/checkout/ec/v1/carts
Body (JSON):
{
  "paymentNotices": [{
    "noticeNumber": {{VALID_NOTICE_CODE}},
    "fiscalCode": {{VALID_FISCAL_CODE_PA}},
    "amount": 12000,
    "companyName": "Nome EC",
    "description": "Oggetto del pagamento"
  }],
  "returnUrls": {
    "returnOkUrl":     "https://returnOkUrl",
    "returnCancelUrl": "https://returnCancelUrl",
    "returnErrorUrl":  "https://returnErrorUrl"
  },
  "emailNotice": "test@test.it",
  "idCart": "3de77d19-1655-4eaa-8bbb-14be203584d4",
  "allCCP": false
}
```

**Test assertion:**
```javascript
pm.test("Status code is 302 with one payment notice", () => {
  pm.expect(pm.response.code).to.eql(302);
  pm.expect(pm.response.to.have.header("Location"));
  pm.environment.set("CART_ID",
    pm.response.headers.get("Location")
      .substring(pm.response.headers.get("Location").lastIndexOf("/") + 1)
  );
});
```
→ *Verifica che lo status sia 302, che l'header `Location` sia presente, ed estrae il `CART_ID`.*

---

## 5. Passo 4 — Mappatura Newman → Gherkin

### Regole di trasformazione

| Elemento Newman | Regola di trasformazione | Step Gherkin risultante |
|---|---|---|
| Nome dell'item | Titolo dello scenario | `Scenario: <nome>` |
| Pre-request: lettura variabile di ambiente | Dato che una variabile è configurata | `Given a valid PA fiscal code configured in "VALID_FISCAL_CODE_PA"` |
| Pre-request: generazione dato casuale | Dato che un dato viene generato dinamicamente | `Given a valid random notice code generated from the prefix configured in "NOTICE_CODE_PREFIX"` |
| Request: metodo + URL | Azione sull'API | `When I send a POST to "/checkout/ec/v1/carts" with cart data and email "test@test.it"` |
| Request: body non valido | Azione con payload specifico | `When I send a POST to "/checkout/ec/v1/carts" with invalid body` |
| Test: `pm.response.code` | Verifica status code | `Then the response has status code 302` |
| Test: `pm.response.to.have.header(...)` | Verifica header presente | `And the response contains the header "location"` |
| Test: estrazione valore da header | Salvataggio valore per uso futuro | `And the CART_ID is extracted from the header "location"` |

### Gestione dei dati dinamici

Nel test Newman, `VALID_NOTICE_CODE` viene generato a runtime nel pre-request script. In Gherkin, questa logica viene espressa come uno step descrittivo:

```gherkin
# Newman (pre-request script):
# const randomNoticeCode = _.random(min, max);
# pm.environment.set("VALID_NOTICE_CODE", randomNoticeCode);

# Gherkin equivalente:
Given a valid random notice code generated from the prefix configured in "NOTICE_CODE_PREFIX"
```

Il dettaglio dell'algoritmo di generazione rimane nella parola `valid random` e nel riferimento alla variabile di configurazione.

### Gestione di `pm.environment.set` nelle asserzioni

Quando il test Newman imposta una variabile dopo aver verificato la risposta (es. salva il `CART_ID` dalla `Location`), in Gherkin si aggiunge uno step `And` separato:

```gherkin
# Newman:
# pm.environment.set("CART_ID", pm.response.headers.get("Location").substring(...));

# Gherkin:
And the CART_ID is extracted from the header "location"
```

---

## 6. Passo 5 — Struttura del file `.feature`

### Template base

```gherkin
# language: en
Feature: <Nome della Feature>
  As a <attore>
  I want to <obiettivo>
  In order to <beneficio>

  Background:
    Given that checkout host is configured through environment variable

  Scenario: <Nome scenario — corrisponde al nome dell'item Newman>
    Given <setup / precondizioni>
    When  <chiamata API>
    Then  <verifica status code>
    And   <verifiche aggiuntive>
```

**`Background`**: contiene i passi comuni a tutti gli scenari (es. caricamento della configurazione host). Equivale al setup globale della collezione Newman.

### Quando usare `Scenario Outline`

Se due o più item Newman differiscono solo per un parametro (es. `emailNotice` con case diverso), si usa `Scenario Outline`:

```gherkin
Scenario Outline: Post cart OK - Email address formatting
  Given a valid random notice code generated from the prefix configured in "NOTICE_CODE_PREFIX"
  And a valid PA fiscal code configured in "VALID_FISCAL_CODE_PA"
  When I send a POST to "/checkout/ec/v1/carts" with cart data and email "<email>"
  Then the response has status code 302
  And the response contains the header "location"
  And the CART_ID is extracted from the header "location"

  Examples:
    | email          |
    | test@test.it   |
    | TEST@test.IT   |
```

---

## 7. Passo 6 — Esempi pratici completi

### Esempio 1 — Test di successo (POST cart v1)

**Newman — `cart-api-dev.tests.json`, item `Post cart OK`:**

```json
{
  "name": "Post cart OK",
  "event": [
    {
      "listen": "prerequest",
      "script": {
        "exec": [
          "const noticeCodePrefix = pm.environment.get('NOTICE_CODE_PREFIX');",
          "const randomNoticeCode = _.random(...);",
          "pm.environment.set('VALID_NOTICE_CODE', randomNoticeCode);"
        ]
      }
    },
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status code is 302 with one payment notice', () => {",
          "  pm.expect(pm.response.code).to.eql(302);",
          "  pm.expect(pm.response.to.have.header('Location'));",
          "  pm.environment.set('CART_ID', ...);",
          "});"
        ]
      }
    }
  ],
  "request": {
    "method": "POST",
    "url": "https://api.dev.platform.pagopa.it/checkout/ec/v1/carts",
    "body": {
      "paymentNotices": [{ "noticeNumber": "{{VALID_NOTICE_CODE}}", ... }],
      "emailNotice": "test@test.it"
    }
  }
}
```

**Gherkin risultante:**

```gherkin
Scenario: Post cart OK - Valid cart creation with one payment notice
  Given a valid random notice code generated from the prefix configured in "NOTICE_CODE_PREFIX"
  And a valid PA fiscal code configured in "VALID_FISCAL_CODE_PA"
  When I send a POST to "/checkout/ec/v1/carts" with cart data and email "test@test.it"
  Then the response has status code 302
  And the response contains the header "location"
  And the CART_ID is extracted from the header "location"
```

---

### Esempio 2 — Test di errore (payload non valido)

**Newman — item `Post carts KO invalid request`:**

```json
{
  "name": "Post carts KO invalid request",
  "event": [{
    "listen": "test",
    "script": {
      "exec": [
        "pm.test('Status code is 400 with invalid request', () => {",
        "  pm.expect(pm.response.code).to.eql(400);",
        "});"
      ]
    }
  }],
  "request": {
    "method": "POST",
    "url": "https://api.dev.platform.pagopa.it/checkout/ec/v1/carts",
    "body": {
      "paymentNotices": [{ "noticeNumber": "302000100440009424", "fiscalCode": "1", ... }],
      "returnurls": { ... }
    }
  }
}
```

> **Nota**: il campo `returnurls` (minuscolo) è intenzionalmente errato nel payload originale Newman. È questo a causare il 400.

**Gherkin risultante:**

```gherkin
Scenario: Post cart KO - Invalid request (malformed body)
  When I send a POST to "/checkout/ec/v1/carts" with invalid body
  Then the response has status code 400
```

> Questo scenario non ha step `Given` perché non richiede setup preliminare: il test verifica solo che un body malformato venga rifiutato.

---

### Esempio 3 — Test di errore (validazione numerica)

**Newman — item `Post carts KO Multiple payment notices`:**

```json
{
  "name": "Post carts KO Multiple payment notices",
  "event": [{
    "listen": "test",
    "script": {
      "exec": [
        "pm.test('Status code is 400 with more than 5 payment notices', () => {",
        "  pm.expect(pm.response.code).to.eql(400);",
        "});"
      ]
    }
  }],
  "request": {
    "method": "POST",
    "body": { "paymentNotices": [ /* 6 elementi */ ] }
  }
}
```

**Gherkin risultante:**

```gherkin
Scenario: Post cart KO - Number of payment notices exceeds maximum allowed
  When I send a POST to "/checkout/ec/v1/carts" with 6 payment notices
  Then the response has status code 400
```

> Il numero `6` è estratto direttamente dal nome del test Newman (`more than 5`) e reso esplicito nello step `When` come parametro.

---

### Esempio 4 — Collezione v2 con campo aggiuntivo

**Newman — `cart-api-dev-v2.tests.json`, item `Post cart OK (v2)`:**

Rispetto a v1, la v2 aggiunge `returnWaitingUrl` nell'oggetto `returnUrls` e usa il path `/v2/carts`.

**Gherkin — scenario separato per v2:**

```gherkin
Scenario: Post cart OK (v2) - Valid cart creation with one payment notice
  Given a valid random notice code generated from the prefix configured in "NOTICE_CODE_PREFIX"
  And a valid PA fiscal code configured in "VALID_FISCAL_CODE_PA"
  When I send a POST to "/checkout/ec/v2/carts" with cart data and email "test@test.it"
  Then the response has status code 302
  And the response contains the header "location"
  And the CART_ID is extracted from the header "location"
```

**Oppure, con `Scenario Outline` per coprire entrambe le versioni:**

```gherkin
Scenario Outline: Post cart OK - <version> - Valid cart creation
  Given a valid random notice code generated from the prefix configured in "NOTICE_CODE_PREFIX"
  And a valid PA fiscal code configured in "VALID_FISCAL_CODE_PA"
  When I send a POST to "/checkout/ec/<path>/carts" with cart data and email "test@test.it"
  Then the response has status code 302
  And the response contains the header "location"

  Examples:
    | version | path |
    | v1      | v1   |
    | v2      | v2   |
```

---

### Esempio 5 — Test specifico v2: campo obbligatorio mancante

**Newman — item `Post cart KO - Missing returnWaitingUrl`:**

```json
{
  "name": "Post cart KO - Missing returnWaitingUrl",
  "event": [{
    "listen": "test",
    "script": {
      "exec": [
        "pm.test('Status code is 400 Bad Request', () => {",
        "  pm.expect(pm.response.code).to.eql(400);",
        "});"
      ]
    }
  }],
  "request": {
    "method": "POST",
    "url": "https://api.dev.platform.pagopa.it/checkout/ec/v2/carts",
    "body": {
      "returnUrls": {
        "returnOkUrl": "...",
        "returnCancelUrl": "...",
        "returnErrorUrl": "..."
        // returnWaitingUrl assente!
      }
    }
  }
}
```

**Gherkin risultante:**

```gherkin
Scenario: Post cart KO (v2) - Missing returnWaitingUrl
  Given a valid random notice code generated from the prefix configured in "NOTICE_CODE_PREFIX"
  And a valid PA fiscal code configured in "VALID_FISCAL_CODE_PA"
  When I send a POST to "/checkout/ec/v2/carts" with cart data missing "returnWaitingUrl"
  Then the response has status code 400
```

---

## 8. Validazione e check finale

Dopo aver scritto il file `.feature`, verificare i seguenti punti:

### Checklist di corrispondenza

| Elemento | Verificato? |
|---|---|
| Ogni item Newman ha uno Scenario corrispondente | ✓ |
| Le variabili in `dev.envs.json` con valore fisso sono in `.env.dev` | ✓ |
| Le variabili calcolate dinamicamente sono step `Given` | ✓ |
| I valori estratti dalla risposta sono step `And` separati | ✓ |
| Lo status code di ogni test Newman è nello step `Then` | ✓ |
| I test v1 e v2 sono differenziati nell'endpoint (`/v1/` vs `/v2/`) | ✓ |

### Verifica della leggibilità

Un buon file `.feature` deve essere leggibile da chi non conosce i dettagli tecnici. Ogni scenario deve rispondere alla domanda:

> *"Dato che... quando faccio... allora mi aspetto..."*

Se uno step contiene dettagli di implementazione (URL completo, codici hardcoded, logica condizionale), è un segnale che la granularità è troppo fine — astrai il concetto nel testo dello step.

### Confronto scenario Newman ↔ Feature Gherkin

| Nome item Newman | Scenario Gherkin |
|---|---|
| `Post cart OK` | `Post cart OK - Valid cart creation with one payment notice` |
| `Post cart OK mail in upper case` | `Post cart OK - Cart creation with uppercase email` |
| `Post carts KO invalid request` | `Post cart KO - Invalid request (malformed body)` |
| `Post carts KO Multiple payment notices` | `Post cart KO - Number of payment notices exceeds maximum allowed` |
| `Post cart OK (v2)` | `Post cart OK (v2) - Valid cart creation with one payment notice` |
| `Post cart KO - Missing returnWaitingUrl` | `Post cart KO (v2) - Missing returnWaitingUrl` |
