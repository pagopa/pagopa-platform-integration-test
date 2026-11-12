## Suite: checkout

# 1. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Payment transaction remains stuck in pending state ("Attendi la conferma del pagamento") instead of reaching final successful status.

### Category
application bug

### Recommended action
Investigate NPG/Wordline payment gateway callbacks and backend authorization response processing.

---

# 2. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Authenticated payment flow via Wordline card remains in pending status instead of reaching confirmation.

### Category
application bug

### Recommended action
Check backend notification status polling and Wordline gateway integration in UAT.

---

# 3. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
PSP selection element for Postepay (`#psp-radio-PPAYITR1XXX`) did not render in UI within 5 seconds.

### Category
flaky

### Recommended action
Verify if Postepay PSP was returned by the API bundle list or increase UI locator wait timeout.

---

# 4. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Payment transaction processing via Worldpay timed out or stayed stuck in pending state.

### Category
application bug

### Recommended action
Verify async authorization processing and webhook handlers for Worldpay integration.

---

# 5. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Postepay PSP option failed to render on UI in time during authenticated checkout flow.

### Category
flaky

### Recommended action
Increase element availability wait times and ensure Postepay active bundles exist in environment.

---

# 6. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Incorrect error modal UI displayed for unknown payment error (creditor entity technical error shown instead of unknown notice error).

### Category
application bug

### Recommended action
Verify mapping of `PAA_PAGAMENTO_SCONOSCIUTO` fault code to frontend user error messages.

---

# 7. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Authenticated payment via Worldpay remains stuck in pending payment state.

### Category
application bug

### Recommended action
Investigate NPG outcome notification sync to the checkout frontend.

---

## Common patterns
- **Pending Payment State Stuck**: Multiple NPG card payment tests (Wordline, Worldpay) fail because UI remains on 'Attendi la conferma del pagamento' instead of displaying payment completion ('Hai pagato').
- **PSP Locator Timeouts**: Postepay radio buttons failed to load dynamically within the strict 5000ms UI wait limit.

---

## Suite: fdr3

No test failures found in the 'FDR-3' suite. Confirm that the execution was complete and that no tests were unintentionally skipped.

---

## Suite: wisp

# 1. Utente esegue un primo reindirizzamento, poi ripete il reindirizzamento e completa il flusso di pagamento
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente esegue un primo reindirizzamento, poi ripete il reindirizzamento e completa il flusso di pagamento`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected with HTTP 401 due to missing or invalid APIM subscription key in test environment headers.

### Category
environment

### Recommended action
Update or refresh the APIM subscription key secret used in test execution pipelines for WISP.

---

# 2. Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
Invalid APIM subscription key causing HTTP 401 authentication error on backend endpoints.

### Category
environment

### Recommended action
Verify configuration of test APIM keys across pipeline variables.

---

# 3. L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti oltre il limite
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti oltre il limite`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
APIM authentication failure (401 Access Denied) preventing SOAP/XML payload transmission.

### Category
environment

### Recommended action
Rotate and deploy valid APIM subscription key to secret store.

---

# 4. Utente tenta due volte di pagare la stessa RPT ma la conversione al nuovo modello fallisce
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente tenta due volte di pagare la stessa RPT ma la conversione al nuovo modello fallisce`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
Request blocked at API Gateway level due to invalid subscription key.

### Category
environment

### Recommended action
Check test environment gateway subscription status.

---

# 5. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Access Denied due to expired or incorrect APIM key.

### Category
environment

### Recommended action
Ensure valid credentials exist for WISP integration test endpoints.

---

# 6. L'utente paga un carrello con tre RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di cinque versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API gateway access denied (401) due to invalid APIM key.

### Category
environment

### Recommended action
Re-issue subscription keys for WISP node endpoints.

---

# 7. Utente tenta di pagare un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD in stato non valido
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente tenta di pagare un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD in stato non valido`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 authentication failure on API Gateway.

### Category
environment

### Recommended action
Provide active subscription key in test request headers.

---

# 8. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
Invalid subscription key rejected by API Management gateway.

### Category
environment

### Recommended action
Audit APIM subscription configurations for UAT integration testing.

---

# 9. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Access Denied response from API Gateway.

### Category
environment

### Recommended action
Update test pipeline secrets with valid APIM credentials.

---

# 10. L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
Gateway authentication rejected (401 Invalid subscription key).

### Category
environment

### Recommended action
Fix APIM key subscription bindings in pipeline settings.

---

# 11. L'utente paga un carrello con singola RPT con due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
Unauthorized status 401 returned due to invalid APIM key.

### Category
environment

### Recommended action
Verify subscription key provisioning on Azure APIM.

---

# 12. L'utente paga un carrello con singola RPT con quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con quattro versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
401 Access Denied from API Gateway.

### Category
environment

### Recommended action
Ensure environment variables contain active APIM key.

---

# 13. Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
Invalid subscription key causing gateway authorization rejection (401).

### Category
environment

### Recommended action
Refresh APIM integration keys.

---

# 14. Utente paga un pagamento singolo con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento semplice e una marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Access Denied due to subscription key failure.

### Category
environment

### Recommended action
Check APIM policy and subscription validity.

---

# 15. L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
Access denied (401) due to invalid API key.

### Category
environment

### Recommended action
Inject proper subscription key into pipeline configuration.

---

# 16. L'utente tenta di pagare un carrello con due RPT gia esistenti in GPD in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT gia esistenti in GPD in stato non valido`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
APIM authentication key rejected (401).

### Category
environment

### Recommended action
Validate API key credentials across UAT environments.

---

# 17. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
401 Access Denied from gateway due to invalid subscription key.

### Category
environment

### Recommended action
Rotate test pipeline APIM credentials.

---

# 18. L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
Invalid subscription key causing HTTP 401 error.

### Category
environment

### Recommended action
Update test secrets with working APIM keys.

---

# 19. L'utente paga un carrello con singola RPT con un versamento
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
APIM Gateway authorization failed (HTTP status 401).

### Category
environment

### Recommended action
Verify APIM subscription state for integration tests.

---

# 20. L'utente tenta di pagare un carrello multibeneficiario gia esistente in GPD in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello multibeneficiario gia esistente in GPD in stato non valido`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
Access denied on gateway call due to invalid subscription key.

### Category
environment

### Recommended action
Renew WISP test subscription credentials.

---

## Common patterns
- **Suite-wide APIM Authentication Failure**: All 69 failures in the WISP suite share the exact same root cause (`HTTP status 401: Access denied due to invalid subscription key`). The test environment lacks a valid API Management key header.

---

## Cross-suite correlation

Analyzing failures across the analyzed test suites reveals distinct, non-overlapping root cause patterns per suite:

1. **API Gateway / Environment Credential Issue (WISP Suite)**:
   - All tests in the WISP suite fail systematically due to an invalid or missing APIM subscription key returning HTTP 401 errors.
   - **Action**: Fix pipeline environment secrets and re-issue valid Azure APIM subscription keys for WISP integration endpoints.

2. **Application Logic & UI Async Handlers (Checkout Suite)**:
   - Card payments (Wordline/Worldpay) fail functional assertions because payment states remain stuck in "Attendi la conferma del pagamento" rather than concluding successfully.
   - Frontend error handling displays incorrect error modal titles for `PAA_PAGAMENTO_SCONOSCIUTO` fault codes.
   - **Action**: Debug NPG authorization status callback/polling flows and correct fault code translation in Checkout UI.