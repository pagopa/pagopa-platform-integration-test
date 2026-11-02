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
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 88, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The "Indietro" button was not found or not rendered within the 5-second timeout on the target page.
### Category
application bug
### Recommended action
Verify if UI changes altered the back button selector or if page load performance is causing rendering delays.

---

# 2. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-WOLLNLB1' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
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
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The PSP radio button for Worldpay (`#psp-radio-WOLLNLB1`) failed to load or render on the PSP selection page.
### Category
test data
### Recommended action
Check if the Worldpay PSP configuration is currently active and returned by the backend services in the dev environment.

---

# 3. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The Postepay PSP radio option (`#psp-radio-PPAYITR1XXX`) was missing from the rendered PSP list.
### Category
test data
### Recommended action
Validate that the Postepay PSP configuration is enabled and available in the test environment configuration.

---

# 4. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-WOLLNLB1' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
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
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The Worldpay PSP element was not present on the list page within the allowed timeout.
### Category
test data
### Recommended action
Ensure the PSP mapping and availability match the expected test environment dataset.

---

# 5. La lista PSP è ordinata per nome nella pagina di selezione PSP
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome nella pagina di selezione PSP`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 5000ms exceeded.
Call log:
  - waiting for locator(".pspFeeName").first to be visible
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 167, in step_psp_selection_page_loaded
    page.locator(".pspFeeName").first.wait_for(state="visible", timeout=5000)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
           ~~~~~~~~~~~^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_locator.py", line 692, in wait_for
    await self._frame.wait_for_selector(
        self._selector, strict=True, timeout=timeout, state=state
    )
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
    await self._channel.send(
        "waitForSelecto
```
### Root cause
The selector `.pspFeeName` did not appear, indicating the PSP selection page failed to load elements properly.
### Category
application bug
### Recommended action
Investigate frontend rendering issues or API failures blocking the display of PSP fee names.

---

# 6. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
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
The Wordline PSP radio element (`#psp-radio-BNLIITRR`) could not be located on the page.
### Category
test data
### Recommended action
Verify if the specific PSP ID mapping has changed or if the PSP is unavailable in the current environment.

---

# 7. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
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
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The back navigation button was not rendered on the landing page within the allocated timeframe.
### Category
application bug
### Recommended action
Check page initialization logic and ensure navigation buttons are rendered correctly.

---

# 8. Flusso lista PSP - indietro da /scegli-metodo (metodo APM)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (metodo APM)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
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
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The back button failed to appear on the APM payment method selection view.
### Category
application bug
### Recommended action
Inspect UI components for APM flows to ensure the back action button is consistently present.

---

# 9. La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 117, in step_select_psp_radio
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The expected PSP radio button (`#psp-radio-BCITITMM`) was missing from the PSP list view.
### Category
test data
### Recommended action
Verify that the test data provides the expected PSP options needed for sorting validation tests.

---

# 10. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BNLIITRR' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The Wordline PSP element was not rendered or loaded on the checkout page.
### Category
test data
### Recommended action
Check environment configuration and ensure PSP availability matches test scenarios.

---

# 11. La lista PSP è ordinata per commissione in ordine decrescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione in ordine decrescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 117, in step_select_psp_radio
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
PSP radio option `#psp-radio-BCITITMM` could not be located during sorting validation.
### Category
test data
### Recommended action
Ensure the required PSP configuration is present in the environment for sorting tests.

---

# 12. La lista PSP è ordinata per commissione nella pagina di selezione PSP
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione nella pagina di selezione PSP`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 5000ms exceeded.
Call log:
  - waiting for locator(".pspFeeName").first to be visible
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 167, in step_psp_selection_page_loaded
    page.locator(".pspFeeName").first.wait_for(state="visible", timeout=5000)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
           ~~~~~~~~~~~^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_locator.py", line 692, in wait_for
    await self._frame.wait_for_selector(
        self._selector, strict=True, timeout=timeout, state=state
    )
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
    await self._channel.send(
        "waitForSelecto
```
### Root cause
Timeout waiting for `.pspFeeName` element to become visible on the page.
### Category
application bug
### Recommended action
Verify if backend services providing PSP fees are responding correctly and timely.

---

# 13. Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento`
- **message**: RuntimeError: Timeout on locator '#psp-radio-MOONITMMXXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 27, in step_on_page
    navigate_to_page(context, page_url)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 164, in navigate_to_page
    elif page_url == "/riepilogo-pagamento": naviga_riepilogo_pagamento(context)
                                             ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 227, in naviga_riepilogo_pagamento
    locate_and_click(page, "#psp-radio-MOONITMMXXX")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The radio button `#psp-radio-MOONITMMXXX` was not found during navigation setup.
### Category
test data
### Recommended action
Confirm that the specified PSP is active and listed in the current environment data set.

---

# 14. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The upstream service returned a generic creditor error ("Ente Creditore") instead of the expected unknown notice error message.
### Category
environment
### Recommended action
Check backend node health and mock/stub responses for invalid payment notice ranges.

---

# 15. La lista PSP è ordinata per commissione in ordine crescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione in ordine crescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 117, in step_select_psp_radio
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
PSP element `#psp-radio-BCITITMM` timed out during summary page validation.
### Category
test data
### Recommended action
Verify that test data configurations match the expected PSP identifiers in sorting scenarios.

---

# 16. Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.6
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Click sul tasto indietro riporta alla pagina precedente del flusso`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
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
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The back navigation button was missing or failed to render on the PSP list page.
### Category
application bug
### Recommended action
Inspect UI implementation for back navigation controls on the PSP listing view.

---

# 17. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
  File "src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Postepay PSP option (`#psp-radio-PPAYITR1XXX`) was missing in the authenticated checkout flow.
### Category
test data
### Recommended action
Check environment data setup for authenticated payment configurations.

---

# 18. La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 117, in step_select_psp_radio
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
PSP element `#psp-radio-BCITITMM` failed to render during descending name sort verification.
### Category
test data
### Recommended action
Validate that PSP configuration datasets are correctly provisioned in the environment.

---

# 19. Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.6
- **status**: broken
- **fullName**: `features.FEAT_005_Checkout - Back Navigation Control.Navigazione Lineare per il flusso di Pagamento.Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.6`
- **message**: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
Failing step: Quando L’utente clicca sul tasto "Indietro" ... failed in 80.093s
Location: src/e2e/checkout/features/FEAT_005_Checkout - Back Navigation Control.feature:78
Traceback (most recent call last):
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 94, in locate_and_click
    to_click.click(click_count=click_count)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 15543, in click
    self._sync(
    ~~~~~~~~~~^
        self._impl_obj.click(
        ^^^^^^^^^^^^^^^^^^^^^
    ...<9 lines>...
        )
        ^
    )
    ^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
           ~~~~~~~~~~~^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_locator.py", line 160, in click
    return await self._frame.click(self._selector, strict=True, **params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 549, in click
    await self._channel.send("click", self._timeout, locals_to_params(locals()))
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_connection.py", line 69, in 
```
### Root cause
The back navigation button was not interactable or missing within the timeout window.
### Category
application bug
### Recommended action
Ensure the back button is correctly rendered and clickable across all steps of the payment flow.

---

# 20. Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento
- **status**: broken
- **fullName**: `features.FEAT_005_Checkout - Back Navigation Control.Navigazione Lineare per il flusso di Pagamento.Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento`
- **message**: Timeout on locator '#psp-radio-MOONITMMXXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
Failing step: Dato L’utente si trova sulla pagina "/riepilogo-pagamento" ... failed in 9.578s
Location: src/e2e/checkout/features/FEAT_005_Checkout - Back Navigation Control.feature:97
Traceback (most recent call last):
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 93, in locate_and_click
    to_click.wait_for(state="visible", timeout=timeout)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
    ~~~~~~~~~~^^^^../opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
           ~~~~~~~~~~~^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_locator.py", line 692, in wait_for
    await self._frame.wait_for_selector(
        self._selector, strict=True, timeout=timeout, state=state
    )
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
    await self._channel.send(
        "waitForSelector", self._timeout, locals_to_params(locals())
    )
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playw
```
### Root cause
The target PSP option `#psp-radio-MOONITMMXXX` failed to load when setting up the summary page state.
### Category
test data
### Recommended action
Verify that the corresponding PSP is correctly configured and available in the target test environment.

---

## Common patterns
- **PSP Selection Timeouts**: A significant portion of failures stem from timeouts trying to locate specific PSP radio buttons (e.g., `#psp-radio-WOLLNLB1`, `#psp-radio-PPAYITR1XXX`, `#psp-radio-BNLIITRR`, `#psp-radio-BCITITMM`). This indicates potential backend instability, missing PSP configurations, or environment data discrepancies.
- **UI Navigation Control Failures**: Several failures involve timeouts waiting for the "Indietro" button or elements like `.pspFeeName`, suggesting frontend performance degradation or rendering issues during step transitions.