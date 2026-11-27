## Suite: checkout

# 1. Inserimento dati - errori -  Inserimento CF ente errato -- @1.3
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
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
```
### Root cause
The test expects a page navigation after clicking a button, but no navigation occurs due to syntax validation errors blocking form submission.

### Category
flaky

### Recommended action
Update step definition to check for UI validation errors instead of expecting page navigation.

---

# 2. Inserimento dati - errori -  Click sul tasto continua con campo non compilato -- @1.3
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
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
```
### Root cause
The test step waits for page navigation when clicking "continua" with empty fields, but form validation prevents navigation.

### Category
flaky

### Recommended action
Remove navigation assertion for error scenarios and assert field error messages directly.

---

# 3. Inserimento dati - errori -  Inserimento codice avviso errato -- @1.3
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
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
```
### Root cause
Step definition incorrectly uses `expect_navigation` during invalid input validation handling where page load does not trigger.

### Category
flaky

### Recommended action
Refactor `back_navigation.py` step implementation to handle non-navigating button clicks gracefully.

---

# 4. Inserimento dati - errori - indirizzo email diverso da ripeti
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
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
```
### Root cause
Mismatching email inputs trigger client-side validation, preventing navigation and timing out the navigation listener.

### Category
flaky

### Recommended action
Remove navigation wait block for mismatch email validation scenario steps.

---

# 5. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Il pagamento non è andato a buon fine'
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
Wordline gateway payment authorization failed during processing on the backend/gateway side.

### Category
application bug

### Recommended action
Investigate backend application logs for Wordline NPG integration failures.

---

# 6. Inserimento dati - errori -  Inserimento indirizzo email non valido -- @1.2
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
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
```
### Root cause
Invalid email format keeps user on same page, timing out navigation expectation in test script.

### Category
flaky

### Recommended action
Adjust step definition logic to avoid calling `expect_navigation` on form validation failures.

---

# 7. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Timeout 80000ms exceeded.
- **trace**:
```
[... earlier frames omitted ...]
    page.wait_for_load_state("networkidle")
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 9875, in wait_for_load_state
    self._sync(
        self._impl_obj.wait_for_load_state(
            state=state, timeout=to_milliseconds(timeout)
```
### Root cause
Network idle wait timed out due to background long-polling requests or slow Worldpay gateway response.

### Category
environment

### Recommended action
Replace `wait_for_load_state("networkidle")` with explicit DOM element visibility waits.

---

# 8. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento: Un pagamento con configurazione carta "Postepay" viene completato con successo`
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
```
### Root cause
Postepay PSP (`PPAYITR1XXX`) radio option was missing from the PSP selection list in UAT environment.

### Category
test data

### Recommended action
Verify PSP configuration and availability for `PPAYITR1XXX` in UAT checkout configuration.

---

# 9. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
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
Backend returned creditor institution error response instead of expected payment unknown status.

### Category
application bug

### Recommended action
Check mock backend response mapping for invalid notice code interval 30240.

---

# 10. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
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
```
### Root cause
Postepay PSP (`PPAYITR1XXX`) is not rendered on the PSP choice list during authenticated checkout.

### Category
test data

### Recommended action
Ensure Postepay PSP is enabled in the catalog for authenticated user checkout workflows.

---

## Common patterns
- **Invalid expectation of page navigation on form validation errors**: Multiple test scenarios (#1, #2, #3, #4, #6) fail because steps use `page.expect_navigation()` during invalid input validation checks, where the application intentionally stays on page.
- **Missing PSP in test environment**: Scenarios #8 and #10 fail due to missing Postepay element locator `#psp-radio-PPAYITR1XXX` on UAT environment.

## Cross-suite correlation

All reported failures stem from the single suite execution (`checkout`).

### Identified Cross-Pattern Summaries & Recommended Actions:
1. **Flaky Test Script Assertions (Navigation Timeout on Validation Errors)**
   - *Impact*: 5 scenarios broken (#1, #2, #3, #4, #6).
   - *Root cause*: Test scripts incorrectly wrap button actions in `expect_navigation()` for negative/validation test cases.
   - *Recommended action*: Refactor `src/e2e/checkout/steps/back_navigation.py` to decouple action triggers from page navigation context for error validation steps.

2. **Environment Data / Configuration Issues (Missing PSP Option)**
   - *Impact*: 2 scenarios broken (#8, #10).
   - *Root cause*: Locator `#psp-radio-PPAYITR1XXX` unavailable on `uat.checkout.pagopa.it`.
   - *Recommended action*: Ensure Postepay PSP (`PPAYITR1XXX`) is seeded and active in the UAT payment provider registry.

3. **Backend Service Integration / Application Bugs**
   - *Impact*: 2 scenarios failed (#5, #9).
   - *Root cause*: Payment authorization failure for Wordline (#5) and incorrect error modal header mapping for invalid notice code (#9).
   - *Recommended action*: Escalate backend payment activation services and error mapping logic to application developers.