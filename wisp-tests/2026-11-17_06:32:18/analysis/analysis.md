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
The PSP selection radio button for Postepay failed to load or render within the 5-second timeout window.

### Category
environment

### Recommended action
Investigate UAT PSP configuration services or increase the locator timeout if the environment is experiencing latency.

---

# 2. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
The system returned a generic creditor issuer error instead of the expected unknown payment error modal.

### Category
application bug

### Recommended action
Verify backend error handling mappings for invalid notice codes to ensure `PAA_PAGAMENTO_SCONOSCIUTO` is correctly translated.

---

# 3. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The PSP selection radio button for Postepay failed to load or render within the 5-second timeout window during authenticated checkout.

### Category
environment

### Recommended action
Check service stability for the PSP listing endpoint in UAT.

---

## Suite: fdr3

The execution of the 'FDR-3' suite was complete, and no tests were unintentionally skipped.

## Suite: wisp

# 1. L'utente tenta di pagare un carrello multibeneficiario gia esistente in GPD in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello multibeneficiario gia esistente in GPD in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
The test expected a redirect business process event with `RT_SEND_SUCCESS`, but no matching event was recorded.

### Category
application bug

### Recommended action
Inspect WISP backend event logging and transaction flows to verify why redirect events fail to generate for invalid GPD states.

---

# 2. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
The receipt-ok business process event did not reach `RT_SEND_SUCCESS` status during payment completion.

### Category
application bug

### Recommended action
Verify downstream receipt generation and transmission services for existing GPD carts.

---

# 3. Utente esegue un primo reindirizzamento, poi ripete il reindirizzamento e completa il flusso di pagamento
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente esegue un primo reindirizzamento, poi ripete il reindirizzamento e completa il flusso di pagamento`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Repeated redirection flows failed to finalize with a successful receipt status event.

### Category
application bug

### Recommended action
Review session handling and state machine logic when a user retries a payment redirection.

---

# 4. L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Multi-RPT carts containing stamps (marche da bollo) failed to produce the expected `RT_SEND_SUCCESS` receipt event.

### Category
application bug

### Recommended action
Debug cart processing logic for multi-RPT transactions involving revenue stamps.

---

# 5. L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Single RPT carts with multiple payments and stamps failed to complete the receipt-ok business process.

### Category
application bug

### Recommended action
Check payment orchestration for complex single RPT structures with stamps.

---

# 6. L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Asymmetric multi-RPT carts with stamps failed to complete successfully.

### Category
application bug

### Recommended action
Validate cart aggregation and splitting logic in the WISP payment flow.

---

# 7. L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Existing GPD debt position flows with a stamp failed to reach `RT_SEND_SUCCESS`.

### Category
application bug

### Recommended action
Examine GPD integration handling for pre-existing debt positions containing stamps.

---

# 8. L'utente tenta di pagare un carrello con due RPT gia esistenti in GPD in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT gia esistenti in GPD in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Invalid GPD state checks failed to generate the expected redirect process events.

### Category
application bug

### Recommended action
Verify error flow triggers for invalid multi-RPT debt positions retrieved from GPD.

---

# 9. L'utente paga un carrello con singola RPT con cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con cinque versamenti`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
High-volume payment installments (five transfers) failed to produce a successful receipt event.

### Category
application bug

### Recommended action
Check payload limits and processing constraints for RPTs containing multiple transfers.

---

# 10. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
No receipt-ok business process events were recorded at all for this configuration.

### Category
application bug

### Recommended action
Trace the end-to-end execution of single RPT payments with stamps to identify where event publishing fails.

---

# 11. L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Multi-beneficiary cart execution failed to complete with `RT_SEND_SUCCESS`.

### Category
application bug

### Recommended action
Investigate multi-beneficiary routing and settlement reporting logic.

---

# 12. L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Multi-beneficiary cart with five transfers failed to complete successfully.

### Category
application bug

### Recommended action
Review transaction limits and handling for multi-beneficiary carts.

---

# 13. L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Pre-existing GPD multi-RPT cart with stamps failed to complete the receipt process.

### Category
application bug

### Recommended action
Examine GPD synchronization for multi-RPT debt positions containing stamps.

---

# 14. L'utente paga un carrello con quattro RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con quattro RPT con un versamento ciascuna`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Cart with four separate RPTs failed to generate the success receipt event.

### Category
application bug

### Recommended action
Debug batch processing of large cart structures across multiple RPTs.

---

# 15. L'utente paga un carrello con due RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT per un totale di cinque versamenti`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Cart with two RPTs and five total transfers failed to complete successfully.

### Category
application bug

### Recommended action
Analyze transfer mapping and execution logs for multi-RPT carts.

---

# 16. L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato non valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
ACA-inserted RPT with invalid state failed to trigger the expected redirect event.

### Category
application bug

### Recommended action
Check ACA integration and state validation rules within WISP.

---

# 17. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Single RPT cart consisting only of a stamp without simple transfers failed to complete.

### Category
application bug

### Recommended action
Verify stamp-only payment execution pathways.

---

# 18. Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Single payment with multiple transfers and stamps failed to reach success status.

### Category
application bug

### Recommended action
Inspect single RPT handling logic for multiple stamps and transfers.

---

# 19. Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Single payment with four transfers failed to complete the receipt process.

### Category
application bug

### Recommended action
Review transfer processing limits for single RPT requests.

---

# 20. Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con two versamenti e nessuna marca da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
```
### Root cause
Single payment with two transfers failed to complete successfully.

### Category
application bug

### Recommended action
Check basic single RPT execution flow and event generation.

---

## Cross-suite correlation

- **WISP Suite Systemic Failure**: The WISP suite exhibits widespread failures across almost all transaction types (carts, single RPTs, multi-beneficiary, GPD integrations, stamps), consistently failing to record `RT_SEND_SUCCESS` business process events. This points to a core environment or backend integration breakdown affecting event publishing or payment finalization across the entire WISP service.
- **Checkout UI / Environment Stability**: Failures in the Checkout suite are split between environment timeout issues loading specific PSP configurations and application assertion mismatches on error modal headers.