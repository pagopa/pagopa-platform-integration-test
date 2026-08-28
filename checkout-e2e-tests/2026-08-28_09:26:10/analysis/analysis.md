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
The SPID authentication page failed to render `form#login-form` within the 80-second timeout window.

### Category
environment

### Recommended action
Verify availability and responsiveness of the SPID IDP mock service in the test environment.

---

# 2. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Il pagamento non è andato a buon fine'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Payment transaction via Wordline provider failed unexpectedly, returning an error message instead of the success confirmation.

### Category
application bug

### Recommended action
Inspect payment gateway integration logs for Wordline to identify why the payment processing failed.

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
SPID IDP login form (`form#login-form`) did not become visible within the 80-second timeout during authentication.

### Category
environment

### Recommended action
Check SPID IDP mock service status and network reachability in the UAT execution environment.

---

# 4. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The PSP radio element `#psp-radio-PPAYITR1XXX` for Postepay was not present on the PSP selection page.

### Category
test data

### Recommended action
Ensure Postepay PSP (`PPAYITR1XXX`) is enabled and available in the test environment configuration for the given notice/tenant.

---

# 5. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
The application rendered generic error header 'L’Ente Creditore sta avendo problemi nella risposta' instead of specific unknown payment error header 'Non riusciamo a trovare l’avviso'.

### Category
application bug

### Recommended action
Verify backend error mapping for `PAA_PAGAMENTO_SCONOSCIUTO` to ensure the correct error message code is propagated to frontend UI.

---

# 6. Accesso SPID completato con successo
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
SPID IDP login form (`form#login-form`) timed out after 80000ms waiting to become visible.

### Category
environment

### Recommended action
Investigate SPID authentication stub health and responsiveness in UAT.

---

# 7. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
SPID login form (`form#login-form`) failed to appear within 80 seconds during the authenticated checkout scenario.

### Category
environment

### Recommended action
Check UAT environment SPID mock availability and latency.

---

# 8. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
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
SPID provider login form (`form#login-form`) timed out after 80 seconds during authenticated checkout flow.

### Category
environment

### Recommended action
Verify SPID IDP stub responsiveness in UAT.

---

## Common patterns

1. **SPID Authentication Service Downtime/Timeout (5 of 8 failures)**:
   - Tests #1, #3, #6, #7, and #8 all timed out waiting 80,000ms for `locator("form#login-form")`. This indicates an outage or severe degradation of the SPID IDP mock provider in the UAT environment.

2. **Application Logic & Gateway Issues (2 of 8 failures)**:
   - Failure #2 failed during Wordline payment execution ("Il pagamento non è andato a buon fine"), pointing to potential gateway processing issues.
   - Failure #5 returned an incorrect error modal title (`L’Ente Creditore sta avendo problemi nella risposta` vs expected `Non riusciamo a trovare l’avviso`), indicating a misconfiguration in backend error handling.

3. **Missing PSP Option in Test Data (1 of 8 failures)**:
   - Failure #4 timed out locator `#psp-radio-PPAYITR1XXX`, likely due to missing configuration or disabling of Postepay in the PSP list for the test notice.