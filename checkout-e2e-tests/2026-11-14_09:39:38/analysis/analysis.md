## Suite: checkout

# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The specific PSP radio option `#psp-radio-PPAYITR1XXX` did not load on the PSP list page within the 5000ms timeout limit.

### Category
flaky

### Recommended action
Increase the explicit wait timeout or retry logic for rendering PSP elements on the `lista-psp` page, and verify Postepay PSP availability in UAT.

---

# 2. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
The backend returned a Creditor Entity response error instead of the expected unknown payment error for the invalid notice code range.

### Category
application bug

### Recommended action
Investigate the payment activation backend handling for invalid notice codes in the 302400000000000000 range to ensure `PAA_PAGAMENTO_SCONOSCIUTO` is mapped correctly.

---

# 3. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The authenticated user checkout flow failed to load `#psp-radio-PPAYITR1XXX` within 5000ms.

### Category
flaky

### Recommended action
Standardize PSP element rendering waits across both standard and authenticated Checkout E2E flows.

---

# 4. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
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
The payment status remained in a pending state ('Attendi la conferma del pagamento') instead of transitioning asynchronously to final success ('Hai pagato') before validation.

### Category
flaky

### Recommended action
Implement polling or lengthen assertion timeout on the final result message page to allow async payment confirmation to settle.

---

# 5. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
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
Payment confirmation remained pending ('Attendi la conferma del pagamento') at the time of assertion in the authenticated Wordline payment scenario.

### Category
flaky

### Recommended action
Add retries or wait explicitly for the final payment completion screen during Wordline integrations.

---

## Common patterns
- **UI Element Loading Delays**: Postepay PSP radio locator `#psp-radio-PPAYITR1XXX` fails consistently due to locator timeouts on the selection page.
- **Async Payment Resolution**: Wordline payments remain in pending state (`Attendi la conferma del pagamento`) due to strict UI checks occurring before backend confirmation completes.

---

## Suite: fdr3

No test failures found in the 'FDR-3' suite. Confirm that the execution was complete and that no tests were unintentionally skipped.

## Suite: wisp

# 1. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` call returned HTTP 500 Internal Server Error (`{"statusCode":500,"message":"Internal server error"}`).

### Category
application bug

### Recommended action
Check application logs for `closepayment` service using activityId `5b081481-8b1d-49a9-84df-7b…` to diagnose backend exception.

---

# 2. L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` backend endpoint failed with HTTP 500 Internal Server Error.

### Category
application bug

### Recommended action
Investigate backend error logs for activityId `4fd44da0-f801-4d5e-b022-bc…` on `closepayment`.

---

# 3. L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` step failed due to HTTP 500 returned by the payment engine backend.

### Category
application bug

### Recommended action
Inspect server-side stack trace for activityId `7f0e3fd1-b011-402a-904d-51…`.

---

# 4. L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
Backend thrown HTTP 500 Internal Server Error during `closepayment`.

### Category
application bug

### Recommended action
Correlate activityId `c4254402-526d-4f3e-b1a4-31…` in backend monitoring system.

---

# 5. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` returned HTTP 500 Internal Server Error.

### Category
application bug

### Recommended action
Review API gateway/backend logs for activityId `1a83cf80-a470-4dca-9db2-37…`.

---

# 6. L'utente paga un carrello con due RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT per un totale di cinque versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` returned HTTP 500 Internal Server Error.

### Category
application bug

### Recommended action
Analyze server exception associated with activityId `a65ec28f-8a6c-4ab9-bd3b-90…`.

---

# 7. L'utente paga un carrello con singola RPT con un versamento
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 error returned by `closepayment` service.

### Category
application bug

### Recommended action
Inspect backend service logs for failure details on activityId `77ae29c2-08c1-495b-bc43-02…`.

---

# 8. Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` service failure returning HTTP 500.

### Category
application bug

### Recommended action
Check backend microservice logs matching activityId `136a3e48-c222-4e82-b7dc-f7…`.

---

# 9. Utente esegue un primo reindirizzamento, poi ripete il reindirizzamento e completa il flusso di pagamento
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente esegue un primo reindirizzamento, poi ripete il reindirizzamento e completa il flusso di pagamento`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` service failed with HTTP 500.

### Category
application bug

### Recommended action
Verify handling of repeated redirects in `closepayment` service via activityId `421684d8-551d-4b66-86b0-b9…`.

---

# 10. L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` call returned HTTP 500 Internal Server Error.

### Category
application bug

### Recommended action
Investigate server-side trace for activityId `0e4c0979-0c02-4021-bc13-c5…`.

---

# 11. Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` service returned HTTP 500.

### Category
application bug

### Recommended action
Check application logs for activityId `96453eb4-8ccf-46dc-aabb-28…`.

---

# 12. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` failed with HTTP 500 Internal Server Error.

### Category
application bug

### Recommended action
Examine backend logs using activityId `dea8b0d1-e91f-4137-8f68-18…`.

---

# 13. Utente tenta due volte di pagare la stessa RPT ma la conversione al nuovo modello fallisce
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente tenta due volte di pagare la stessa RPT ma la conversione al nuovo modello fallisce`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 received from `closepayment` backend during conversion handling.

### Category
application bug

### Recommended action
Investigate backend error logs for activityId `ed255dd7-fa04-46b1-b353-a1…`.

---

# 14. L'utente paga un carrello con singola RPT con cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con cinque versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` API endpoint returned HTTP 500.

### Category
application bug

### Recommended action
Retrieve details for activityId `8f037c3a-cc1d-454d-b04b-7b…` in logging framework.

---

# 15. L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` endpoint returned HTTP 500 Internal Server Error.

### Category
application bug

### Recommended action
Query server telemetry for activityId `625c258b-1476-4393-a879-af…`.

---

# 16. L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` service failed with HTTP 500 Internal Server Error.

### Category
application bug

### Recommended action
Check backend logs corresponding to activityId `cec9b80b-8812-4d79-a534-11…`.

---

# 17. L'utente paga un carrello con singola RPT con due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 status returned by `closepayment` step.

### Category
application bug

### Recommended action
Review server errors linked to activityId `741a3166-cd5e-4cea-a856-65…`.

---

# 18. L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` service returned HTTP 500 Internal Server Error.

### Category
application bug

### Recommended action
Verify log traces for activityId `a439a492-d51a-41a2-a7ef-b1…`.

---

# 19. Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` operation failed with HTTP 500 Internal Server Error.

### Category
application bug

### Recommended action
Investigate backend application errors for activityId `82e5a454-65e0-49a9-992d-b5…`.

---

# 20. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
`closepayment` backend service returned HTTP 500 Internal Server Error.

### Category
application bug

### Recommended action
Examine server logs associated with activityId `dc290d19-842b-4369-a63b-e9…`.

---

## Common patterns
- **Systemic Backend Failure on `closepayment`**: All failures in the `wisp` suite consistently fail at the step redirecting to Checkout because the underlying `closepayment` REST endpoint returns an `HTTP 500 Internal Server Error`.

---

## Cross-suite correlation

Analyzing failures across the **checkout** and **wisp** suites reveals distinct failure patterns:

1. **WISP `closepayment` Backend Outage / Service Degradation**:
   - **Pattern**: Every failure reported in the `wisp` suite stems from the `closepayment` API returning HTTP 500 (`Internal server error`).
   - **Impact**: Payment redirections fail completely across single/cart RPT scenarios.
   - **Recommended Action**: Escalate to the backend/platform team responsible for the `closepayment` microservice to investigate activity logs and restore service stability in UAT.

2. **Checkout UI Timing & PSP Availability Issues**:
   - **Pattern**: Failures in `checkout` are driven by UI layer issues, specifically locator timeouts (`#psp-radio-PPAYITR1XXX`) and non-deterministic payment state transitions (`Attendi la conferma del pagamento` instead of immediate completion).
   - **Impact**: E2E test instability on specific PSP selections and asynchronous confirmation steps.
   - **Recommended Action**: Update test automation helpers to include robust retries/polling for payment completion screens and review PSP mock dynamic load performance in test environments.