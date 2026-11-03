# 1. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded.
Call log:
  - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
[... earlier frames omitted ...]
        state="visible", timeout=120000
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
```
### Root cause
Payment completion timed out after 120s waiting for the response page redirect/element `#responsePageMessageTitle`, likely due to NPG/Wordline gateway latency or non-response in dev environment.

### Category
environment

### Recommended action
Investigate NPG/Wordline payment gateway sandbox availability and response times; increase test timeout or handle gateway unavailability gracefully.

---

# 2. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded.
Call log:
  - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
[... earlier frames omitted ...]
        state="visible", timeout=120000
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
```
### Root cause
Payment completion timed out after 120s waiting for `#responsePageMessageTitle`, indicating Worldpay integration gateway slow response or failure to redirect back to Checkout.

### Category
environment

### Recommended action
Verify Worldpay sandbox environment health and check integration logs for missing redirect callbacks.

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
```
### Root cause
Mismatch in error handling; application displayed a generic Creditor Institution response error modal instead of the specific unknown payment notice error modal.

### Category
application bug

### Recommended action
Check backend mock/response mapping for notice code range `302400000000000000-302409999999999999` and update frontend modal logic or error code handling.

---

# 4. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 88, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
```
### Root cause
The "Indietro" (Back) button locator was not found within 5 seconds on page `https://dev.checkout.pagopa.it/`, likely because navigation landed on the root URL instead of `/inserisci-carta` or the button text changed.

### Category
application bug

### Recommended action
Verify client-side route redirection when `enablePspPage=true` and confirm the visibility and locator of the back button.

---

# 5. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded.
Call log:
  - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
[... earlier frames omitted ...]
        state="visible", timeout=120000
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
```
### Root cause
Unauthenticated Wordline flow timed out after 120s waiting for payment completion response screen `#responsePageMessageTitle`.

### Category
environment

### Recommended action
Check NPG Wordline gateway availability and mock responses in dev environment.

---

# 6. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded.
Call log:
  - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
[... earlier frames omitted ...]
        state="visible", timeout=120000
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
```
### Root cause
Authenticated Worldpay payment flow timed out after 120s waiting for response page `#responsePageMessageTitle`.

### Category
environment

### Recommended action
Inspect backend logs for Worldpay transaction completion callbacks to resolve gateway timeout issues.

---

# 7. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
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
```
### Root cause
The specific PSP element `#psp-radio-PPAYITR1XXX` for Postepay was not present or rendered in the PSP list within 5 seconds.

### Category
test data

### Recommended action
Ensure test environment PSP catalog returned by backend API contains active configuration for Postepay (`PPAYITR1XXX`).

---

# 8. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
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
```
### Root cause
Postepay PSP choice `#psp-radio-PPAYITR1XXX` missing from `/lista-psp` page in authenticated checkout context.

### Category
test data

### Recommended action
Verify PSP seeding and activation status for `PPAYITR1XXX` in the test database/environment API.

---

# 9. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 88, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
```
### Root cause
The back navigation step failed to locate `button:has-text('Indietro')` within 5s because browser URL unexpectedly redirected to root `https://dev.checkout.pagopa.it/` instead of staying on `/scegli-metodo`.

### Category
application bug

### Recommended action
Investigate navigation state management and session initialization when `enablePspPage=true` is set.

---

## Common patterns

- **Payment Gateway Timeouts (Environment):** 4 failures (#1, #2, #5, #6) were caused by a 120-second timeout waiting for `#responsePageMessageTitle` across Wordline and Worldpay card configurations. This points to external gateway unavailability or missing callbacks in the `dev` environment.
- **Missing PSP Options (Test Data):** 2 failures (#7, #8) were caused by missing `#psp-radio-PPAYITR1XXX` radio buttons on the `/lista-psp` page, indicating stale or missing PSP mock/configuration data for Postepay.
- **Navigation/Routing Issues (Application Bug):** 2 failures (#4, #9) failed because tests unexpectedly landed on the base URL (`https://dev.checkout.pagopa.it/`) without displaying the expected "Indietro" button during `enablePspPage=true` test flows.