# 1. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
The application returned a generic creditor response error modal instead of the expected specific notice-not-found message for code PAA_PAGAMENTO_SCONOSCIUTO.

### Category
application bug

### Recommended action
Verify backend mapping for `PAA_PAGAMENTO_SCONOSCIUTO` error codes to ensure the correct user-facing modal header is rendered.

---

# 2. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded.
Call log:
  - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
    await self._channel.send(
        "waitForSelector", self._timeout, locals_to_params(locals())
    )
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
```
### Root cause
Payment completion timed out waiting for the final response page title element (`#responsePageMessageTitle`) after 120 seconds, likely due to slow or unhandled third-party gateway responses from Worldline.

### Category
environment

### Recommended action
Check backend logs and Worldline payment gateway integration/mock environment availability for hanging payment authorizations.

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
The test attempted to click the "Indietro" button while still on the root URL (`https://dev.checkout.pagopa.it/`) instead of the expected `/inserisci-carta` page, causing the locator to fail.

### Category
flaky

### Recommended action
Ensure proper page navigation waits/assertions exist before trying to click elements on sub-routes.

---

# 4. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The expected PSP option (`#psp-radio-PPAYITR1XXX`) was not present or visible on the `/lista-psp` page within the 5-second timeout.

### Category
test data

### Recommended action
Verify if `PPAYITR1XXX` is active and returned by the PSP configuration API for the test environment.

---

# 5. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded.
Call log:
  - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
    await self._channel.send(
        "waitForSelector", self._timeout, locals_to_params(locals())
    )
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
```
### Root cause
Payment transaction did not complete within 120 seconds waiting for `#responsePageMessageTitle` during a Worldpay test flow.

### Category
environment

### Recommended action
Inspect payment gateway downstream communication with Worldpay sandbox environments.

---

# 6. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
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
The test attempted to locate the back button before navigating away from the base checkout landing page.

### Category
flaky

### Recommended action
Add explicit assertions ensuring navigation to `/scegli-metodo` has completed prior to triggering back navigation actions.

---

# 7. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded.
Call log:
  - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
    await self._channel.send(
        "waitForSelector", self._timeout, locals_to_params(locals())
    )
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
```
### Root cause
Payment completion timed out waiting for `#responsePageMessageTitle` on non-authenticated Worldpay checkout.

### Category
environment

### Recommended action
Investigate connectivity issues and latency between Checkout backend services and Worldpay.

---

# 8. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The element `#psp-radio-PPAYITR1XXX` was missing from the `/lista-psp` page within 5000 ms.

### Category
test data

### Recommended action
Ensure the test environment seed data includes `PPAYITR1XXX` in the available PSP list for card payments.

---

# 9. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded.
Call log:
  - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
    await self._channel.send(
        "waitForSelector", self._timeout, locals_to_params(locals())
    )
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
```
### Root cause
Payment flow timed out after 120 seconds waiting for the confirmation title element (`#responsePageMessageTitle`).

### Category
environment

### Recommended action
Verify Wordline payment gateway mock/sandbox reliability in the dev environment.

---

## Common patterns

- **Payment Gateway Timed Out (Environment)**: Tests 2, 5, 7, and 9 all failed with a 120-second timeout waiting for `#responsePageMessageTitle` across Worldline and Worldpay gateways, pointing to backend processing or third-party integration hangs in the `dev` environment.
- **Missing Test Data (Test Data)**: Tests 4 and 8 both failed with a 5-second timeout on locator `#psp-radio-PPAYITR1XXX` at `/lista-psp`, indicating that the Postepay PSP ID is missing from active environment configuration data.
- **Unsynchronised Back Navigation (Flaky)**: Tests 3 and 6 failed attempting to click the `Indietro` button while the browser was still at the landing page URL (`https://dev.checkout.pagopa.it/`), indicating race conditions in step navigation setup.