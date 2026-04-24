# Analisi Tecnica — API Tests BDD (Python/Behave)

---

## 1. Tecnologia e Architettura

### 1.1 Stack

| Componente | Dettaglio |
|---|---|
| **Linguaggio** | Python 3.x |
| **Framework BDD** | [Behave](https://behave.readthedocs.io/) 1.2.6 |
| **Sintassi scenari** | Gherkin (file `.feature`) |
| **Client HTTP** | `requests` 2.32.4 |
| **Configurazione** | `python-dotenv` — caricamento file `.env` per ambiente |
| **Report** | `allure-behave` 2.13.5 — integrazione Allure Framework |

### 1.2 Struttura del progetto

```
pagopa-platform-integration-test/
├── requirements.txt                          ← dipendenze Python
├── config/
│   └── api-test/
│       ├── .env.dev                          ← variabili DEV
│       └── .env.uat                          ← variabili UAT
└── src/
    ├── bdd/
    │   ├── cart/                             ← test modulo cart
    │   │   ├── environment.py
    │   │   ├── features/cart.feature
    │   │   └── steps/cart_steps.py
    │   ├── auth-service/                     ← test auth service
    │   │   ├── environment.py
    │   │   ├── features/auth_service.feature
    │   │   └── steps/auth_service_steps.py
    │   ├── checkout/                         ← test checkout NPG
    │   │   ├── environment.py
    │   │   ├── features/checkout_npg.feature
    │   │   └── steps/checkout_npg_steps.py
    │   └── ecommerce_cdc/                    ← test eCommerce CDC
    │       ├── environment.py
    │       ├── features/ecommerce_cdc.feature
    │       └── steps/ecommerce_cdc_steps.py
    └── utility/
        └── api_test/
            ├── api_test_environment.py       ← hook comuni (before_all, before_scenario)
            ├── cart/
            │   └── cart_helpers.py
            ├── auth_service/
            │   └── auth_service_helpers.py
            └── checkout/
                └── checkout_helpers.py       ← condiviso da checkout e ecommerce_cdc
```

### 1.3 Pattern architetturale

Ogni modulo BDD segue una separazione rigida delle responsabilità:

| Layer | File | Responsabilità |
|---|---|---|
| **Hook comuni** | `src/utility/api_test/api_test_environment.py` | Caricamento `.env`, reset `context.response` |
| **Hook modulo** | `src/bdd/<modulo>/environment.py` | Delega a hook comuni + reset stato specifico del modulo |
| **Helpers** | `src/utility/api_test/<modulo>/<modulo>_helpers.py` | Client HTTP, builder request body, utility dati |
| **Step definitions** | `src/bdd/<modulo>/steps/<modulo>_steps.py` | Mapping Gherkin → codice Python (importa helpers) |
| **Scenari** | `src/bdd/<modulo>/features/<modulo>.feature` | Specifiche Gherkin (Given/When/Then) |

### 1.4 Flusso di esecuzione Behave

```
behave src/bdd/<modulo> -D env=dev
    │
    ├─ environment.py → before_all()
    │      └─ api_test_environment.before_all()
    │             └─ Carica config/api-test/.env.dev via python-dotenv
    │
    ├─ environment.py → before_scenario()
    │      ├─ api_test_environment.before_scenario() → reset context.response
    │      └─ Reset variabili di stato del modulo (es. notice_code, transaction_id)
    │
    ├─ Per ogni Scenario:
    │   ├─ Given → setup contesto (resolve env vars, genera dati casuali)
    │   ├─ When  → esecuzione chiamata HTTP via helpers
    │   └─ Then  → asserzioni su status code, body, headers; propagazione stato
    │
    └─ Output: reports/allure-results/<modulo>-<env>/
```

---

## 2. Configurazione Comune e Variabili di Ambiente

### 2.1 File di configurazione

| File | Ambiente | Percorso |
|---|---|---|
| `.env.dev` | DEV | `config/api-test/.env.dev` |
| `.env.uat` | UAT | `config/api-test/.env.uat` |

Il file viene selezionato a runtime tramite il parametro `-D env=<dev|uat>` passato a `behave`.  
Il caricamento avviene in `api_test_environment.before_all()` tramite `load_dotenv(env_file, override=True)`.

Il percorso del file `.env` è risolto dinamicamente risalendo 4 livelli dal file `api_test_environment.py` fino alla root del repository.

### 2.2 Variabili di ambiente

**Comuni a tutti i moduli:**

| Variabile | DEV | UAT | Descrizione |
|---|---|---|---|
| `CHECKOUT_HOST` | `https://api.dev.platform.pagopa.it` | `https://api.uat.platform.pagopa.it` | Base URL API |
| `NOTICE_CODE_PREFIX` | `3020` | `3020` | Prefisso per generazione notice code casuale |
| `VALID_FISCAL_CODE_PA` | `77777777777` | `77777777777` | Codice fiscale EC valido per i test |

**Auth service:**

| Variabile | Descrizione |
|---|---|
| `FAKE_RECAPTCHA_NOT_VALIDATED` | Token reCAPTCHA di test (non validato lato server) |
| `AUTH_USER_EXPECT_NAME` | Nome atteso nel profilo utente autenticato |
| `AUTH_USER_EXPECT_SURNAME` | Cognome atteso nel profilo utente autenticato |

**Checkout / eCommerce CDC:**

| Variabile | Descrizione |
|---|---|
| `UNKNOWN_NOTICE_CODE` | Numero avviso inesistente (test negativi) |
| `UNKNOWN_FISCAL_CODE_PA` | CF EC inesistente (test negativi) |
| `UNKNOWN_STAZIONE_NOTICE_CODE` | Notice code con stazione sconosciuta |
| `UNKNOWN_STAZIONE_FISCAL_CODE_PA` | CF EC con stazione sconosciuta |
| `EXPECTED_PAYMENT_REASON` | Causale attesa nella risposta payment verify |
| `DUE_DATE` | Data scadenza attesa nella risposta |
| `AMOUNT` | Importo in centesimi (`12000`) |
| `PSP_ID` | Identificativo PSP (`BCITITMM`) |
| `FEE` | Commissione in centesimi (`100`) |
| `NPG_HOST` | Host NPG staging (`https://stg-ta.nexigroup.com`) |
| `NPG_TEST_CARD_PAN` | PAN carta di test Nexi |
| `NPG_TEST_EXPIRATION_DATE` | Data scadenza carta test |
| `NPG_TEST_SECURITY_CODE` | CVV carta test |
| `NPG_TEST_CARDHOLDER_NAME` | Nome titolare carta test |
| `NPG_TEST_CARD_BRAND` | Brand carta (`VISA`) |

**Deployment / blue-green routing:**

| Variabile | DEV | UAT | Descrizione |
|---|---|---|---|
| `USE_BETA_BACKEND_HEADER` | `green` | `blue` | Header `deployment` globale |
| `DEPLOYMENT` | `green` | `green` | Routing generico |
| `DEPLOYMENT_PAYMENT_METHODS` | `green` | `green` | Routing microservizio payment-methods |
| `DEPLOYMENT_PAYMENT_REQUESTS` | `green` | `green` | Routing microservizio payment-requests |
| `DEPLOYMENT_TRANSACTION_SERVICE` | `green` | `green` | Routing microservizio transaction-service |

**Lingue per sessioni NPG:**

| Variabile | Valore |
|---|---|
| `OPERATION_LANGUAGE_IT` | `it` |
| `OPERATION_LANGUAGE_FR` | `fr` |
| `OPERATION_LANGUAGE_DE` | `de` |
| `OPERATION_LANGUAGE_EN` | `en` |
| `OPERATION_LANGUAGE_SL` | `sl` |

### 2.3 Routing blue/green

Il `checkout_helpers.py` espone due funzioni per la gestione del routing:

- `get_deployment_header()` — legge `USE_BETA_BACKEND_HEADER`, restituisce `{"deployment": "<valore>"}` se presente.
- `get_specific_deployment_header(env_key)` — legge la variabile specificata, con fallback su `USE_BETA_BACKEND_HEADER`.

Ogni chiamata HTTP verso endpoint Checkout include l'header `deployment` corrispondente al microservizio target (es. `DEPLOYMENT_PAYMENT_METHODS` per `/payment-methods/`). Questo permette di indirizzare il traffico alla versione blue o green in ambienti con deployment parallelo.

### 2.4 Variabili di stato runtime (contesto Behave)

Queste variabili non sono file `.env` ma vengono propagate tra gli step tramite `context.<attr>`:

| Attributo context | Tipo | Moduli | Descrizione |
|---|---|---|---|
| `context.response` | `requests.Response` | tutti | Risposta HTTP dell'ultimo `When` |
| `context.notice_code` | `str` | cart, checkout, cdc | Notice code generato casualmente |
| `context.fiscal_code` | `str` | cart | Codice fiscale letto dall'env |
| `context.cart_id` | `str` | cart | CART_ID estratto dall'header `Location` |
| `context.payment_method_id` | `str` | checkout, cdc | UUID metodo di pagamento CP |
| `context.order_id` | `str` | checkout, cdc | Order ID NPG dalla risposta `sessions` |
| `context.correlation_id` | `str` | checkout, cdc | Correlation ID dalla risposta `sessions` |
| `context.npg_correlation_id` | `str` | checkout, cdc | Correlation ID estratto dall'URL iframe NPG |
| `context.npg_session_id` | `str` | checkout, cdc | Session ID estratto dall'URL iframe NPG |
| `context.npg_field_id` | `str` | checkout, cdc | Field ID estratto dall'URL iframe NPG |
| `context.transaction_id` | `str` | checkout, cdc | ID transazione eCommerce |
| `context.auth_token` | `str` | checkout, cdc | Bearer token per le chiamate autenticate |
| `context.amount` | `int` | checkout, cdc | Somma degli amount nei payments |
| `context.session_token` | `str` | auth-service | Token sessione utente autenticato |
| `context.auth_code` | `str` | auth-service | Authorization code OIDC |
| `context.state` / `context.nonce` | `str` | auth-service | Parametri OIDC estratti dalla redirect URL |

---

## 3. Moduli di Test

### 3.1 `cart`

**Feature:** [`src/bdd/cart/features/cart.feature`](src/bdd/cart/features/cart.feature)  
**Steps:** [`src/bdd/cart/steps/cart_steps.py`](src/bdd/cart/steps/cart_steps.py)  
**Helpers:** [`src/utility/api_test/cart/cart_helpers.py`](src/utility/api_test/cart/cart_helpers.py)

**Endpoint testato:**
```
POST /checkout/ec/v1/carts
```

**Stato context resettato in `before_scenario`:** `notice_code`, `fiscal_code`, `cart_id`

#### Scenari

| Tag / Scenario | Input | Atteso |
|---|---|---|
| `Post cart OK` (email valida) | Body con notice code casuale, CF, email lowercase | `302` + header `Location` con CART_ID |
| `Post cart OK` (email uppercase) | Come sopra, email mista `TEST@test.IT` | `302` — verifica normalizzazione email |
| `Post cart KO` (body malformato) | Body con CF `"1"`, chiave `returnurls` lowercase | `400` |
| `Post cart KO` (6 avvisi) | 6 `paymentNotices` (limite = 5) | `400` |

#### Preparazione input

Il notice code viene generato casualmente da `generate_notice_code()` a partire da `NOTICE_CODE_PREFIX`:
```python
min_val = int(prefix + "10000000000000")
max_val = int(prefix + "19999999999999")
return str(random.randint(min_val, max_val))
```

Il body valido è costruito da `build_cart_body(notice_code, fiscal_code, email)`, che include `paymentNotices`, `returnUrls`, `emailNotice`, `idCart` (fisso), `allCCP: False`.

Il body invalido `INVALID_CART_BODY` è una costante con `fiscalCode="1"` e `returnurls` (lowercase) — pattern di test negativo.

#### Verifica risposta

- Status code verificato con `assert actual == expected`.
- Header `location` verificato con ricerca case-insensitive sulle chiavi.
- CART_ID estratto dalla parte finale dell'URL in `Location`: `header_value[header_value.rfind("/") + 1:]`.

Il client HTTP usa `requests.post(..., allow_redirects=False)` per catturare il `302` senza seguire la redirect.

---

### 3.2 `auth-service`

**Feature:** [`src/bdd/auth-service/features/auth_service.feature`](src/bdd/auth-service/features/auth_service.feature)  
**Steps:** [`src/bdd/auth-service/steps/auth_service_steps.py`](src/bdd/auth-service/steps/auth_service_steps.py)  
**Helpers:** [`src/utility/api_test/auth_service/auth_service_helpers.py`](src/utility/api_test/auth_service/auth_service_helpers.py)

**Stato context resettato in `before_scenario`:** `login_payload`, `redirect_url`, `auth_code`, `state`, `nonce`, `session_token`, `user_profile`

#### Scenari

**Scenario positivo — flusso OIDC completo:**

```
Given   host + env vars configurati
When    GET /checkout/auth-service/v1/auth/login?recaptcha=<token>
Then    200 + urlRedirect nel body
When    GET <urlRedirect>  (OneIdentity)
Then    200 + estrazione auth_code dall'HTML (regex: code=([^&"']+))
When    POST /checkout/auth-service/v1/auth/token {state, authCode}
Then    200 + session_token nel body
When    GET /checkout/auth-service/v1/auth/users  [Bearer session_token]
Then    200 + name e familyName corrispondono alle env vars
When    POST /checkout/auth-service/v1/auth/logout [Bearer session_token]
Then    204
```

**Scenario negativo — credenziali invalide:**

```
When    POST /checkout/auth-service/v1/auth/token {state: "invalid", authCode: "invalid"}
Then    401
When    GET /ecommerce/checkout/v3/auth/payment-requests/... [Bearer "invalid-session-token"]
Then    401
When    GET /checkout/auth-service/v1/auth/users [Bearer "invalid-session-token"]
Then    401
```

#### Dettagli implementativi

- `parse_login_redirect_payload()` — valida la redirect URL OIDC: verifica `response_type=CODE`, `scope=openid`, presenza di `state`, `nonce`, `client_id`, `redirect_uri`.
- `extract_auth_code_from_html()` — parsing regex `re.search(r"code=([^&\"']+)", html)`.
- L'header `deployment` è aggiunto automaticamente da `get_deployment_headers()` in tutte le chiamate.
- `build_payment_requests_endpoint()` genera un suffix numerico casuale a 12 cifre per rendere ogni chiamata unica.

---

### 3.3 `checkout` (NPG)

**Feature:** [`src/bdd/checkout/features/checkout_npg.feature`](src/bdd/checkout/features/checkout_npg.feature)  
**Steps:** [`src/bdd/checkout/steps/checkout_npg_steps.py`](src/bdd/checkout/steps/checkout_npg_steps.py)  
**Helpers:** [`src/utility/api_test/checkout/checkout_helpers.py`](src/utility/api_test/checkout/checkout_helpers.py)

**Stato context resettato in `before_scenario`:** `payment_method_id`, `notice_code`, `order_id`, `correlation_id`, `npg_correlation_id`, `npg_session_id`, `npg_field_id`, `transaction_id`, `auth_token`, `amount`

#### Scenari per area funzionale

**Payment Verification (`@payment-verify`):**
- `Successful payment verification` — `GET /payment-requests/{rptId}` → `200` + struttura payments
- `404 unknown PA domain` — CF inesistente → `404` + `faultCodeDetail: PPT_DOMINIO_SCONOSCIUTO`
- `404 unknown station` — stazione sconosciuta → `404` + `PPT_STAZIONE_INT_PA_SCONOSCIUTA`

**Payment Methods (`@payment-methods`):**
- `GET /payment-methods` (v1) → `200` + campi attesi + brand assets VISA/MC
- `POST /payment-methods` (v2) → `200` + struttura metodi
- `GET /payment-methods/{id}` → `200` + `name=CARDS`, `paymentTypeCode=CP`
- Fee computation → `200` + `paymentMethodStatus=ENABLED`, bundles non vuoti

**NPG Session Creation (`@session`) — Scenario Outline:**

Eseguito per 5 lingue (`it`, `fr`, `de`, `en`, `sl`):
```
Given   credit card payment method id risolto
When    POST /payment-methods/{id}/sessions?recaptchaResponse=test [lang header]
Then    200 + form con 4 campi (CARD_NUMBER, EXPIRATION_DATE, SECURITY_CODE, CARDHOLDER_NAME)
```

**Transactions (`@transaction`):**
- `POST /transactions senza orderId` → `400`
- `POST /transactions con email mista` → `200` + stato `ACTIVATED`
- `POST /transactions standard + cached verify` → `200` + payment verify ancora valido

**Card Data (`@card`):**
- Flusso completo: session → fill NPG fields → `GET sessions/{orderId}` → `200` + dati carta corrispondenti
- Test negativi: wrong `orderId` → `401`; wrong `transactionId` → `401`; senza token → `401`

#### Dettagli implementativi chiave

**Risoluzione payment method ID:**
```python
def resolve_credit_card_payment_method_id() -> str:
    # POST /payment-methods v2, filtra paymentTypeCode == "CP"
    methods = response.json().get("paymentMethods", [])
    cp_methods = [m for m in methods if m.get("paymentTypeCode") == "CP"]
    return cp_methods[0]["id"]
```

**Estrazione parametri NPG dall'URL iframe:**

La risposta di `POST /sessions` contiene un `form[0].src` con URL NPG da cui si estraggono:
- `correlationid` — Correlation ID NPG
- `sessionid` — Session ID NPG (URL-decoded)
- `id` — Field ID NPG

```python
def _extract_npg_params_from_url(field_url: str) -> dict[str, str]:
    parsed = urlparse(field_url)
    query_params = parse_qs(parsed.query)
    # con decodifica manuale %2F, %2B, %3D
```

**Compilazione campi carta NPG:**

```python
def fill_npg_card_fields(npg_correlation_id, npg_session_id) -> Response:
    # POST {NPG_HOST}/fe/build/text/
    # Headers: Correlation-Id, session, Idempotency-Key (uuid4)
    # Body: fieldValues con EXPIRATION_DATE, CARD_NUMBER, SECURITY_CODE, CARDHOLDER_NAME
```

**Polling transazione:**
```python
def poll_transaction_until_status(transaction_id, auth_token, wanted_status,
                                   max_attempts=10, interval_sec=1.0) -> str:
    # GET /ecommerce/checkout/v2/transactions/{id} ogni secondo
    # Solleva AssertionError se non raggiunge lo stato entro max_attempts
```

**Flusso completo autorizzazione** (step composito `@given("the full NPG authorization flow is executed")`):
1. Risolve payment method ID
2. Crea sessione NPG
3. Genera notice code casuale
4. Crea transazione
5. Compila campi carta NPG
6. `POST /transactions/{id}/auth-requests` con PSP, fee, orderId
7. Polling fino a `AUTHORIZATION_REQUESTED`

**Deployment per microservizio:**

| Endpoint | Header `deployment` da |
|---|---|
| `/payment-methods` (v1) | `DEPLOYMENT_PAYMENT_METHODS` |
| `/payment-methods` (v2) | `DEPLOYMENT` |
| `/payment-requests/` | `DEPLOYMENT_PAYMENT_REQUESTS` |
| `/sessions/` | `DEPLOYMENT_TRANSACTION_SERVICE` |
| `/transactions` | `DEPLOYMENT_TRANSACTION_SERVICE` |

---

### 3.4 `ecommerce_cdc`

**Feature:** [`src/bdd/ecommerce_cdc/features/ecommerce_cdc.feature`](src/bdd/ecommerce_cdc/features/ecommerce_cdc.feature)  
**Steps:** [`src/bdd/ecommerce_cdc/steps/ecommerce_cdc_steps.py`](src/bdd/ecommerce_cdc/steps/ecommerce_cdc_steps.py)  
**Helpers:** (condivisi con checkout) [`src/utility/api_test/checkout/checkout_helpers.py`](src/utility/api_test/checkout/checkout_helpers.py)

**Note:** Il modulo CDC riusa interamente `checkout_helpers.py` per le chiamate HTTP. La differenza rispetto a `checkout` è nella logica degli scenari: ogni step mutante è seguito da un polling che verifica la propagazione dello stato nel pipeline CDC.

**Stato context resettato in `before_scenario`:** identico a checkout (`payment_method_id`, `notice_code`, `order_id`, `npg_*`, `transaction_id`, `auth_token`, `amount`) + `field_url`.

#### Scenari

| Tag / Scenario | Flusso | Status finale atteso |
|---|---|---|
| `@cancel` — Transazione annullata | Crea tx → `DELETE /transactions/{id}` | `202` → polling `CANCELED` |
| `@session` — Sessione NPG | `POST /sessions` | `200` + 4 form fields + `CARDS` + `orderId` |
| `@activated` — Creazione transazione | Crea sessione → crea tx | `200` + `ACTIVATED` → polling `ACTIVATED` |
| `@payment-methods` — Dettaglio metodo | `GET /payment-methods/{id}` | `200` + `CARDS`/`CP` + asset/ranges |
| `@fees` — Calcolo commissioni | Crea sessione+tx → `POST /fees` | `200` + `ENABLED` + bundles |
| `@payment-methods` — Brand assets v1 | `GET /payment-methods` v1 | `200` + VISA/MC brand assets |
| `@authorization @e2e` — Flusso completo | Sessione → cookies NPG → tx → fill card → `POST /auth-requests` | `200` + `authorizationUrl` + `AUTHORIZATION_REQUESTED` |

#### Dettagli implementativi chiave

**Pattern CDC — polling post-mutazione:**

Ogni operazione che modifica lo stato della transazione (`CREATE`, `DELETE`, `POST /auth-requests`) è seguita da un passo `Then the transaction status reaches "<STATUS>" via polling`.  
Il polling usa `poll_transaction_until_status()` (max 10 tentativi, 1 sec intervallo) su `GET /v2/transactions/{id}`.

**Scenario e2e completo (`@authorization`):**
```
Given   CDC credit card payment method id → risolto
And     CDC NPG session → POST /sessions → salva order_id, npg_*
And     NPG cookies → GET {NPG_HOST}/fe/build/field_settings/{field_id}
And     random CDC notice code → generato
And     CDC transaction → POST /transactions → salva transaction_id, auth_token
And     polling ACTIVATED
And     card data → POST {NPG_HOST}/fe/build/text/ con dati carta di test
When    POST /transactions/{id}/auth-requests → richiesta autorizzazione
Then    200 + authorizationUrl valido + requestId == orderId
And     polling AUTHORIZATION_REQUESTED
```

**Helpers interni step CDC:**

```python
def _save_session_data(context, session_data: dict) -> None:
    context.order_id = session_data["order_id"]
    context.npg_correlation_id = session_data["npg_correlation_id"]
    context.npg_session_id = session_data["npg_session_id"]
    context.npg_field_id = session_data["npg_field_id"]
    # + field_url (usato in CDC per populate_npg_cookies)

def _save_transaction_data(context, body: dict) -> None:
    context.transaction_id = body["transactionId"]
    context.auth_token = body["authToken"]
    context.amount = sum(p["amount"] for p in body.get("payments", []))
```

---

## 4. Installazione ed Esecuzione

### 4.1 Prerequisiti

- Python 3.10+
- Java (richiesto da Allure CLI)
- [Allure CLI](https://allurereport.org/docs/install/) installato e disponibile nel PATH

### 4.2 Installazione dipendenze Python

```bash
cd pagopa-platform-integration-test
pip install -r requirements.txt
```

Dipendenze chiave installate:

| Package | Versione | Scopo |
|---|---|---|
| `behave` | 1.2.6 | Runner BDD |
| `allure-behave` | 2.13.5 | Formatter Allure per Behave |
| `requests` | 2.32.4 | Client HTTP |
| `python-dotenv` | ≥1.0.0 | Lettura file `.env` |

### 4.3 Configurazione ambiente

Copiare e compilare il file `.env` per l'ambiente target:

```bash
# Esempio — DEV (i valori di default per test sono già presenti)
# config/api-test/.env.dev è già incluso nel repository con valori di esempio
```

I valori sensibili (credenziali reali, token) devono essere inseriti localmente senza committare.

### 4.4 Esecuzione test — solo output terminale

```bash
# Da pagopa-platform-integration-test/
behave src/bdd/cart -D env=dev -f progress
behave src/bdd/auth-service -D env=dev -f progress
behave src/bdd/checkout -D env=dev -f progress
behave src/bdd/ecommerce_cdc -D env=dev -f progress
```

Parametro `-D env=<dev|uat>` seleziona il file `.env` corrispondente (default: `dev`).

### 4.5 Esecuzione test — con report Allure

**Passo 1 — Preparare la directory e produrre i risultati:**

```powershell
# Da pagopa-platform-integration-test/
# Su Windows con allure-behave 2.x la directory deve esistere e essere vuota

Remove-Item -Recurse -Force -ErrorAction SilentlyContinue reports\allure-results\cart-dev
New-Item reports\allure-results\cart-dev -ItemType Directory -Force | Out-Null

behave src/bdd/cart `
    -D env=dev `
    -f allure_behave.formatter:AllureFormatter -o reports/allure-results/cart-dev `
    -f progress
```

> **Ordine dei formatter critico:** `-o` si associa al **primo** `-f`. `AllureFormatter` deve
> precedere `-f progress`, altrimenti `progress` riceve il path della directory e genera
> un `PermissionError`.

**Passo 2 — Visualizzare il report:**

```powershell
allure --version   # verifica versione installata

# Allure 2.x
allure serve reports/allure-results/cart-dev --port 5300

# Allure 3.x
allure open reports/allure-results/cart-dev --port 5300
```

### 4.6 Esempi completi per ogni modulo

**cart — DEV:**
```powershell
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue reports\allure-results\cart-dev
New-Item reports\allure-results\cart-dev -ItemType Directory -Force | Out-Null
behave src/bdd/cart -D env=dev -f allure_behave.formatter:AllureFormatter -o reports/allure-results/cart-dev -f progress
allure serve reports/allure-results/cart-dev --port 5300
```

**auth-service — UAT:**
```powershell
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue reports\allure-results\auth-service-uat
New-Item reports\allure-results\auth-service-uat -ItemType Directory -Force | Out-Null
behave src/bdd/auth-service -D env=uat -f allure_behave.formatter:AllureFormatter -o reports/allure-results/auth-service-uat -f progress
allure serve reports/allure-results/auth-service-uat --port 5300
```

**checkout NPG — DEV:**
```powershell
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue reports\allure-results\checkout-dev
New-Item reports\allure-results\checkout-dev -ItemType Directory -Force | Out-Null
behave src/bdd/checkout -D env=dev -f allure_behave.formatter:AllureFormatter -o reports/allure-results/checkout-dev -f progress
allure serve reports/allure-results/checkout-dev --port 5300
```

**ecommerce_cdc — DEV:**
```powershell
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue reports\allure-results\ecommerce-cdc-dev
New-Item reports\allure-results\ecommerce-cdc-dev -ItemType Directory -Force | Out-Null
behave src/bdd/ecommerce_cdc -D env=dev -f allure_behave.formatter:AllureFormatter -o reports/allure-results/ecommerce-cdc-dev -f progress
allure serve reports/allure-results/ecommerce-cdc-dev --port 5300
```

