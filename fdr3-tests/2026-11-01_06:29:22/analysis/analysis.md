## Suite: checkout

# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The locator `#psp-radio-PPAYITR1XXX` timed out after 5 seconds on the PSP selection page, indicating that Postepay PSP was not present or visible in the list.

### Category
environment

### Recommended action
Verify if the PSP `PPAYITR1XXX` is active and configured in the UAT environment dataset and check if UI render latency exceeds 5 seconds.

---

# 2. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
The application returned an Creditor Entity response error instead of the specific unknown payment error modal header (`PAA_PAGAMENTO_SCONOSCIUTO`).

### Category
application bug

### Recommended action
Investigate mock/backend response mapping for `PAA_PAGAMENTO_SCONOSCIUTO` to ensure the correct user-facing error message is rendered.

---

# 3. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Payment transaction remained in an asynchronous pending state ("Attendi la conferma del pagamento") without completing within the expected execution window.

### Category
flaky

### Recommended action
Increase polling wait time for payment status resolution or inspect Wordline gateway callback delays in UAT.

---

# 4. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
Element `#psp-radio-PPAYITR1XXX` was not visible on the PSP selection screen within 5000 ms.

### Category
environment

### Recommended action
Check whether PSP list rendering is delayed or if `PPAYITR1XXX` service is unavailable in UAT.

---

# 5. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `features.checkout_npg.Attivazione pagamento Checkout.Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1`
- **message**: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
Failing step: E L'utente seleziona il PSP con id "PPAYITR1XXX" ... failed in 5.066s
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
Playwright timed out waiting for element visibility of `#psp-radio-PPAYITR1XXX`.

### Category
environment

### Recommended action
Ensure the PSP selection endpoint returns consistent data for Postepay in test environments.

---

# 6. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `features.checkout_npg.Attivazione pagamento Checkout.Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2`
- **message**: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
Failing step: Allora Viene mostrato un messaggio di pagamento completato con successo ... failed in 91.547s
Location: src/e2e/checkout/features/checkout_npg.feature:38
Assertion Failed: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
```
### Root cause
Payment outcome was stuck in pending state after 91 seconds during Wordline card payment confirmation.

### Category
flaky

### Recommended action
Investigate Wordline async callback handling and extend explicit wait conditions for terminal status update.

---

# 7. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `features.checkout_npg.Attivazione pagamento Checkout.Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1`
- **message**: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
Failing step: E L'intestazione della modale di errore contiene "Non riusciamo a trovare l’avviso" ... failed in 0.016s
Location: src/e2e/checkout/features/checkout_npg.feature:57
Assertion Failed: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
```
### Root cause
Incorrect error modal content displayed when testing invalid notice code range `302400000000000000-302409999999999999`.

### Category
application bug

### Recommended action
Fix backend error handling logic for invalid notice code lookup to return `PAA_PAGAMENTO_SCONOSCIUTO` instead of generic EC failure.

---

# 8. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `features.checkout_npg_auth.Attivazione pagamento Checkout autenticato.Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1`
- **message**: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
Failing step: E L'utente seleziona il PSP con id "PPAYITR1XXX" ... failed in 5.060s
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
Timeout locating element `#psp-radio-PPAYITR1XXX` on the authenticated checkout flow.

### Category
environment

### Recommended action
Verify UAT PSP availability service and ensure `#psp-radio-PPAYITR1XXX` is populated in the DOM.

---

## Common patterns
- **Missing/Unavailable PSP Element (4 failures)**: All Postepay test variants failed due to timeout locating `#psp-radio-PPAYITR1XXX` on `https://uat.checkout.pagopa.it/lista-psp`.
- **Unexpected Error Modal Text (2 failures)**: Invalid notice range scenarios consistently received generic Creditor Entity failure modal instead of unknown notice modal.
- **Asynchronous Payment Settlement Delay (2 failures)**: Wordline card payments remained stuck at "Attendi la conferma del pagamento" state.


## Suite: fdr3

Execution of the FDR-3 suite was completed with zero test failures, and all configured tests ran to completion without being skipped.


## Suite: wisp

# 1. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
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
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Nodo Event Hub/RE events missing business process `receipt-ok` with status `RT_SEND_SUCCESS` after payment completion.

### Category
application bug

### Recommended action
Verify asynchronous receipt generation service (Nodo/GPD) and ensure RE event writer publishes `receipt-ok` events.

---

# 2. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo`
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
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Missing `receipt-ok` event in event store for single payment flow via `nodoInviaRPT`.

### Category
application bug

### Recommended action
Check RT transmission flow in Nodo to confirm why `RT_SEND_SUCCESS` status events were not registered.

---

# 3. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_existingPaymentPosition.L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT.L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 41.358s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_existingPaymentPosition.feature:19
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f58533e1260>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '348179351457034728', 'state': 'OK'}]}
```
### Root cause
Event verification failed after 20-second wait period because no `receipt-ok` event was produced.

### Category
application bug

### Recommended action
Investigate event ingestion pipeline for `nodoInviaCarrelloRPT` execution path.

---

# 4. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo
- **status**: failed
- **fullName**: `features.nodoInviaRPT.nodoInviaRPT_noStamp.Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT.Utente paga un pagamento singolo con un versamento e nessuna marca da bollo`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 39.051s
Location: src/integration/wisp/features/nodoInviaRPT/nodoInviaRPT_noStamp.feature:17
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f58534a6b10>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179351625680380', 'state': 'OK'}]}
```
### Root cause
Event store check failed to find `receipt-ok` event following `nodoInviaRPT` payment execution.

### Category
application bug

### Recommended action
Inspect downstream receipt generation and RE log emission for single RPT payments.

---

## Common patterns
- **Missing RE Receipt Event (`receipt-ok`)**: 100% of failures in the WISP suite failed on the assertion `There are not events with business process receipt-ok.` during the receipt verification step across both `nodoInviaCarrelloRPT` and `nodoInviaRPT` features.