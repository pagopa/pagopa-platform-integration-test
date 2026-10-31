## Suite: checkout

# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
```
### Root cause
Playwright timed out after 5 seconds waiting for selector `#psp-radio-PPAYITR1XXX` on the UAT PSP selection page.

### Category
environment

### Recommended action
Verify if PSP `PPAYITR1XXX` (Postepay) is active and available in the UAT environment PSP catalog configuration.

---

# 2. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
```
### Root cause
The element `#psp-radio-PPAYITR1XXX` was not visible within 5000 ms during authenticated checkout on UAT.

### Category
environment

### Recommended action
Ensure PSP `PPAYITR1XXX` is active for authenticated flows in UAT environment settings.

---

# 3. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The application rendered a generic Creditor Institution error header instead of the expected unknown notice header.

### Category
application bug

### Recommended action
Inspect error response mapping in Checkout backend for `PAA_PAGAMENTO_SCONOSCIUTO` within notice range `302400000000000000-302409999999999999`.

---

# 4. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `features.checkout_npg.Attivazione pagamento Checkout.Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1`
- **message**: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
Failing step: E L'utente seleziona il PSP con id "PPAYITR1XXX" ... failed in 5.069s
Location: src/e2e/checkout/features/checkout_npg.feature:35
Traceback (most recent call last):
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 93, in locate_and_click
    to_click.wait_for(state="visible", timeout=timeout)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
```
### Root cause
Playwright step failed to find locator `#psp-radio-PPAYITR1XXX` on the PSP list view.

### Category
environment

### Recommended action
Verify UAT PSP availability and card configuration for Postepay (`PPAYITR1XXX`).

---

# 5. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `features.checkout_npg.Attivazione pagamento Checkout.Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1`
- **message**: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
Failing step: E L'intestazione della modale di errore contiene "Non riusciamo a trovare l’avviso" ... failed in 0.013s
Location: src/e2e/checkout/features/checkout_npg.feature:57
Assertion Failed: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
```
### Root cause
Error modal text mismatch when triggering payment activation with invalid notice code in range `302400000000000000-302409999999999999`.

### Category
application bug

### Recommended action
Fix error translation logic for notice range validation in Checkout frontend/backend error handler.

---

# 6. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `features.checkout_npg_auth.Attivazione pagamento Checkout autenticato.Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1`
- **message**: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
Failing step: E L'utente seleziona il PSP con id "PPAYITR1XXX" ... failed in 5.061s
Location: src/e2e/checkout/features/checkout_npg_auth.feature:36
Traceback (most recent call last):
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 93, in locate_and_click
    to_click.wait_for(state="visible", timeout=timeout)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
```
### Root cause
Locator `#psp-radio-PPAYITR1XXX` timed out waiting to become visible during Postepay PSP selection.

### Category
environment

### Recommended action
Verify PSP `PPAYITR1XXX` status and presence on `https://uat.checkout.pagopa.it/lista-psp`.

---

## Common patterns

1. **PSP selection timeouts (`#psp-radio-PPAYITR1XXX`)**: 4 out of 6 failures are caused by missing or unrendered Postepay PSP option in UAT environment.
2. **Error modal messaging mismatch (`PAA_PAGAMENTO_SCONOSCIUTO`)**: 2 out of 6 failures show application returning generic Creditor Institution error instead of notice search failure message.

---

## Suite: fdr3

Execution completed with no test failures found in the FDR-3 suite; please verify that all tests were executed and none were unintentionally skipped.

---

## Suite: wisp

# 1. L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
```
### Root cause
No event with business process `receipt-ok` and status `RT_SEND_SUCCESS` was logged in RE following cart payment execution.

### Category
application bug

### Recommended action
Investigate RT receipt generation and transmission pipeline in WISP / Nodo for multi-RPT carts with stamp duty.

---

# 2. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
```
### Root cause
Missing `receipt-ok` RE event during receipt generation check.

### Category
application bug

### Recommended action
Check receipt dispatch logs in Nodo to ensure RT delivery succeeds for single RPT with stamp duty.

---

# 3. L'utente paga un carrello con singola RPT con quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con quattro versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
```
### Root cause
`receipt-ok` event with status `RT_SEND_SUCCESS` was not registered in RE logs.

### Category
application bug

### Recommended action
Verify RT processing logic when handling single RPTs containing multi-transfers (4 payments).

---

# 4. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
```
### Root cause
No `receipt-ok` RE event recorded after checkout payment completion for existing GPD payment position.

### Category
application bug

### Recommended action
Audit receipt publication workflow for payment positions initiated via `nodoInviaCarrelloRPT` backed by GPD.

---

# 5. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_existingPaymentPosition.L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT.L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 37.553s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_existingPaymentPosition.feature:19
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f5c31634fe0>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '348179342807722901', 'state': 'OK'}]}
```
### Root cause
Assertion failed after waiting 32+ seconds for `receipt-ok` RE event generation.

### Category
application bug

### Recommended action
Verify backend event emission for `receipt-ok` during Checkout completion steps.

---

# 6. L'utente paga un carrello con singola RPT con quattro versamenti
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_noStamp.L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT.L'utente paga un carrello con singola RPT con quattro versamenti`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 36.420s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_noStamp.feature:51
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f5c316d1ad0>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179342868076806', 'state': 'OK'}]}
```
### Root cause
`receipt-ok` business process event was not found in RE events query.

### Category
application bug

### Recommended action
Investigate whether RT generation or RE event ingestion delayed/failed for multi-transfer RPT payments.

---

# 7. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_withStamp.L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT.L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 36.161s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_withStamp.feature:29
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f5c316d3830>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179342919213054', 'state': 'OK'}]}
```
### Root cause
Missing `receipt-ok` business process event in RE after payment redirect step.

### Category
application bug

### Recommended action
Inspect event log pipeline for single RPT + stamp duty payments on `nodoInviaCarrelloRPT`.

---

# 8. L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_withStamp.L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT.L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 38.318s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_withStamp.feature:52
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f5c316d51c0>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179342926982905', 'state': 'OK'}, {'fiscalCode': '15376371009', 'noticeNumber': '351179342926986743', 'state': 'OK'}]}
```
### Root cause
Missing `receipt-ok` event in RE for multi-RPT payment flow.

### Category
application bug

### Recommended action
Verify asynchronous receipt generation and event publication service for cart payments.

---

## Common patterns

1. **Systemic missing `receipt-ok` events in WISP**: All 8 failures across WISP share the exact same root cause (`There are not events with business process receipt-ok.`). Payments submitted via `nodoInviaCarrelloRPT` complete the HTTP flow, but the corresponding receipt event (`receipt-ok` with status `RT_SEND_SUCCESS`) is not generated or recorded in the RE log store.
2. **Cross-Suite Correlation**: WISP failures indicate issues downstream of Checkout completion (receipt handling / event emission), whereas Checkout suite failures stem from frontend PSP availability and invalid notice error code mappings.