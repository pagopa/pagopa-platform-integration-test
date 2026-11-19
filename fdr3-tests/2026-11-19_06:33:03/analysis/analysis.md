## Suite: checkout

# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The PSP selection radio button for Postepay did not render within the 5-second timeout on the UAT page.

### Category
environment

### Recommended action
Increase the locator timeout or investigate UAT environment slowness/PSP availability issues.

---

# 2. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
```
### Root cause
The creditor institution (EC) mock returned a generic error instead of the expected unknown payment error.

### Category
application bug

### Recommended action
Verify the mock creditor institution configuration and backend error handling for invalid notice codes.

---

# 3. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Il pagamento non è andato a buon fine'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
```
### Root cause
The payment transaction was rejected or failed during processing with the Worldline gateway configuration.

### Category
environment

### Recommended action
Check NPG gateway logs and sandbox/UAT credentials for Worldline.

---

# 4. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The PSP selection radio button for Postepay timed out due to slow rendering or loading on the UAT page.

### Category
environment

### Recommended action
Investigate frontend performance or increase the explicit wait time for the PSP list elements.

---

## Common patterns
UI test failures in Checkout are primarily driven by environment timeouts loading specific PSP elements and intermittent gateway/mock failures.

## Suite: fdr3
No test failures found in the 'FDR-3' suite, and the execution completed successfully without any skipped tests.

## Suite: wisp

# 1. Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
The expected receipt-ok event with status RT_SEND_SUCCESS was not generated by the workflow backend.

### Category
application bug

### Recommended action
Inspect WISP and Node backend logs to trace the RPT submission and receipt generation failure.

---

# 2. L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Multi-beneficiary cart payment processing failed to complete with a successful receipt status.

### Category
application bug

### Recommended action
Review cart payment orchestration logs in nodoInviaCarrelloRPT flows.

---

# 3. L'utente tenta di pagare un carrello multibeneficiario inserito da ACA e in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello multibeneficiario inserito da ACA e in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
The redirect business process did not emit the expected success status for an invalid cart state.

### Category
application bug

### Recommended action
Verify validation logic for ACA-inserted multi-beneficiary carts in invalid states.

---

# 4. L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
No receipt-ok events were recorded for the multi-RPT cart payment flow.

### Category
application bug

### Recommended action
Check event publisher and WISP notification flows for multi-RPT carts.

---

# 5. Utente paga un pagamento singolo con cinque versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con cinque versamenti e nessuna marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Single payment with multiple installments failed to produce the success receipt event.

### Category
application bug

### Recommended action
Analyze payment receipt propagation for single payments with high installment counts.

---

# 6. L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Redirect event status assertion failed for a valid ACA cart flow.

### Category
application bug

### Recommended action
Verify ACA integration and cart redirection state transitions.

---

# 7. L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Cart payment involving pre-existing revenue stamps (marche da bollo) in GPD failed to complete.

### Category
application bug

### Recommended action
Check GPD state synchronization and duplicate revenue stamp handling during cart payments.

---

# 8. L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Complex cart with multiple RPTs and mixed revenue stamps failed to generate a receipt-ok event.

### Category
application bug

### Recommended action
Debug cart processing limits and breakdown handling for mixed versamenti and marche da bollo.

---

# 9. L'utente tenta di pagare un carrello multibeneficiario gia esistente in GPD in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello multibeneficiario gia esistente in GPD in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Existing multi-beneficiary cart in GPD with an invalid state failed to trigger the expected redirect error flow.

### Category
application bug

### Recommended action
Review GPD state validation rules for multi-beneficiary carts.

---

# 10. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo`
- **message**: AssertionError: There are no events with business process receipt-ko and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
The payment retry mechanism failed to properly register the initial receipt-ko event followed by success.

### Category
application bug

### Recommended action
Investigate retry logic and event logging for failed payment closures.

---

# 11. L'utente paga un carrello con singola RPT con tre versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con tre versamenti`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Single RPT cart with three installments failed to complete successfully.

### Category
application bug

### Recommended action
Check cart execution flow for single RPT multi-installment scenarios.

---

# 12. Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Single payment with four installments did not emit a receipt-ok event.

### Category
application bug

### Recommended action
Verify event generation rules for single payments with multiple installments.

---

# 13. L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Cart with multiple installments pre-existing in GPD failed to complete.

### Category
application bug

### Recommended action
Inspect GPD debt position retrieval and cart execution integration.

---

# 14. Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Single payment with three installments failed to produce a successful receipt event.

### Category
application bug

### Recommended action
Trace payment execution and receipt generation for multi-installment single payments.

---

# 15. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Cart containing only a revenue stamp and no simple installment failed to complete.

### Category
application bug

### Recommended action
Verify stamp-only cart processing logic in WISP.

---

# 16. L'utente paga un carrello con three RPT per un totale di dieci versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di dieci versamenti`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Large cart with 3 RPTs and 10 total installments failed to complete successfully.

### Category
application bug

### Recommended action
Check payload limits and processing timeouts for large cart transactions.

---

# 17. L'utente tenta di pagare un carrello con due RPT gia esistenti in GPD in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT gia esistenti in GPD in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Redirect validation failed for pre-existing GPD carts in invalid states.

### Category
application bug

### Recommended action
Review GPD state validation handling for cart redirects.

---

# 18. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
- **message**: AssertionError: Test execution details omitted for brevity.
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Cart payment from existing GPD debt position failed to complete.

### Category
application bug

### Recommended action
Inspect GPD integration and event emission for single RPT carts.

---

# 19. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD`
- **message**: AssertionError: Test execution details omitted for brevity.
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Single payment from existing GPD debt position failed to generate receipt events.

### Category
application bug

### Recommended action
Verify GPD synchronization for single payment flows.

---

# 20. L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato non valido`
- **message**: AssertionError: Test execution details omitted for brevity.
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
ACA-inserted cart validation failed to produce the expected redirect error event.

### Category
application bug

### Recommended action
Check ACA validation rules and error event emission.

---

## Common patterns
The WISP test suite failures are heavily concentrated around missing event assertions (`receipt-ok`, `receipt-ko`, and `redirect` events with `RT_SEND_SUCCESS`), indicating a systemic issue where payment receipts or event notifications are not being properly dispatched or recorded during complex cart and multi-installment payment flows.

## Cross-suite correlation
- **Checkout Suite**: Suffers from UI element timeouts and environment/mock integration issues.
- **WISP Suite**: Suffers from backend event emission failures (missing `receipt-ok`/`redirect` events), pointing to downstream notification or receipt processing issues in the platform integration layer.
- **Correlation**: Both suites indicate integration-level friction, where Checkout relies on stable UI components and PSP mocks, while WISP relies on reliable backend event logging and receipt generation across complex cart and installment flows.