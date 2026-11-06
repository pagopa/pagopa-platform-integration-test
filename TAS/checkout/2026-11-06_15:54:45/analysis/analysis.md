# 1. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
The back button (`button:has-text('Indietro')`) was not found or visible within 5000ms because the browser redirected unexpectedly to the root URL (`https://dev.checkout.pagopa.it/`).

### Category
application bug

### Recommended action
Verify client-side routing and session state preservation when navigating backward from `/scegli-metodo` with `enablePspPage=true`.

---

# 2. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
The application displayed a generic backend error message instead of the specific modal header expected for `PAA_PAGAMENTO_SCONOSCIUTO`.

### Category
application bug

### Recommended action
Check backend error response mapping to ensure `PAA_PAGAMENTO_SCONOSCIUTO` translates to the user-facing modal header 'Non riusciamo a trovare l’avviso'.

---

# 3. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
The test attempted to click the back button while the application was prematurely redirected to the root URL (`https://dev.checkout.pagopa.it/`).

### Category
application bug

### Recommended action
Fix navigation handling when going back from `/inserisci-carta` under the `enablePspPage=true` flag.

---

# 4. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
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
Payment authorization via Wordline gateway timed out after 120 seconds without redirecting to the final status response page.

### Category
environment

### Recommended action
Investigate latency or connectivity issues with the Wordline payment gateway sandbox/environment integration.

---

# 5. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
The Postepay PSP option (`#psp-radio-PPAYITR1XXX`) was missing from the `/lista-psp` page element list.

### Category
test data

### Recommended action
Ensure the PSP `PPAYITR1XXX` is active and returned by the configuration/mock service in the target environment.

---

# 6. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
The test timed out locating `#psp-radio-PPAYITR1XXX` on `/lista-psp`, indicating the PSP was unavailable during selection.

### Category
test data

### Recommended action
Verify availability and activation status of the Postepay provider (`PPAYITR1XXX`) in the environment's PSP catalog.

---

# 7. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
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
The payment process timed out after 120 seconds while awaiting completion confirmation from the Worldpay gateway.

### Category
environment

### Recommended action
Check external network connectivity and webhook callback handling for the Worldpay gateway environment.

---

## Common patterns

- **Unexpected Fallback Redirects during Back Navigation (#1, #3):** Both back navigation tests failed because the page prematurely fell back to the root URL (`https://dev.checkout.pagopa.it/`), causing a timeout when looking for the "Indietro" button.
- **Missing PSP Options in UI (#5, #6):** Multiple tests targeting Postepay failed because `#psp-radio-PPAYITR1XXX` was not present on `/lista-psp`, indicating potential test data or feature-flag mismatch in the test environment.
- **Gateway Checkout Timeouts (#4, #7):** Third-party payment provider flows (Wordline and Worldpay) both hit a 120-second Playwright timeout waiting for `#responsePageMessageTitle`, suggesting backend/gateway integration delays.