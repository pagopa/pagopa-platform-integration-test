# Analisi Tecnica — API Tests Checkout (Newman/Postman)

---

## 1. Tecnologia e Architettura

### 1.1 Stack

| Componente | Dettaglio |
|---|---|
| **Test authoring** | Postman (collezioni esportate in JSON) |
| **Runner** | [Newman](https://github.com/postmanlabs/newman) — CLI runner per Postman |
| **Linguaggio script** | JavaScript (eseguito dal runtime V8 di Postman/Newman) |
| **Assertion library** | Chai (integrata in `pm.expect`) |
| **Report** | JUnit XML (`--reporter-junit-export`) / CLI |
| **Schema collezione** | Postman Collection v2.1.0 (`https://schema.getpostman.com/json/collection/v2.1.0/collection.json`) |

### 1.2 Struttura delle collezioni Postman

Ogni file `.json` è una **Postman Collection**. La struttura di ogni item (request) è:

```
item
├── name          — nome del test
├── request       — definizione HTTP (method, url, headers, body)
├── event[]
│   ├── listen: "prerequest"  — script eseguito PRIMA della chiamata
│   └── listen: "test"        — script eseguito DOPO la risposta
└── response[]    — array vuoto (nessuna risposta salvata)
```

### 1.3 Scripting API (`pm.*`)

Gli script usano l'oggetto globale `pm` esposto da Postman/Newman:

| API | Utilizzo |
|---|---|
| `pm.environment.get("KEY")` | Legge una variabile di ambiente |
| `pm.environment.set("KEY", value)` | Scrive/aggiorna una variabile di ambiente |
| `pm.response.code` | HTTP status code della risposta |
| `pm.response.json()` | Body della risposta come oggetto JS |
| `pm.response.headers.get("Header")` | Legge un header della risposta |
| `pm.expect(...)` | Assertion (stile Chai) |
| `pm.test("nome", fn)` | Registra un test con nome e callback |
| `pm.sendRequest(opts, callback)` | Esegue una chiamata HTTP ausiliaria (usata nei pre-request) |

### 1.4 Pattern ricorrenti

**Pre-request: generazione notice code casuale**
```javascript
const noticeCodePrefix = pm.environment.get("NOTICE_CODE_PREFIX");
const min = Number(noticeCodePrefix.concat("10000000000000"));
const max = Number(noticeCodePrefix.concat("19999999999999"));
const randomNoticeCode = _.random(min, max);  // lodash in alcune collezioni
pm.environment.set("VALID_NOTICE_CODE", randomNoticeCode);
```

**Test script: verifica status code + estrazione ID per step successivi**
```javascript
pm.test("nome test", () => {
  pm.expect(pm.response.code).to.eql(302);
  pm.environment.set("CART_ID", pm.response.headers.get("Location").split("/").pop());
});
```

**Polling asincrono** (usato nelle collezioni ecommerce):
```javascript
async function executeGetTransactionPollingUntilStatus(wantedStatus) {
    const maxAttempts = 10;
    let counter = 0;
    let transactionStatus = null;
    while (counter < maxAttempts && transactionStatus !== wantedStatus) {
        await new Promise(r => setTimeout(r, 1000));
        // pm.sendRequest GET /transactions/:id → legge status
        counter++;
    }
    if (transactionStatus !== wantedStatus) throw new Error(...);
}
```

---

## 2. Configurazione e Variabili di Ambiente

### 2.1 File di ambiente

| File | Ambiente | Scope |
|---|---|---|
| `dev.envs.json` | DEV | Tutte le collezioni |
| `uat.envs.json` | UAT | Tutte le collezioni |
| `uat.payment-methods.blue.envs.json` | UAT Blue | Solo payment-methods microservice |
| `uat.payment-requests.blue.envs.json` | UAT Blue | Solo payment-requests microservice |
| `uat.transactions.blue.envs.json` | UAT Blue | Solo transactions microservice |

I **file \*.blue** contengono subset ridotti delle variabili, pensati per testare il canale blue/green di specifici microservizi. Non includono NPG credentials né tutte le variabili comuni.

### 2.2 Struttura di un file di ambiente

```json
{
  "id": "<uuid>",
  "name": "Checkout Tests DEV",
  "values": [
    { "key": "VARIABILE", "value": "valore", "enabled": true, "type": "default" }
  ],
  "_postman_variable_scope": "environment",
  "_postman_exported_at": "...",
  "_postman_exported_using": "Postman/11.6.2"
}
```

### 2.3 Variabili comuni (DEV e UAT)

| Variabile | DEV | UAT | Descrizione |
|---|---|---|---|
| `CHECKOUT_HOST` | `https://api.dev.platform.pagopa.it` | `https://api.uat.platform.pagopa.it` | Base URL delle API |
| `USE_BETA_BACKEND_HEADER` | `green` | `blue` | Valore header `deployment` per blue/green routing |
| `FAKE_RECAPTCHA_NOT_VALIDATED` | `123456789AAbbCC` | `123456789AAbbCC` | Token recaptcha di test (non validato lato server) |
| `VALID_NOTICE_CODE` | `10095545846194` | `302000100000009424` | Numero avviso valido (spesso sovrascritto in pre-request) |
| `VALID_FISCAL_CODE_PA` | `77777777777` | `77777777777` | Codice fiscale EC valido |
| `UNKNOWN_NOTICE_CODE` | `302170000000000000` | `002720356084529460` | Numero avviso inesistente |
| `UNKNOWN_FISCAL_CODE_PA` | `00000000001` | `00000000000` | CF EC inesistente |
| `NOTICE_CODE_PREFIX` | `3020` | `3020` | Prefisso per generazione casuale notice code |
| `AMOUNT` | `12000` (cent) | `12000` | Importo in centesimi |
| `PSP_ID` | `BCITITMM` | `BCITITMM` | Identificativo PSP |
| `FEE` | `100` | `100` | Commissione in centesimi |
| `EXPECTED_PAYMENT_REASON` | `TARI/TEFA 2021` | `TARI/TEFA 2021` | Causale attesa nella risposta |
| `DUE_DATE` | `2021-07-31` | `2021-07-31` | Data scadenza pagamento |
| `NPG_HOST` | `https://stg-ta.nexigroup.com` | `https://stg-ta.nexigroup.com` | Host NPG (staging Nexi) |
| `NPG_TEST_CARD_PAN` | `4349940199004549` | `4349940199004549` | PAN carta di test |
| `NPG_TEST_EXPIRATION_DATE` | `12/99` | `12/99` | Data scadenza carta test |
| `NPG_TEST_SECURITY_CODE` | `123` | `123` | CVV carta test |
| `NPG_TEST_CARDHOLDER_NAME` | `Test Test` | `Test Test` | Nome titolare carta test |
| `NPG_TEST_CARD_BRAND` | `VISA` | `VISA` | Brand carta test |

### 2.4 Variabili dinamiche (settate a runtime dagli script)

| Variabile | Settata da | Contenuto |
|---|---|---|
| `CART_ID` | Test script `cart-tests` | UUID estratto dall'header `Location` del 302 |
| `TRANSACTION_ID` | Test script `checkout-tests` / `eCommerce-cdc` | ID transazione eCommerce |
| `AUTH_TOKEN` | Test script | Bearer token per le chiamate successive |
| `PAYMENT_METHOD_ID` | Pre-request `checkout-tests` / `eCommerce-cdc` | UUID del metodo di pagamento (tipo CP) |
| `ORDER_ID` | Test script | Order ID NPG dalla risposta `POST sessions` |
| `NPG_CORRELATION_ID` | Test script | Correlation ID NPG (parsing URL iframe) |
| `NPG_SESSION_ID` | Test script | Session ID NPG (parsing URL iframe, URL-decoded) |
| `NPG_IFRAME_FIELD_URL` | Test script | URL del campo iframe NPG |
| `NPG_IFRAME_FIELD_ID` | Test script | ID del campo iframe NPG |
| `SESSION_TOKEN` | Test script `auth-service` | Token sessione utente autenticato |
| `STATE` / `NONCE` | Test script `auth-service` | Parametri OIDC estratti dalla redirect URL |
| `AUTH_CODE` | Test script `auth-service` | Authorization code OIDC (da HTML redirect) |
| `RANDOM_PAYMENT` | Pre-request `auth-service` | Stringa numerica casuale (12 cifre) |

### 2.5 Deployment Header (blue/green routing)

Quasi tutte le request includono l'header `deployment` con valori come `green` o `blue`. Questo permette di indirizzare il traffico verso la versione attiva del microservizio in ambienti con blue/green deployment. Variabili correlate:

- `DEPLOYMENT_PAYMENT_METHODS`
- `DEPLOYMENT_PAYMENT_REQUESTS`
- `DEPLOYMENT_TRANSACTION_SERVICE`
- `USE_BETA_BACKEND_HEADER`

---

## 3. Test — Sezione per Collezione

### 3.1 `cart-tests`

**File:** `cart-api-dev.tests.json`, `cart-api-uat.tests.json`, `cart-api-dev-v2.tests.json`, `cart-api-uat-v2.tests.json`  
**Scopo:** Verifica le API del servizio Carts (endpoint EC verso Checkout).

#### Endpoint testato

```
POST /checkout/ec/v1/carts   (v1)
POST /checkout/ec/v2/carts   (v2 — aggiunge returnWaitingUrl)
```

**Nota:** I file `dev`/`uat` hanno URL hardcoded; i file `v2` rispettano la stessa struttura ma con path `/v2/carts` e body con `returnWaitingUrl` aggiuntivo. La v2 UAT usa il file `uat.envs.json` in abbinamento; la v1 UAT usa un header `DEPLOYMENT` (senza suffisso microservice).

#### Test items e logica

| Nome request | Pre-request | Test Script | Atteso |
|---|---|---|---|
| `Post cart OK` | Genera `VALID_NOTICE_CODE` casuale da prefisso | Status 302, estrae `CART_ID` da `Location` | `302` + `Location` header |
| `Post cart OK mail in upper case` | Genera `VALID_NOTICE_CODE` casuale | Status 302 (verifica normalizzazione email) | `302` |
| `Post carts KO invalid request` | — | Status 400 (body malformato: `returnurls` minuscolo, CF = `"1"`) | `400` |
| `Post carts KO Multiple payment notices` | — | Status 400 (6 avvisi di pagamento, limite 5) | `400` |

#### Body request (v1)

```json
{
  "paymentNotices": [
    {
      "noticeNumber": {{VALID_NOTICE_CODE}},
      "fiscalCode": {{VALID_FISCAL_CODE_PA}},
      "amount": 12000,
      "companyName": "Nome EC",
      "description": "Oggetto del pagamento"
    }
  ],
  "returnUrls": {
    "returnOkUrl": "https://returnOkUrl",
    "returnCancelUrl": "https://returnCancelUrl",
    "returnErrorUrl": "https://returnErrorUrl"
  },
  "emailNotice": "test@test.it",
  "idCart": "3de77d19-1655-4eaa-8bbb-14be203584d4",
  "allCCP": false
}
```

---

### 3.2 `auth-service-tests`

**File:** `auth-service-api.tests.json`, `auth-service-api.oneidentity.tests.json`  
**Scopo:** Verifica il flusso OIDC del servizio di autenticazione Checkout (Auth Service).

#### Differenza tra i due file

| File | Scenario | Atteso finale |
|---|---|---|
| `auth-service-api.tests.json` | Flusso positivo: login → redirect → token valido | 200 su tutti gli step finali |
| `auth-service-api.oneidentity.tests.json` | Flusso negativo tramite OneIdentity: token non valido | 401 su AuthToken, PaymentRequests, Users |

#### Flusso (Happy Path)

```
1. GET /checkout/auth-service/v1/auth/login?recaptcha={{FAKE_RECAPTCHA_NOT_VALIDATED}}
   → 200, estrae STATE, NONCE, REDIRECT_URL dalla risposta JSON (urlRedirect)

2. GET {{REDIRECT_URL}}  (OneIdentity redirect)
   → Parsing HTML: estrae AUTH_CODE col regex /code=([^&]+)/

3. POST /checkout/auth-service/v1/auth/token
   Body: { "state": "{{STATE}}", "authCode": "{{AUTH_CODE}}" }
   → 200, estrae SESSION_TOKEN da authToken

4. GET /ecommerce/checkout/v3/auth/payment-requests/77777777777302016{{RANDOM_PAYMENT}}
   Auth: Bearer {{SESSION_TOKEN}}
   → (nessun assert esplicito, validazione presenza endpoint)

5. GET /checkout/auth-service/v1/auth/users
   Auth: Bearer {{SESSION_TOKEN}}
   → 200, verifica name == AUTH_USER_EXPECT_NAME, familyName == AUTH_USER_EXPECT_SURNAME

6. POST /checkout/auth-service/v1/auth/logout
   Auth: Bearer {{SESSION_TOKEN}}
   → 204
```

#### Flusso (Negativo — OneIdentity)

Stesse request, ma il token usati in AuthToken sono `"state": "some-invalid-state"` e `"authCode": "some-invalid-code"`. Tutti gli step autenticati si aspettano `401`.

---

### 3.3 `checkout-tests/npg`

**File:** `checkout-for-ecommerce-api.tests.json`  
**Scopo:** Testa il flusso completo di pagamento eCommerce con gateway NPG (Nexi Payment Gateway), inclusa la multi-lingua delle sessioni.

#### Flusso principale

```
1. DELETE /ecommerce/checkout/v1/transactions/{{TRANSACTION_ID}}   [cleanup]
   Pre-request: crea inline una transazione via pm.sendRequest → estrae TRANSACTION_ID e AUTH_TOKEN
   Test: 202

2. POST /ecommerce/checkout/v1/payment-methods/{{PAYMENT_METHOD_ID}}/sessions?recaptchaResponse=test
   Ripetuto per lingue: it, fr, de, en, sl
   Pre-request: recupera PAYMENT_METHOD_ID via POST /ecommerce/checkout/v2/payment-methods (filtra CP)
   Test: 200, verifica form con 4 campi (CARD_NUMBER, EXPIRATION_DATE, SECURITY_CODE, CARDHOLDER_NAME)
   Estrae: ORDER_ID, NPG_CORRELATION_ID, NPG_SESSION_ID, NPG_IFRAME_FIELD_ID (parsing URL iframe)

3. GET {{NPG_HOST}}/fe/build/field_settings/{{NPG_IFRAME_FIELD_ID}}?lang=ITA
   Auth: noauth — chiamata diretta a NPG staging per popolare cookies
   Headers: Correlation-Id, session (NPG)

4. POST /ecommerce/checkout/v2/transactions?recaptchaResponse=token
   Body: rptId = VALID_FISCAL_CODE_PA + VALID_NOTICE_CODE, orderId = ORDER_ID
   Test: 200, verifica struttura payments (rptId, reason, isAllCCP, transferList), estrae TRANSACTION_ID, AUTH_TOKEN, AMOUNT
   → Polling: executeGetTransactionPollingUntilStatus("ACTIVATED")

5. GET /ecommerce/checkout/v1/payment-methods/{{PAYMENT_METHOD_ID}}
   Test: 200, verifica id, name="CARDS", paymentTypeCode="CP", asset e ranges non vuoti

6. POST /ecommerce/checkout/v1/payment-methods/{{PAYMENT_METHOD_ID}}/fees
   Auth: Bearer {{AUTH_TOKEN}}
   Body: bin, touchpoint, paymentAmount, isAllCCP, transferList
   Test: 200, verifica paymentMethodStatus="ENABLED", belowThreshold=false, bundles non vuoti

7. GET /ecommerce/checkout/v1/payment-methods
   Test: 200, verifica struttura metodi (7 campi attesi), verifica brandAssets VISA/MC

8. POST {{NPG_HOST}}/fe/build/text/
   Body: fieldValues array (EXPIRATION_DATE, CARD_NUMBER, SECURITY_CODE, CARDHOLDER_NAME)
   Headers NPG: Correlation-Id, session → popola iframe con dati carta di test

9. GET /ecommerce/checkout/v1/payment-methods/{{PAYMENT_METHOD_ID}}/sessions/{{ORDER_ID}}
   Auth: Bearer {{AUTH_TOKEN}}
   Test: 200, verifica sessionId, bin (8 cifre PAN), lastFourDigits, expiringDate, brand

10. POST /ecommerce/checkout/v1/transactions/{{TRANSACTION_ID}}/auth-requests
    Auth: Bearer {{AUTH_TOKEN}}
    Body: amount, fee, paymentInstrumentId, pspId, isAllCCP, details.orderId
    Test: 200, verifica authorizationUrl e authorizationRequestId == ORDER_ID
    → Polling: executeGetTransactionPollingUntilStatus("AUTHORIZATION_REQUESTED")
```

#### Meccanismo di setup inline (pre-request con pm.sendRequest)

Molti test usano `pm.sendRequest` nel pre-request per costruire il contesto senza dover eseguire una request separata. Esempio in "Delete transaction": la transazione viene creata dentro il pre-request, e la request vera è il DELETE sulla transazione appena creata.

---

### 3.4 `eCommerce-cdc`

**File:** `eCommerce-cdc-service.postman_collection.json`  
**Scopo:** Test di integrazione del servizio CDC (Change Data Capture) di eCommerce. Verifica che le transizioni di stato della transazione si propaghino correttamente al CDC e siano visibili tramite le GET transactions.

#### Differenze rispetto a `checkout-tests/npg`

| Aspetto | checkout-tests/npg | eCommerce-cdc |
|---|---|---|
| Scopo | Verifica API eCommerce/Checkout | Verifica propagazione CDC dopo ogni step |
| Polling | Solo post-Create e post-AuthRequest | Dopo **ogni** step con cambio stato |
| Libreria random | `_` (Underscore/Lodash globale) | `require("lodash")` esplicito |
| Scenario | Un singolo scenario completo | Ripetuto in varianti (es. scenario con Delete, scenario senza Delete) |
| Lingue sessione | 5 varianti (it, fr, de, en, sl) + test specifici | Principalmente `it` |

#### Flusso (identico a checkout-tests/npg con polling CDC)

Il flusso degli step è strutturalmente identico a §3.3. La differenza è che dopo `DELETE /transactions` il polling verifica stato `CANCELED`, dopo `POST /transactions` verifica stato `ACTIVATED`, dopo `POST auth-requests` verifica stato `AUTHORIZATION_REQUESTED`. Questo polling implementa l'attesa della propagazione asincrona verso il CDC service.

#### Descrizione dalla collection

> "Those checks are implemented as GET transactions performed after each status changing operation performed on eCommerce with a polling strategy, allowing for async status update operation propagation to CDC service and then to eCommerce transaction view."

---

## 4. Installazione e Avvio

### 4.1 Prerequisiti

- **Node.js** (versione LTS consigliata)
- **Newman**: `npm install -g newman`
- **Reporter JUnit** (opzionale): `npm install -g newman-reporter-junit`

Verifica installazione:
```sh
newman --version
```

### 4.2 Struttura directory di lavoro

```
pagopa-checkout-tests/
├── api-tests/
│   ├── dev.envs.json
│   ├── uat.envs.json
│   ├── uat.payment-methods.blue.envs.json
│   ├── uat.payment-requests.blue.envs.json
│   ├── uat.transactions.blue.envs.json
│   ├── auth-service-tests/
│   ├── cart-tests/
│   ├── checkout-tests/npg/
│   └── eCommerce-cdc/
└── Results/           ← directory creata automaticamente da newman
```

### 4.3 Sintassi generale

```sh
newman run --ignore-redirects <COLLECTION_FILE> \
  --environment=<ENV_FILE> \
  --reporters cli,junit \
  --reporter-junit-export Results/<REPORT_NAME>.xml
```

- `--ignore-redirects`: impedisce a Newman di seguire automaticamente i redirect (essenziale per i test cart che si aspettano il `302`)
- `--reporters cli,junit`: output su console + file JUnit
- `--reporter-junit-export`: percorso file XML di output

### 4.4 Esempi per ogni test

**Cart Tests — DEV v1**
```sh
newman run --ignore-redirects ./api-tests/cart-tests/cart-api-dev.tests.json \
  --environment=./api-tests/dev.envs.json \
  --reporters cli,junit \
  --reporter-junit-export Results/cart-dev-v1.xml
```

**Cart Tests — UAT v2**
```sh
newman run --ignore-redirects ./api-tests/cart-tests/cart-api-uat-v2.tests.json \
  --environment=./api-tests/uat.envs.json \
  --reporters cli,junit \
  --reporter-junit-export Results/cart-uat-v2.xml
```

**Auth Service Tests — DEV (Happy Path)**
```sh
newman run --ignore-redirects ./api-tests/auth-service-tests/auth-service-api.tests.json \
  --environment=./api-tests/dev.envs.json \
  --reporters cli,junit \
  --reporter-junit-export Results/auth-dev.xml
```

**Auth Service Tests — DEV (OneIdentity Negative)**
```sh
newman run --ignore-redirects ./api-tests/auth-service-tests/auth-service-api.oneidentity.tests.json \
  --environment=./api-tests/dev.envs.json \
  --reporters cli,junit \
  --reporter-junit-export Results/auth-oneidentity-dev.xml
```

**Checkout NPG Tests — DEV**
```sh
newman run --ignore-redirects ./api-tests/checkout-tests/npg/checkout-for-ecommerce-api.tests.json \
  --environment=./api-tests/dev.envs.json \
  --reporters cli,junit \
  --reporter-junit-export Results/checkout-npg-dev.xml
```

**eCommerce CDC Tests — DEV**
```sh
newman run --ignore-redirects ./api-tests/eCommerce-cdc/eCommerce-cdc-service.postman_collection.json \
  --environment=./api-tests/dev.envs.json \
  --reporters cli,junit \
  --reporter-junit-export Results/ecommerce-cdc-dev.xml
```

### 4.5 Note operative

- I comandi vanno eseguiti dalla **root di `pagopa-checkout-tests/`**
- La cartella `Results/` deve esistere o essere creata prima dell'esecuzione (`mkdir Results`)
- Per i test `checkout-tests/npg` e `eCommerce-cdc` è necessario che l'ambiente target abbia dati di test validi (avvisi pagamento esistenti con il prefisso configurato in `NOTICE_CODE_PREFIX`)
- Il polling NPG (step `Get NPG field`) richiede connettività verso `stg-ta.nexigroup.com`
- I test auth-service richiedono che il provider OIDC (OneIdentity) sia raggiungibile e che l'utente di test sia configurato nell'ambiente target
