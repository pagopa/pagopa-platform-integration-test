# 1. Logout SPID completato con successo
- **status**: broken
- **fullName**: `Flusso di accesso con SPID: Logout SPID completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Page.wait_for_selector: Timeout 80000ms exceeded.
Call log:
  - waiting for locator("form#login-form") to be visible
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/spid_auth.py", line 13, in step_login_with_spid
    step_click_login_button(context)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/spid_auth.py", line 30, in step_click_login_button
```
### Root cause
The test timed out after 80 seconds waiting for the login form locator (`form#login-form`), indicating the SPID IDP provider mock page did not load.

### Category
environment

### Recommended action
Verify the availability and response times of the mock SPID Identity Provider environment used during E2E test execution.

---

# 2. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 124, in locate_and_click
```
### Root cause
The PSP radio option `#psp-radio-PPAYITR1XXX` was not found on the PSP list page within the 5-second timeout window.

### Category
test data

### Recommended action
Ensure that PSP `PPAYITR1XXX` (Postepay) is properly enabled and returned by the UAT list-psp service for this payment scenario.

---

# 3. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Page.wait_for_selector: Timeout 80000ms exceeded.
Call log:
  - waiting for locator("form#login-form") to be visible
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/checkout_npg_auth.py", line 14, in step_impl
    step_click_login_button(context)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/spid_auth.py", line 30, in step_click_login_button
```
### Root cause
Timeout exceeding 80 seconds when waiting for `form#login-form` during authenticated checkout via SPID.

### Category
environment

### Recommended action
Check SPID mock service responsiveness and network latency between Playwright runners and the authentication endpoint.

---

# 4. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The system displayed a generic Creditor Institution error message instead of the specific 'unknown notice' error modal header.

### Category
application bug

### Recommended action
Fix backend error handling logic for invalid notice codes in range 302400000000000000-302409999999999999 to correctly return `PAA_PAGAMENTO_SCONOSCIUTO`.

---

# 5. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Page.wait_for_selector: Timeout 80000ms exceeded.
Call log:
  - waiting for locator("form#login-form") to be visible
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/checkout_npg_auth.py", line 14, in step_impl
    step_click_login_button(context)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/spid_auth.py", line 30, in step_click_login_button
```
### Root cause
Timeout exceeding 80 seconds when waiting for `form#login-form` during authenticated checkout via SPID.

### Category
environment

### Recommended action
Verify health and status of SPID IDP login service in test environment.

---

# 6. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Page.wait_for_selector: Timeout 80000ms exceeded.
Call log:
  - waiting for locator("form#login-form") to be visible
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/checkout_npg_auth.py", line 14, in step_impl
    step_click_login_button(context)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/spid_auth.py", line 30, in step_click_login_button
```
### Root cause
Timeout exceeding 80 seconds when waiting for `form#login-form` during authenticated checkout via SPID.

### Category
environment

### Recommended action
Investigate mock SPID provider container health in UAT pipeline execution.

---

# 7. Accesso SPID completato con successo
- **status**: broken
- **fullName**: `Flusso di accesso con SPID: Accesso SPID completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Page.wait_for_selector: Timeout 80000ms exceeded.
Call log:
  - waiting for locator("form#login-form") to be visible
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/spid_auth.py", line 30, in step_click_login_button
    perform_login(page)
    ~~~~~~~~~~~~~^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 72, in perform_login
```
### Root cause
Timeout exceeding 80 seconds waiting for `form#login-form` to appear on SPID authentication page.

### Category
environment

### Recommended action
Restart or inspect SPID authentication mock service used during test runs.

---

## Common patterns

1. **SPID Service Unavailability / Environmental Failure**:
   5 out of 7 test failures (#1, #3, #5, #6, #7) failed with the exact same error: `playwright._impl._errors.TimeoutError: Page.wait_for_selector: Timeout 80000ms exceeded` waiting for locator `form#login-form`. This strongly indicates a service outage or high latency in the SPID mock provider environment rather than an application defect.

2. **Error Handling Logic Defects**:
   Failure #4 highlights a functional application bug where backend status mapping for notice code range `302400000000000000-302409999999999999` returns a generic creditor failure modal instead of `PAA_PAGAMENTO_SCONOSCIUTO`.