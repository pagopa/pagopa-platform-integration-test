# 1. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
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
```
### Root cause
The back button (`Indietro`) was not rendered within 5000ms, possibly due to unexpected redirection back to the root URL (`https://dev.checkout.pagopa.it/`).

### Category
application bug

### Recommended action
Verify back navigation state preservation when `enablePspPage=true` is enabled to ensure the back button renders properly.

---

# 2. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded. Call log: - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
[... earlier frames omitted ...]
        state="visible", timeout=120000
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
```
### Root cause
Payment completion timed out after 120 seconds while waiting for the final response page header (`#responsePageMessageTitle`), indicating a hang in Worldpay gateway processing.

### Category
environment

### Recommended action
Check the health and latency of the Worldpay sandbox/gateway backend integration.

---

# 3. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded. Call log: - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
[... earlier frames omitted ...]
        state="visible", timeout=120000
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
```
### Root cause
Payment completion timed out after 120 seconds waiting for `#responsePageMessageTitle`, indicating Wordline gateway backend unresponsiveness.

### Category
environment

### Recommended action
Inspect Wordline gateway mock/sandbox backend logs to determine why payment confirmation response was delayed or not dispatched.

---

# 4. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
```
### Root cause
PSP option `#psp-radio-PPAYITR1XXX` was missing from `/lista-psp` page within the 5000ms timeout window.

### Category
test data

### Recommended action
Verify if PSP `PPAYITR1XXX` is active and returned by the backend API in the dev environment test configuration.

---

# 5. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
```
### Root cause
Mismatch between expected error message header and the actual error header returned by the UI when handling `PAA_PAGAMENTO_SCONOSCIUTO`.

### Category
application bug

### Recommended action
Align UI copy mapping for error code `PAA_PAGAMENTO_SCONOSCIUTO` or update the step definition assertion if the modal text was intentionally changed.

---

# 6. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
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
```
### Root cause
The back button was missing because navigation unexpected redirected to root URL (`https://dev.checkout.pagopa.it/`).

### Category
application bug

### Recommended action
Ensure session state and page context are retained properly during back navigation from `/scegli-metodo`.

---

# 7. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BNLIITRR' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
Locator `#psp-radio-BNLIITRR` was not found on `/lista-psp` page, indicating the PSP option was missing or disabled for the user flow.

### Category
test data

### Recommended action
Verify configuration and availability of PSP `BNLIITRR` in dev environment for authenticated checkout flows.

---

# 8. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded. Call log: - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
[... earlier frames omitted ...]
        state="visible", timeout=120000
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
```
### Root cause
Payment completion timed out after 120 seconds waiting for `#responsePageMessageTitle` in authenticated Worldpay flow.

### Category
environment

### Recommended action
Check backend services responsible for payment outcome notifications from Worldpay integration.

---

# 9. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Timeout 80000ms exceeded.
- **trace**:
```
[... earlier frames omitted ...]
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 147, in step_fill_card_number
    page.wait_for_load_state("networkidle")
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
```
### Root cause
`wait_for_load_state("networkidle")` timed out after 80000ms due to continuous network activity or pending background HTTP requests during card entry.

### Category
flaky

### Recommended action
Replace `networkidle` wait strategy with explicit element availability checks to avoid test instability caused by background polling.

---

## Common patterns

1. **Payment Gateway Timeouts (`#responsePageMessageTitle`):** Multiple scenarios involving Worldpay and Wordline (Tests #2, #3, #8) failed after waiting 120 seconds for the completion response screen. This points to environment-level issues or slow response times in third-party gateway mocks/sandboxes.
2. **Missing PSP Options on `/lista-psp`:** Tests #4 and #7 failed because specific PSP radio locators (`#psp-radio-PPAYITR1XXX`, `#psp-radio-BNLIITRR`) were not rendered in time, indicating missing or misconfigured test data in the backend environment.
3. **Back Navigation / Route Loss:** Tests #1 and #6 timed out waiting for the `Indietro` button because the browser redirected unexpectedly to the root URL (`https://dev.checkout.pagopa.it/`), losing step context when `enablePspPage=true`.