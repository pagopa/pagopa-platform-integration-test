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
The system returned a generic creditor issuer error instead of the expected 'notice not found' error modal message.
### Category
application bug
### Recommended action
Verify the backend mapping for the specified notice code range to ensure proper error codes are returned to the frontend.

---

# 2. Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.2
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
Back navigation redirected the user to an unexpected step in the checkout flow due to routing state mismatches.
### Category
application bug
### Recommended action
Check the browser history management and routing logic for the back button on the payment details page.

---

# 3. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
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
The test timed out waiting for the 'Indietro' button because the UI failed to render or load the expected page correctly.
### Category
environment
### Recommended action
Check environment stability and increase element wait timeouts if the UAT environment experiences high latency.

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
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The Postepay PSP option element was not rendered on the PSP list page, likely due to configuration or API data issues.
### Category
test data
### Recommended action
Ensure the test data environment correctly configures and returns the Postepay PSP option for the target payment notice.

---

# 5. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
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
The test timed out looking for the back button on the root checkout URL due to a slow page load or failed redirection.
### Category
environment
### Recommended action
Investigate UAT environment response times and add robust page load synchronization before querying UI elements.

---

# 6. Navigazione - Conferma pagina di riepilogo
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
The summary page confirmation action redirected the user to the initial notice insertion page instead of the expected payment details page.
### Category
application bug
### Recommended action
Review the routing logic tied to the summary page confirmation action to ensure it preserves the correct navigation stack.

---

# 7. Navigazione - Scelta metodo di pagamento “Carte di Credito”
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
```
### Root cause
The `networkidle` load state timed out because background network polling or analytics requests prevented network quiescence within 5 seconds.
### Category
flaky
### Recommended action
Replace `networkidle` state waits with specific element visibility checks or increase the timeout duration.

---

# 8. Flusso lista PSP - indietro da /scegli-metodo (metodo APM)
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
Timeout locating the back button on the root checkout URL due to delayed page rendering or redirection failure.
### Category
environment
### Recommended action
Ensure stability of the UAT environment and verify proper page navigation before invoking locator actions.

---

# 9. Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento
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
The button text mapping dictionary (`BUTTON_SELECTORS`) lacks an entry for 'Modifica metodo di pagamento'.
### Category
application bug
### Recommended action
Update the test step definitions or `BUTTON_SELECTORS` mapping in `back_navigation.py` to include the missing button label.

---

# 10. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#spidButton' after 5000 ms (url: https://uat.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg_auth.py", line 14, in step_impl
    step_click_login_button(context)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/spid_auth.py", line 129, in step_click_login_button
    perform_login(page)
    ~~~~~~~~~~~~~^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 72, in perform_login
    locate_and_click(page, "#spidButton")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The SPID login button (`#spidButton`) failed to load or render within the timeout period on the UAT checkout page.
### Category
environment
### Recommended action
Check UAT environment stability and identity provider availability during test execution.

---

## Common patterns
- **Environment & Timeout Failures**: Several test failures (3, 5, 8, 10) stem from element location timeouts (`RuntimeError: Timeout on locator ... after 5000 ms`) caused by slow loading or redirection issues on the UAT environment, often dropping back to the base URL.
- **Navigation & Routing Mismatches**: Failures 2 and 6 indicate discrepancies in expected versus actual URL states during back-navigation and summary confirmation flows.