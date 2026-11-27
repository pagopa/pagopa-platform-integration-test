## Suite: checkout

# 1. Inserimento dati - errori - indirizzo email diverso da ripeti
- **status**: broken
- **fullName**: `Validazione sintattica dei campi: Inserimento dati - errori - indirizzo email diverso da ripeti`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 85, in __exit__
    self._event.value
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 59, in value
    raise exception
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 264, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The test expected page navigation upon clicking a button, but no navigation occurred within 15 seconds due to form validation blocking submission.

### Category
flaky

### Recommended action
Update test step logic to avoid expecting page navigation when submitting forms with invalid inputs.

---

# 2. Inserimento dati - errori -  Inserimento codice avviso errato -- @1.3
- **status**: broken
- **fullName**: `Validazione sintattica dei campi: Inserimento dati - errori -  Inserimento codice avviso errato`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 85, in __exit__
    self._event.value
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 59, in value
    raise exception
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 264, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Form validation error prevented page navigation, causing Playwright navigation waiter to hit the 15-second timeout.

### Category
flaky

### Recommended action
Refactor the step definition to expect inline validation messages rather than page navigation.

---

# 3. Inserimento dati - errori -  Click sul tasto continua con campo non compilato -- @1.1
- **status**: broken
- **fullName**: `Validazione sintattica dei campi: Inserimento dati - errori -  Click sul tasto continua con campo non compilato`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 85, in __exit__
    self._event.value
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 59, in value
    raise exception
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 264, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Clicking continue with unfulfilled input fields prevented page navigation, leading to navigation timeout.

### Category
flaky

### Recommended action
Remove navigation wait guard for negative validation scenarios.

---

# 4. Inserimento dati - errori -  Inserimento indirizzo email non valido -- @1.3
- **status**: broken
- **fullName**: `Validazione sintattica dei campi: Inserimento dati - errori -  Inserimento indirizzo email non valido`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 85, in __exit__
    self._event.value
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 59, in value
    raise exception
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 264, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Client-side email validation prevented form submission, triggering a Playwright `TimeoutError` waiting for navigation.

### Category
flaky

### Recommended action
Adjust step definition to assert validation UI states instead of page navigation.

---

# 5. Inserimento dati - errori -  Inserimento CF ente errato -- @1.2
- **status**: broken
- **fullName**: `Validazione sintattica dei campi: Inserimento dati - errori -  Inserimento CF ente errato`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 85, in __exit__
    self._event.value
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 59, in value
    raise exception
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 264, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Invalid fiscal code input triggered client validation preventing navigation, timing out the navigation expectation.

### Category
flaky

### Recommended action
Fix test assertions to check error messages without waiting for page load navigation.

---

# 6. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
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
Element `#psp-radio-PPAYITR1XXX` did not appear on the PSP list page within 5000 ms, likely due to slow PSP list loading or missing data in UAT.

### Category
environment

### Recommended action
Verify PSP service availability and configuration for Postepay (`PPAYITR1XXX`) in UAT environment and increase locator timeout if necessary.

---

# 7. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento: Un pagamento con configurazione carta "Postepay" viene completato con successo`
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
Element `#psp-radio-PPAYITR1XXX` failed to render within the 5-second timeout window during PSP selection.

### Category
environment

### Recommended action
Check UAT environment latency and backend availability for retrieving PSP choices.

---

# 8. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
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
The application returned a generic creditor entity failure modal message instead of the specific unknown payment error message (`PAA_PAGAMENTO_SCONOSCIUTO`).

### Category
application bug

### Recommended action
Investigate mock server or downstream creditor service responses for the `30240*` notice code range to return the expected error code.

---

## Common patterns
- **Incorrect Navigation Expectation in Form Validation Tests**: Tests 1-5 fail due to `page.expect_navigation` timing out when invalid inputs prevent navigation.
- **PSP Element Visibility Timeouts**: Tests 6-7 fail because locator `#psp-radio-PPAYITR1XXX` is not found within 5 seconds.


## Suite: fdr3

Execution completed successfully with no test failures detected; confirm no tests were skipped during the run.


## Suite: wisp

# 1. L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 197, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 926, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        f'There are not events with business process {business_process}.')
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
The event bus or event store did not record any event with business process `receipt-ok` and status `RT_SEND_SUCCESS`.

### Category
application bug

### Recommended action
Inspect event processing pipelines and receipt generation services to verify why `receipt-ok` events are not generated or published.

---

# 2. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 926, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        f'There are not events with business process {business_process}.')
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Missing `receipt-ok` event with `RT_SEND_SUCCESS` status after payment completion.

### Category
application bug

### Recommended action
Verify downstream receipt processing and asynchronous event propagation in the WISP workflow.

---

# 3. Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 926, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        f'There are not events with business process {business_process}.')
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
`receipt-ok` event was not published or registered in step `check_wisp_session_timers_del_and_rts_were_sent`.

### Category
application bug

### Recommended action
Check RT (Ricevuta Telematica) transmission components to ensure receipt sending triggers properly.

---

# 4. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 197, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 926, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        f'There are not events with business process {business_process}.')
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
System failed to emit `receipt-ok` event upon successful retry of payment closure.

### Category
application bug

### Recommended action
Investigate retry flow handling in WISP backend to ensure receipts are produced on secondary payment attempts.

---

# 5. Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 926, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        f'There are not events with business process {business_process}.')
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Missing `receipt-ok` event with `RT_SEND_SUCCESS` status across payment scenarios involving revenue stamps (marche da bollo).

### Category
application bug

### Recommended action
Debug event streaming or polling mechanism in test framework and verify RT receipt generation service logs.

---

## Common patterns
- **Systematic Absence of Receipt Events (`receipt-ok`)**: All 5 failures in the `wisp` suite share the exact same assertion error (`There are not events with business process receipt-ok.`). This points to a suite-wide integration failure where receipt processing or event notification delivery is completely failing or delayed across WISP workflows.


## Cross-suite correlation

### Shared Failure Patterns & System-wide Dependencies
1. **Asynchronous Event and Notification Breakdown**:
   - **WISP Suite**: 100% of failures stem from missing `receipt-ok` events with status `RT_SEND_SUCCESS`.
   - **Checkout Suite**: Errors related to navigation timeouts and unexpected error modals (`L'Ente Creditore sta avendo problemi nella risposta`).
   - **Correlation**: Potential degradation or latency in downstream/async dependencies (such as event streaming, receipt delivery services, or mock API responses in the UAT environment) affecting both UI flow conclusions and backend validation steps.

2. **Test Automation & Step Implementation Flaws**:
   - In the **Checkout** suite, invalid form input tests fail due to rigid step logic (`page.expect_navigation`) waiting for page loads that are intentionally blocked by client-side validation.

### Recommended Actions Summary
1. **Investigate Backend Receipt & Event Services**:
   - Priority 1: Check the UAT event handler/bus service responsible for producing `receipt-ok` events (`RT_SEND_SUCCESS`) in the WISP workflow.
2. **Standardize Playwright Step Guardrails**:
   - Refactor UI test steps in `checkout` for form validation to check element visibility/error text directly instead of wrapping click actions inside `expect_navigation`.
3. **Environment and Mock Data Verification**:
   - Audit PSP availability (`#psp-radio-PPAYITR1XXX`) and response behavior for special notice ranges (`30240*`) in the UAT environment.