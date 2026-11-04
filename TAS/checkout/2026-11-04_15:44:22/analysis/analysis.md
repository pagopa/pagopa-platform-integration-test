# 1. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded.
Call log:
  - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_locator.py", line 692, in wait_for
    await self._frame.wait_for_selector(
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
```
### Root cause
Timeout waiting for the payment response confirmation page title after interacting with Worldpay gateway.

### Category
application bug

### Recommended action
Investigate backend processing time or gateway redirect issues for Worldpay transactions in the dev environment.

---

# 2. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 88, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The 'Indietro' button could not be found within the 5-second timeout on the checkout page.

### Category
flaky

### Recommended action
Increase the timeout or ensure the element is fully rendered before attempting the click action.

---

# 3. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The specific PSP radio button for Postepay (`#psp-radio-PPAYITR1XXX`) failed to render or load on the PSP list page.

### Category
test data

### Recommended action
Verify if the Postepay PSP configuration is active and correctly returned by the mock/backend services in the dev environment.

---

# 4. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded.
Call log:
  - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_locator.py", line 692, in wait_for
    await self._frame.wait_for_selector(
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
```
### Root cause
Timed out waiting for the response confirmation page after completing a Wordline payment flow.

### Category
application bug

### Recommended action
Check Worldline webhook integration and callback handling in the checkout service.

---

# 5. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The Postepay PSP option did not appear on the PSP selection page during the authenticated checkout flow.

### Category
test data

### Recommended action
Ensure test environment PSP mappings include Postepay and that the upstream catalog API is responsive.

---

# 6. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded.
Call log:
  - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_locator.py", line 692, in wait_for
    await self._frame.wait_for_selector(
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
```
### Root cause
Worldpay payment completion page failed to load within the 120-second window.

### Category
application bug

### Recommended action
Examine server-side logs for Worldpay integration timeouts or redirect failures.

---

# 7. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
```
### Root cause
The application returned a generic creditor issuer error instead of the expected 'notice not found' error modal header.

### Category
environment

### Recommended action
Verify the stub/mock configuration for invalid notice codes in the test environment to ensure correct error mapping.

---

# 8. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 120000ms exceeded.
Call log:
  - waiting for locator("#responsePageMessageTitle") to be visible
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_locator.py", line 692, in wait_for
    await self._frame.wait_for_selector(
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
```
### Root cause
Wordline payment response title element did not appear before the 120s timeout.

### Category
application bug

### Recommended action
Debug the Wordline payment gateway callback route and frontend rendering state upon return.

---

# 9. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 88, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
Navigation back button failed to render or become clickable within the allocated 5 seconds.

### Category
flaky

### Recommended action
Add an explicit wait for element visibility before clicking the back button in navigation tests.

---

## Common patterns
- **Gateway Timeouts**: Payment completions using Worldpay and Wordline consistently hit the 120s timeout waiting for `#responsePageMessageTitle`, pointing to potential backend callback or redirect issues.
- **PSP Selection Failures**: Postepay PSP selection steps fail due to missing elements on the `lista-psp` page, likely caused by test data or environment configuration inconsistencies.
- **UI Interaction Timeouts**: Short timeouts (5s) on navigation buttons (`Indietro`) lead to flaky test failures when the DOM is slow to update.