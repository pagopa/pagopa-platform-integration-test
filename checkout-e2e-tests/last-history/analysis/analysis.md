## Suite: checkout

# 1. Inserimento dati - errori -  Inserimento indirizzo email non valido -- @1.2
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
The test waited for a page navigation event upon clicking a button during validation error scenarios, but no navigation occurred within 15 seconds.

### Category
flaky

### Recommended action
Review `back_navigation.py` to ensure navigation expectation (`expect_navigation`) is not wrapped around clicks that trigger client-side validation without changing pages.

---

# 2. Inserimento dati - errori -  Inserimento CF ente errato -- @1.3
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
Navigation event timeout when submitting invalid CF data where form validation prevents page navigation.

### Category
flaky

### Recommended action
Update step implementation to avoid expecting page navigation on inline form field validation steps.

---

# 3. Inserimento dati - errori -  Inserimento codice avviso errato -- @1.1
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
Navigation event timeout when submitting invalid payment notice code, as the UI stays on the same page displaying field errors.

### Category
flaky

### Recommended action
Remove mandatory page navigation expectation for validation error trigger steps.

---

# 4. Inserimento dati - errori -  Click sul tasto continua con campo non compilato -- @1.2
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
Navigation event timeout when clicking continue with unfulfilled fields.

### Category
flaky

### Recommended action
Condition navigation check on expected application state rather than enforcing navigation timeout on invalid form submission.

---

# 5. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
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
The PSP option `#psp-radio-PPAYITR1XXX` was not found or visible on the PSP selection page within 5000ms.

### Category
test data

### Recommended action
Verify if PSP `PPAYITR1XXX` is active and available in the UAT environment PSP list configuration.

---

# 6. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento: Un pagamento con configurazione carta "Postepay" viene completato con successo`
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
The requested PSP (`PPAYITR1XXX`) radio button element did not render on the UAT PSP list page within the allowed timeout.

### Category
test data

### Recommended action
Check UAT environment configuration for Postepay PSP availability or update test metadata if the PSP ID has changed.

---

# 7. Inserimento dati - errori - indirizzo email diverso da ripeti
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
Timeout waiting for page navigation that never fires when email confirmation field validation fails.

### Category
flaky

### Recommended action
Refactor `step_click_button` in `back_navigation.py` to only expect navigation when valid input triggers actual page routing.

---

# 8. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
Unexpected error modal title returned; backend/mock returned a connectivity issue message instead of the expected unknown payment error message (`PAA_PAGAMENTO_SCONOSCIUTO`).

### Category
application bug

### Recommended action
Investigate mock/backend handling for invalid notice code ranges to ensure `PAA_PAGAMENTO_SCONOSCIUTO` error mapping is correct.

---

## Common patterns
- **Unnecessary Navigation Expectation in Form Validation**: Tests #1, #2, #3, #4, and #7 fail with a Playwright `TimeoutError` waiting for navigation during validation steps. This indicates test logic issues where form submit actions expect page reloads even when client validation prevents page transitions.
- **Missing PSP in UAT Environment**: Tests #5 and #6 fail due to missing target element `#psp-radio-PPAYITR1XXX` on the PSP selection screen.

---

## Cross-suite correlation
Only one test suite (`checkout`) was evaluated in this report run. Primary issues stem from:
1. Test framework automation patterns expecting navigation on static validation steps.
2. Missing test data / environment setup for PSP `PPAYITR1XXX`.
3. Application error message discrepancy for invalid payment notice codes.