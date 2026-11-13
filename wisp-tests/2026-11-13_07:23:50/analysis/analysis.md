## Suite: checkout

# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
UI element for the specified PSP radio button failed to load or rendered slowly, causing a locator timeout.

### Category
environment

### Recommended action
Increase the locator timeout threshold or check if the PSP list service is experiencing latency.

---

# 2. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
```
### Root cause
The payment confirmation polling timed out or received a delayed callback, leaving the status as pending ("Attendi la conferma del pagamento").

### Category
flaky

### Recommended action
Implement an explicit wait with polling for the payment success message instead of a single assertion check.

---

# 3. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
```
### Root cause
The payment confirmation polling timed out or received a delayed callback, leaving the status as pending ("Attendi la conferma del pagamento").

### Category
flaky

### Recommended action
Implement an explicit wait with polling for the payment success message instead of a single assertion check.

---

# 4. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
```
### Root cause
The payment confirmation polling timed out or received a delayed callback, leaving the status as pending ("Attendi la conferma del pagamento").

### Category
flaky

### Recommended action
Implement an explicit wait with polling for the payment success message instead of a single assertion check.

---

# 5. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
```
### Root cause
Upstream creditor institution mock returned a generic error response instead of the expected unknown payment notice error.

### Category
application bug

### Recommended action
Verify the creditor institution simulator configuration for invalid notice codes to ensure proper error mapping.

---

# 6. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BNLIITRR' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
UI element for the specified PSP radio button failed to load or rendered slowly, causing a locator timeout.

### Category
environment

### Recommended action
Increase the locator timeout threshold or check if the PSP list service is experiencing latency.

---

# 7. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
UI element for the specified PSP radio button failed to load or rendered slowly, causing a locator timeout.

### Category
environment

### Recommended action
Increase the locator timeout threshold or check if the PSP list service is experiencing latency.

---

## Common patterns
- PSP selection failures are caused by UI load timeouts on the `lista-psp` page.
- Payment completion assertions fail due to race conditions where the backend takes longer than expected to transition from pending to success.

## Suite: fdr3

No test failures found in the 'FDR-3' suite. Confirm that the execution was complete and that no tests were unintentionally skipped. Reply in English, in a single sentence.

## Suite: wisp

# 1. L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 2. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 3. L'utente paga un carrello con tre RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di cinque versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 4. Utente tenta due volte di pagare la stessa RPT ma la conversione al nuovo modello fallisce
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente tenta due volte di pagare la stessa RPT ma la conversione al nuovo modello fallisce`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 5. L'utente paga un carrello con singola RPT con tre versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con tre versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 6. Utente tenta il pagamento, poi riprova il flusso ma fallisce
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente tenta il pagamento, poi riprova il flusso ma fallisce`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 7. L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 8. L'utente paga un carrello con singola RPT con quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con quattro versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 9. L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 10. Utente paga un pagamento singolo con nessun versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con nessun versamento semplice e una marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 11. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 12. L'utente paga un carrello con singola RPT con cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con cinque versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 13. L'utente paga un carrello con singola RPT con un versamento
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 14. L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 15. L'utente paga un carrello con quattro RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con quattro RPT con un versamento ciascuna`
- **message**: AssertionError: Test status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 16. Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 17. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 18. L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistened in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 19. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

# 20. L'utente paga un carrello con singola RPT con due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) encountered during position check / cart redirect.

### Category
application bug

### Recommended action
Investigate backend application logs using the activity ID to trace the internal exception.

---

## Common patterns
- All WISP failures consistently stem from an HTTP 500 Internal Server Error during the `checkPosition` step when attempting to redirect to Checkout.

## Cross-suite correlation
- Both the **checkout** and **wisp** suites experience failures related to payment checkout flows and redirects. While **checkout** is impacted by UI locator timeouts and polling races, **wisp** suffers from widespread backend HTTP 500 errors during position checks. It is recommended to check downstream payment gateway connectivity and WISP backend services for systemic issues.