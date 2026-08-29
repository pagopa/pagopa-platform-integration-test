# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The PSP option `#psp-radio-PPAYITR1XXX` was not visible on the PSP selection page within the 5-second timeout, likely due to slow rendering or missing PSP configuration.

### Category
flaky

### Recommended action
Increase the explicit timeout for PSP radio button selection and ensure PSP list API responses are ready before assertion.

---

# 2. Accesso SPID completato con successo
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
The SPID authentication service/mock failed to load the `form#login-form` page element within the 80-second timeout.

### Category
environment

### Recommended action
Verify health and availability of the SPID Identity Provider stub/environment in UAT.

---

# 3. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The authenticated payment flow blocked because the SPID login form (`form#login-form`) timed out while loading.

### Category
environment

### Recommended action
Check SPID auth service status in UAT and consider adding retry mechanisms for authenticating test sessions.

---

# 4. Logout SPID completato con successo
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
Prerequisite login step failed due to SPID login page (`form#login-form`) not rendering within 80 seconds.

### Category
environment

### Recommended action
Ensure SPID provider mock service is stable before running SPID lifecycle tests.

---

# 5. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
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
The authenticated payment setup timed out while waiting for `form#login-form` during SPID authentication.

### Category
environment

### Recommended action
Investigate latency/unavailability issues in the SPID login mock environment.

---

# 6. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
The backend returned a generic Creditor Entity communication error modal instead of the expected unknown payment error (`PAA_PAGAMENTO_SCONOSCIUTO`).

### Category
application bug

### Recommended action
Verify error mapping logic in the application when processing invalid notice codes in the specified range to ensure correct modal error copy is rendered.

---

# 7. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
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
SPID authentication step failed to load `form#login-form` within the 80,000 ms timeout window.

### Category
environment

### Recommended action
Restore connectivity and performance of the test SPID IDP mock service.

---

## Common patterns

- **SPID Authentication Service Outage (5/7 failures)**: Failures #2, #3, #4, #5, and #7 all failed with an identical 80-second Playwright timeout waiting for `locator("form#login-form")`. This indicates a major environment instability or outage with the SPID Identity Provider endpoint in the UAT test environment.
- **Incorrect Error Handling**: Failure #6 highlights an application response mismatch where the UI displays a generic creditor entity failure modal instead of the domain-specific unknown payment modal.