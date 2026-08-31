# 1. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
The error modal header displayed a generic creditor institution error instead of the specific unknown payment notice error message.

### Category
application bug

### Recommended action
Verify if the application copy changed or if the backend returned the wrong error code response for invalid notice codes in this range.

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
The SPID identity provider login form (`form#login-form`) failed to load or become visible within the 80-second timeout.

### Category
environment

### Recommended action
Check the availability and response times of the SPID mock/stub provider service in the test environment.

---

# 3. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
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
    perform_login(page)
```

### Root cause
Authenticated checkout flow failed during SPID login step due to timeout waiting for `form#login-form`.

### Category
environment

### Recommended action
Ensure the SPID authentication service is accessible and stable before running authenticated checkout integration tests.

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
The radio button locator for Postepay PSP (`#psp-radio-PPAYITR1XXX`) was not found on the PSP list page within 5 seconds.

### Category
test data

### Recommended action
Verify that the PSP `PPAYITR1XXX` is active and available in the UAT configuration for the payment notice being processed.

---

# 5. Logout SPID completato con successo
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
    perform_login(page)
```

### Root cause
Prerequisite SPID login failed due to an 80-second timeout waiting for `form#login-form` to appear.

### Category
environment

### Recommended action
Verify SPID test IdP uptime and network connectivity in the UAT integration environment.

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
    perform_login(page)
```

### Root cause
Authenticated Postepay checkout test failed because SPID identity provider login page (`form#login-form`) timed out.

### Category
environment

### Recommended action
Investigate SPID IdP mock stability and responsiveness during integration test execution.

---

# 7. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
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
    perform_login(page)
```

### Root cause
Authenticated Worldpay payment test timed out waiting 80 seconds for SPID login form (`form#login-form`).

### Category
environment

### Recommended action
Ensure SPID authentication mock is operational prior to initiating test suite execution.

---

## Common patterns
- **SPID Provider Outage / Unresponsiveness (Environment Issue)**: 5 out of 7 failures (#2, #3, #5, #6, #7) failed with an identical `TimeoutError: Page.wait_for_selector: Timeout 80000ms exceeded` waiting for `locator("form#login-form")`. This indicates that the SPID Identity Provider endpoint/mock was unavailable or unresponsive throughout the test run, cascading failures across all authenticated checkout scenarios.