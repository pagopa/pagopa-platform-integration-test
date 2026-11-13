## Suite: checkout

# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
Element locator for Postepay PSP radio button failed to load or was missing within the timeout.

### Category
environment

### Recommended action
Verify if the PSP configuration or UAT environment is experiencing rendering delays or if the selector needs updating.

---

# 2. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The system returned a generic creditor issuer error instead of the expected 'notice not found' error message.

### Category
application bug

### Recommended action
Check backend handling for invalid notice code ranges to ensure correct error mapping (PAA_PAGAMENTO_SCONOSCIUTO).

---

# 3. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Payment completion status polling timed out or webhook confirmation is delayed, leaving the UI in a pending state.

### Category
flaky

### Recommended action
Increase the polling timeout for payment confirmation or check NPG/Worldpay sandbox callback reliability.

---

# 4. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Payment completion status polling timed out or webhook confirmation is delayed, leaving the UI in a pending state.

### Category
flaky

### Recommended action
Increase the polling timeout for payment confirmation or check NPG/Worldpay sandbox callback reliability.

---

# 5. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
Element locator for Postepay PSP radio button failed to load or was missing within the timeout.

### Category
environment

### Recommended action
Verify if the PSP configuration or UAT environment is experiencing rendering delays or if the selector needs updating.

---

# 6. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Payment completion status polling timed out or webhook confirmation is delayed, leaving the UI in a pending state.

### Category
flaky

### Recommended action
Increase the polling timeout for payment confirmation or check NPG/Wordline sandbox callback reliability.

---

# 7. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Payment completion status polling timed out or webhook confirmation is delayed, leaving the UI in a pending state.

### Category
flaky

### Recommended action
Increase the polling timeout for payment confirmation or check NPG/Wordline sandbox callback reliability.

---

## Common patterns
- **Gateway confirmation delay**: Multiple payment completion tests fail because the UI remains stuck on "Attendi la conferma del pagamento", indicating asynchronous notification or polling issues across multiple PSPs (Worldpay, Wordline).
- **PSP selection timeout**: Postepay PSP elements intermittently fail to load within the 5s window.

## Suite: fdr3
No test failures found in the 'FDR-3' suite, and execution completed successfully without skipped tests.

## Suite: wisp

# 1. L'utente paga un carrello con singola RPT con due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 2. L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 3. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 4. Utente paga un pagamento singolo con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento semplice e una marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 5. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 6. L'utente paga un carrello con quattro RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con quattro RPT con un versamento ciascuna`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 7. L'utente paga un carrello con singola RPT con quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con quattro versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 8. L'utente paga un carrello con tre RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di cinque versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 9. L'utente paga un carrello con tre RPT per un totale di dieci versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di dieci versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 10. L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 11. L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 12. L'utente tenta di pagare un carrello con singola RPT gia esistente in GPD in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con singola RPT gia esistente in GPD in stato non valido`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 13. Utente paga un pagamento singolo di tipo PO con due versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo di tipo PO con due versamenti e nessuna marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 14. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 15. L'utente tenta di pagare un carrello multibeneficiario con due RPT con una marca da bollo, ma fallisce perche una RPT ha la marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello multibeneficiario con due RPT con una marca da bollo, ma fallisce perche una RPT ha la marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 16. L'utente paga un carrello con cinque RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con cinque RPT con un versamento ciascuna`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 17. Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 18. L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request Calls rejected due to an invalid subscription key.

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 19. L'utente paga un carrello con tre RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT con un versamento ciascuna`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

# 20. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
API request rejected due to an invalid or missing API subscription key (HTTP 401).

### Category
environment

### Recommended action
Update the test environment secrets with a valid, active APIM subscription key.

---

## Common patterns
- **Subscription Key Authentication Failure**: All 69 failures in the WISP suite stem from HTTP 401 responses indicating an invalid or expired API subscription key for the endpoints being tested.

## Cross-suite correlation
- **Environment & Configuration Issues**: Both `checkout` and `wisp` suites exhibit environment-related issues (element loading timeouts and API authentication failures respectively), suggesting that test execution environments require validation of credentials and service health before test runs.