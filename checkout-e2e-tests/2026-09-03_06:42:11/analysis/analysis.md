# 1. Flusso lista PSP - indietro da /scegli-metodo (metodo APM)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (metodo APM)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://uat.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 79, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The test timed out trying to locate and click the 'Indietro' button on the root checkout page.
### Category
### Recommended action
Verify if the UI button selector changed or if the page failed to render the expected navigation controls in time.

---

# 2. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The specific Postepay PSP option (`#psp-radio-PPAYITR1XXX`) did not render or load on the PSP list page within the timeout.
### Category
### Recommended action
Check if the UAT environment's PSP configuration for Postepay is currently active or experiencing loading delays.

---

# 3. Navigazione - Conferma pagina di riepilogo
- **status**: failed
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Navigazione - Conferma pagina di riepilogo`
- **message**: AssertionError: Expected page '/dati-pagamento', but found '/inserisci-dati-avviso'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 29, in step_on_page
    assert current_url == page_url, f"Expected page '{page_url}', but found '{current_url}'"
           ^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The test expected the user to progress to `/dati-pagamento`, but the application kept the user on `/inserisci-dati-avviso`.
### Category
### Recommended action
Investigate application routing logic or upstream validation failures when submitting notice data.

---

# 4. Assenza loop de navigazione per indietro successivi da pagina Modifica metodo di pagamento
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento`
- **message**: KeyError: 'Modifica metodo di pagamento'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 57, in step_click_button_given
    step_click_button(context, button_text)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 78, in step_click_button
    logger.debug("Clicking button: %s with selector %s", button_text, BUTTON_SELECTORS[button_text])
                                                                      ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
```
### Root cause
A `KeyError` occurred because the dictionary `BUTTON_SELECTORS` lacks an entry mapping for 'Modifica metodo di pagamento'.
### Category
### Recommended action
Update the test automation step definitions (`BUTTON_SELECTORS`) to include the missing button text mapping.

---

# 5. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
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
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Timeout waiting for the Postepay radio button element on the authenticated checkout PSP list page.
### Category
### Recommended action
Check environment data or API stability regarding PSP list loading in the authenticated flow.

---

# 6. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://uat.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 79, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The 'Indietro' button locator timed out on the initial base URL due to page rendering latency or state mismatch.
### Category
### Recommended action
Increase locator timeout thresholds or ensure the page has fully loaded before attempting navigation interactions.

---

# 7. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
The creditor institution (Ente Creditore) mock service returned an unexpected generic error instead of the specific notice-not-found error message.
### Category
### Recommended action
Verify the stub/mock configuration for invalid notice code ranges in the UAT environment.

---

# 8. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://uat.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 79, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Timeout waiting for the 'Indietro' button to appear on the card entry view under specific feature flags.
### Category
### Recommended action
Review recent UI changes affecting back-navigation button render conditions on the card input screen.

---

# 9. Navigazione - Scelta metodo di pagamento “Carte di Credito”
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Navigazione - Scelta metodo di pagamento “Carte di Credito”`
- **message**: playwright._impl._errors.TimeoutError: Timeout 5000ms exceeded.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 80, in step_click_button
    page.wait_for_load_state("networkidle", timeout=5000)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 9117, in wait_for_load_state
    self._sync(self._impl_obj.wait_for_load_state(state=state, timeout=timeout))
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
           ~~~~~~~~~~~^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/playwright/_impl/_page.py", line 576, in wait_for_load_state
    return await self._main_frame.wait_for_load_state(**locals_to_params(locals()))
           ^^^^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/playwright/_impl/_frame.py", line 33, in wait_for_load_state
    |    return
```
### Root cause
The page failed to reach the `networkidle` load state within the 5000ms threshold due to persistent background polling/analytics network requests.
### Category
### Recommended action
Avoid using `networkidle` state checks in test steps; prefer explicit element visibility assertions instead.

---

# 10. Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.2
- **status**: failed
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Click sul tasto indietro riporta alla pagina precedente del flusso`
- **message**: AssertionError: Expected page '/dati-pagamento', but found '/inserisci-dati-avviso'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 29, in step_on_page
    assert current_url == page_url, f"Expected page '{page_url}', but found '{current_url}'"
           ^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Navigation history handling directed the user back to the initial entry page instead of the immediate previous step.
### Category
### Recommended action
Debug the client-side routing history implementation to ensure back buttons pop the correct history state.

---

## Common patterns
1. **Element & Locator Timeouts**: Several failures stem from strict 5-second timeouts (`TimeoutError` / `RuntimeError`) on UI elements and network states (`networkidle`), pointing to environmental latency or fragile synchronization techniques.
2. **Back Navigation & Routing Mismatches**: Multiple test cases fail when validating expected URLs after navigation actions (e.g., unexpected redirects to `/inserisci-dati-avviso`), indicating potential regressions in the frontend routing or history stack.