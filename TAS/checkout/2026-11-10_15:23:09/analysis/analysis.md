# 1. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
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
The "Indietro" (Back) button locator timed out (5s) on the root URL (`/`), indicating navigation failed to reach or render the step containing the back button.

### Category
application bug

### Recommended action
Verify navigation flow when `enablePspPage=true` to ensure the back button renders properly and URL transitions occur as expected.

---

# 2. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato with successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 30000ms exceeded. Call log: waiting for locator("#frame_CARD_NUMBER") to be visible
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
```
### Root cause
The payment gateway iframe (`#frame_CARD_NUMBER`) from Nexi/Wordline loaded in a hidden state and exceeded the 30-second visibility timeout.

### Category
environment

### Recommended action
Investigate third-party payment gateway integration (Nexi/Wordline staging service) to ensure card iframe renders visibly in test environment.

---

# 3. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 30000ms exceeded. Call log: waiting for locator("#frame_CARD_NUMBER") to be visible
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
```
### Root cause
The payment gateway iframe (`#frame_CARD_NUMBER`) failed to become visible within 30 seconds during Postepay payment processing.

### Category
environment

### Recommended action
Check external payment gateway service status and iframe initialization logic for Postepay configuration.

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
The application returned a generic creditor error modal header instead of the specific unknown notice error message (`PAA_PAGAMENTO_SCONOSCIUTO`).

### Category
application bug

### Recommended action
Review error handling logic for invalid notice codes in the specified range to map mock backend responses to the correct modal message.

---

# 5. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
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
The "Indietro" button locator timed out on the base URL (`/`), indicating navigation back from `/scegli-metodo` failed to render expected UI components.

### Category
application bug

### Recommended action
Inspect linear navigation state handling when `enablePspPage=true` and saved wallets are present to ensure UI control rendering.

---

# 6. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The specific PSP selection radio button (`#psp-radio-PPAYITR1XXX`) was not found or failed to load within 5 seconds on the `/lista-psp` page.

### Category
flaky

### Recommended action
Verify if PSP list loading is asynchronous/slow and ensure appropriate wait strategies or test data availability for `PPAYITR1XXX`.

---

## Common patterns
- **Payment Gateway Frame Loading Issues**: Failures #2 and #3 share identical 30-second timeouts waiting for `#frame_CARD_NUMBER` iframe visibility, pointing to downstream issues with third-party iframe rendering (Nexi/Wordline).
- **Back Navigation Failures in PSP Flow**: Failures #1 and #5 fail due to locator timeouts for the `Indietro` button while redirected to the root URL (`https://dev.checkout.pagopa.it/`), indicating a failure in preserving session context or state under `enablePspPage=true`.