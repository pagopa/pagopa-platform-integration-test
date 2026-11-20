## Suite: checkout

# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The Postepay PSP option did not load within the 5-second timeout on the checkout page.

### Category
environment

### Recommended action
Increase the element wait timeout or verify the availability and response time of the PSP listing service in UAT.

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
The creditor institution (Ente Creditore) returned a generic error response instead of the expected unknown payment error.

### Category
application bug

### Recommended action
Check backend integration handling for invalid notice codes to ensure proper error mapping.

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
Intermittent UI loading timeout for the Postepay PSP option on the checkout page.

### Category
flaky

### Recommended action
Add retry logic or increase the explicit wait timeout for PSP selection elements.

---

## Common patterns
PSP selection timeouts indicate potential frontend performance bottlenecks or environment instability during test execution.

## Suite: fdr3
The FDR-3 execution was complete and no tests were unintentionally skipped.

## Suite: wisp

# 1. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Missing receipt generation event (`RT_SEND_SUCCESS`) for the cart payment process.

### Category
application bug

### Recommended action
Investigate the backend notification and receipt delivery pipeline for cart transactions.

---

# 2. Utente esegue un primo reindirizzamento, poi ripete il reindirizzamento e completa il flusso di pagamento
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente esegue un primo reindirizzamento, poi ripete il reindirizzamento e completa il flusso di pagamento`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Failure to generate the final receipt after repeated payment redirection flows.

### Category
application bug

### Recommended action
Verify state management during repeated redirect attempts to ensure receipt generation completes.

---

# 3. L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
The expected redirect or status validation event for invalid ACA cart positions was not triggered.

### Category
application bug

### Recommended action
Review validation logic for ACA-inserted carts in invalid states.

---

# 4. L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Multi-beneficiary cart payment failed to produce the success receipt event.

### Category
application bug

### Recommended action
Trace the multi-beneficiary payment orchestration to identify where receipt confirmation fails.

---

# 5. L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Multi-beneficiary cart payment processing failed to complete successfully and generate a receipt.

### Category
application bug

### Recommended action
Inspect transaction logs for multi-RPT carts with four transfers to identify blocking errors.

---

# 6. L'utente paga un carrello con singola RPT con quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con quattro versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Complete absence of `receipt-ok` business process events for single RPT carts with four transfers.

### Category
application bug

### Recommended action
Check transaction processing limits and error handling for carts with multiple transfers.

---

# 7. L'utente tenta di pagare un carrello multibeneficiario inserito da ACA e in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello multibeneficiario inserito da ACA e in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Incorrect handling or missing event generation for invalid multi-beneficiary ACA carts.

### Category
application bug

### Recommended action
Verify validation rules and event publishing for invalid ACA positions in multi-beneficiary carts.

---

# 8. L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
High-transfer multi-beneficiary cart payments fail to generate receipts.

### Category
application bug

### Recommended action
Analyze backend capacity and execution flow for complex multi-RPT carts.

---

# 9. L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Missing redirect or receipt success events for valid ACA-inserted single RPT carts.

### Category
application bug

### Recommended action
Debug the redirect phase for valid ACA positions.

---

# 10. L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Duplicate stamp duty (marca da bollo) handling in GPD prevents successful receipt generation.

### Category
application bug

### Recommended action
Verify GPD integration logic for pre-existing stamp duties within cart payments.

---

# 11. L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Failure to trigger expected redirect/error flow for invalid two-RPT ACA carts.

### Category
application bug

### Recommended action
Check validation and error response handling for multi-RPT ACA positions.

---

# 12. L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Cart payment containing multiple RPTs with stamp duties fails to complete the receipt cycle.

### Category
application bug

### Recommended action
Investigate transaction processing for multi-RPT carts involving stamp duties.

---

# 13. Utente paga un pagamento singolo con due versamenti semplici e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti semplici e una marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Single payment with multiple transfers and stamp duty fails to generate a success receipt.

### Category
application bug

### Recommended action
Check the receipt generation service for single payments with complex transfer structures.

---

# 14. L'utente paga un carrello con singola RPT con due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Single RPT cart payment with two transfers fails to complete the receipt workflow.

### Category
application bug

### Recommended action
Debug cart payment execution for multi-transfer single RPT scenarios.

---

# 15. Utente tenta di pagare un pagamento singolo inserito da ACA e in stato non valido
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente tenta di pagare un pagamento singolo inserito da ACA e in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Invalid ACA single payment fails to trigger the expected redirect or status event.

### Category
application bug

### Recommended action
Verify error handling and event emission for invalid single payments from ACA.

---

# 16. L'utente tenta di pagare un carrello con due RPT gia esistenti in GPD in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT gia esistenti in GPD in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Existing invalid GPD cart positions fail to trigger proper redirect handling.

### Category
application bug

### Recommended action
Review validation and redirect triggers for pre-existing invalid carts in GPD.

---

# 17. L'utente paga un carrello con quattro RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con quattro RPT con un versamento ciascuna`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Large cart structures (four RPTs) fail to complete the receipt generation phase.

### Category
application bug

### Recommended action
Inspect backend transaction limits and asynchronous processing for large carts.

---

# 18. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Single RPT cart with stamp duty fails to finalize receipt processing.

### Category
application bug

### Recommended action
Verify stamp duty processing integration within cart payment flows.

---

# 19. Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Single payment with multiple stamp duties fails to generate success receipts.

### Category
application bug

### Recommended action
Debug multi-stamp duty handling for single payments.

---

# 20. Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Pre-existing stamp duty in GPD for single payments disrupts the final receipt event emission.

### Category
application bug

### Recommended action
Check GPD synchronization and receipt generation logic for pre-existing stamp duties.

---

## Common patterns
The vast majority of WISP failures stem from missing `receipt-ok` (`RT_SEND_SUCCESS`) or redirect events across various payment flows (carts, multi-beneficiary, ACA-inserted positions, and stamp duties), pointing to a systemic backend issue in transaction finalization or event publishing.

## Cross-suite correlation
Across the suites, Checkout experiences intermittent UI loading/timeout issues and error handling discrepancies, while WISP exhibits a widespread systemic failure in backend receipt generation and event publishing (`RT_SEND_SUCCESS`) across diverse payment scenarios. Addressing the WISP backend event emission pipeline is critical to resolving the bulk of the integration test failures.