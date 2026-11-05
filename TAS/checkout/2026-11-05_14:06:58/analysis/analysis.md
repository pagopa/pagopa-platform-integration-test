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
The back button (`button:has-text('Indietro')`) could not be found within the 5-second timeout because the page redirected prematurely to the root URL (`/`) instead of remaining on `/scegli-metodo`.

### Category
application bug

### Recommended action
Investigate the navigation logic for back button handling on `/scegli-metodo` when `enablePspPage=true` to ensure user sessions do not redirect unexpectedly to root.

---

# 2. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
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
The 'Indietro' button was not located within 5000ms due to an unexpected redirect to the root landing page (`/`) while on `/inserisci-carta`.

### Category
application bug

### Recommended action
Verify back-navigation state retention on `/inserisci-carta` when `enablePspPage=true` to prevent improper root redirects.

---

# 3. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato with successo`
- **message**: playwright._impl._errors.TimeoutError: Timeout 80000ms exceeded.
- **trace**:
```
[... earlier frames omitted ...]
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 147, in step_fill_card_number
    page.wait_for_load_state("networkidle")
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 9117, in wait_for_load_state
```
### Root cause
The test timed out after 80 seconds waiting for `networkidle` state during card entry, likely due to persistent background polling or dynamic requests on the Wordline checkout page.

### Category
flaky

### Recommended action
Replace `page.wait_for_load_state("networkidle")` with explicit locator-based waits for specific UI elements or response listeners instead of relying on network idle states.

---

# 4. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
The backend returned a generic timeout/error response from the Creditor Institution (`PAA_UNREACHABLE` / response issues) instead of the domain-specific `PAA_PAGAMENTO_SCONOSCIUTO` error modal.

### Category
environment

### Recommended action
Check mock/stub backend services for the creditor institution in the DEV environment to ensure correct error code handling for invalid payment notices.

---

# 5. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The PSP element `#psp-radio-PPAYITR1XXX` for Postepay was missing from the `/lista-psp` selection list or failed to load within 5 seconds.

### Category
test data

### Recommended action
Verify if the PSP `PPAYITR1XXX` is active and returned by the backend configuration API in the DEV environment for non-authenticated flows.

---

# 6. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Il pagamento non è andato a buon fine'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
The payment attempt failed during authorization on the payment gateway side, resulting in an outcome message of 'Il pagamento non è andato a buon fine'.

### Category
environment

### Recommended action
Inspect payment gateway integration logs for Wordline in the DEV environment to check why transactions are failing authorization.

---

# 7. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The PSP input element `#psp-radio-PPAYITR1XXX` was missing from `/lista-psp` during the authenticated payment flow.

### Category
test data

### Recommended action
Ensure `PPAYITR1XXX` is available in the PSP catalog API response for authenticated user contexts in DEV environment setup.

---

## Common patterns

- **Linear Navigation / Session Eviction (Failures #1 & #2)**: Back-navigation steps are failing because the application redirects to the landing page (`https://dev.checkout.pagopa.it/`) unexpectedly, causing locator timeouts for the 'Indietro' button.
- **Missing PSP Options in DEV (Failures #5 & #7)**: Postepay (`PPAYITR1XXX`) radio buttons are consistently missing from the `/lista-psp` page across both authenticated and non-authenticated flows.
- **Wordline Integration Stability (Failures #3 & #6)**: Tests involving Wordline card processing suffer from backend authorization failures or hanging network calls (`networkidle` timeouts).