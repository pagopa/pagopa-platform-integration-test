## Suite: checkout

# 1. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Timeout 80000ms exceeded.
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 9875, in wait_for_load_state
    self._sync(
        self._impl_obj.wait_for_load_state(
            state=state, timeout=to_milliseconds(timeout)
        )
    )
```
### Root cause
Page load state networkidle timed out due to slow external gateway responses or lingering network requests.

### Category
environment

### Recommended action
Increase the networkidle timeout or replace it with a more specific element visibility check.

---

# 2. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
```
### Root cause
The target Creditor Institution (EC) mock returned a generic error response instead of the expected 'not found' status.

### Category
test data

### Recommended action
Verify the mock configuration for the invalid notice code range to ensure the correct error code is returned.

---

# 3. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The PSP selection radio button for Postepay did not render within the 5-second timeout on the PSP list page.

### Category
flaky

### Recommended action
Increase the locator timeout or add an explicit wait for the PSP list container to fully load.

---

# 4. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The PSP selection radio button for Postepay did not render within the 5-second timeout on the PSP list page.

### Category
flaky

### Recommended action
Increase the locator timeout or add an explicit wait for the PSP list container to fully load.

---

## Common patterns
Failures in the checkout suite are primarily driven by UI element timeouts on dynamic pages and unexpected responses from external mock services.

## Suite: fdr3
The execution of the 'FDR-3' suite was complete, and no tests were skipped.

## Suite: wisp

# 1. L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
The payment flow did not generate the expected `RT_SEND_SUCCESS` receipt event within the monitoring system.

### Category
application bug

### Recommended action
Inspect backend logs for node and payment broker interactions to trace why the receipt was not successfully dispatched.

---

# 2. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
The payment flow did not generate the expected `RT_SEND_SUCCESS` receipt event within the monitoring system.

### Category
application bug

### Recommended action
Inspect backend logs for node and payment broker interactions to trace why the receipt was not successfully dispatched.

---

# 3. Utente tenta di pagare un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD in stato non valido
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente tenta di pagare un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
Expected redirect business process event with `RT_SEND_SUCCESS` was not recorded.

### Category
application bug

### Recommended action
Verify GPD state validation logic during payment activation requests.

---

# 4. L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
The payment flow did not generate the expected `RT_SEND_SUCCESS` receipt event within the monitoring system.

### Category
application bug

### Recommended action
Inspect backend logs for node and payment broker interactions to trace why the receipt was not successfully dispatched.

---

# 5. Utente tenta di pagare un pagamento singolo inserito da ACA e in stato non valido
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente tenta di pagare un pagamento singolo inserito da ACA e in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
Expected redirect business process event with `RT_SEND_SUCCESS` was not recorded.

### Category
application bug

### Recommended action
Verify ACA integration and status validation checks during payment requests.

---

# 6. L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
The payment flow did not generate the expected `RT_SEND_SUCCESS` receipt event within the monitoring system.

### Category
application bug

### Recommended action
Inspect backend logs for node and payment broker interactions to trace why the receipt was not successfully dispatched.

---

# 7. L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
Expected redirect business process event with `RT_SEND_SUCCESS` was not recorded.

### Category
application bug

### Recommended action
Verify ACA integration and status validation checks during payment requests.

---

# 8. L'utente paga un carrello con due RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT per un totale di cinque versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
No receipt-ok business process events were recorded for the cart payment.

### Category
application bug

### Recommended action
Check cart processing and multi-RPT handling in nodoInviaCarrelloRPT.

---

# 9. L'utente paga un carrello con quattro RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con quattro RPT con un versamento ciascuna`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
The payment flow did not generate the expected `RT_SEND_SUCCESS` receipt event within the monitoring system.

### Category
application bug

### Recommended action
Inspect backend logs for node and payment broker interactions to trace why the receipt was not successfully dispatched.

---

# 10. Utente paga un pagamento singolo con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento semplice e una marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
The payment flow did not generate the expected `RT_SEND_SUCCESS` receipt event within the monitoring system.

### Category
application bug

### Recommended action
Inspect backend logs for node and payment broker interactions to trace why the receipt was not successfully dispatched.

---

# 11. Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
No receipt-ok business process events were recorded.

### Category
application bug

### Recommended action
Verify GPD integration for pre-existing debt positions involving revenue stamps (marca da bollo).

---

# 12. L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
Expected redirect business process event with `RT_SEND_SUCCESS` was not recorded.

### Category
application bug

### Recommended action
Verify ACA integration and status validation checks during payment requests.

---

# 13. L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
The payment flow did not generate the expected `RT_SEND_SUCCESS` receipt event within the monitoring system.

### Category
application bug

### Recommended action
Inspect backend logs for node and payment broker interactions to trace why the receipt was not successfully dispatched.

---

# 14. L'utente tenta di pagare un carrello con due RPT gia esistenti in GPD in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT gia esistenti in GPD in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
Expected redirect business process event with `RT_SEND_SUCCESS` was not recorded.

### Category
application bug

### Recommended action
Verify GPD state validation logic during payment activation requests.

---

# 15. Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
The payment flow did not generate the expected `RT_SEND_SUCCESS` receipt event within the monitoring system.

### Category
application bug

### Recommended action
Inspect backend logs for node and payment broker interactions to trace why the receipt was not successfully dispatched.

---

# 16. L'utente paga un carrello con singola RPT con un versamento
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
The payment flow did not generate the expected `RT_SEND_SUCCESS` receipt event within the monitoring system.

### Category
application bug

### Recommended action
Inspect backend logs for node and payment broker interactions to trace why the receipt was not successfully dispatched.

---

# 17. L'utente paga un carrello multibeneficiario con due RPT con un totale di due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con two RPT con un totale di due versamenti`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
The payment flow did not generate the expected `RT_SEND_SUCCESS` receipt event within the monitoring system.

### Category
application bug

### Recommended action
Inspect backend logs for node and payment broker interactions to trace why the receipt was not successfully dispatched.

---

# 18. L'utente tenta di pagare un carrello con singola RPT gia esistente in GPD in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con singola RPT gia esistente in GPD in stato non valido`
- **message**: AssertionError: Eventi non trovati
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
Expected business process events were not found in the event store.

### Category
application bug

### Recommended action
Check event publisher service health and event tracing configuration.

---

# 19. L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
The payment flow did not generate the expected `RT_SEND_SUCCESS` receipt event within the monitoring system.

### Category
application bug

### Recommended action
Inspect backend logs for node and payment broker interactions to trace why the receipt was not successfully dispatched.

---

# 20. Utente paga un pagamento singolo con cinque versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con cinque versamenti e nessuna marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
  File "model.py", line 1329, in run
    assert assertion_value, message
```
### Root cause
The payment flow did not generate the expected `RT_SEND_SUCCESS` receipt event within the monitoring system.

### Category
application bug

### Recommended action
Inspect backend logs for node and payment broker interactions to trace why the receipt was not successfully dispatched.

---

## Common patterns
Across the WISP suite, failures consistently stem from missing business process events (`receipt-ok` or `redirect`) containing `RT_SEND_SUCCESS`, indicating a widespread issue with receipt generation or event publishing across various payment modalities (single RPT, carts, multi-beneficiary, and GPD/ACA integrations).

## Cross-suite correlation
- **Checkout Suite**: Suffers from UI element timeout issues and occasional environment/mock discrepancies.
- **WISP Suite**: Suffers from systematic backend event publishing failures where expected `RT_SEND_SUCCESS` events are absent across almost all test cases.
- **Fdr3 Suite**: Executed successfully with no correlation to failures elsewhere.