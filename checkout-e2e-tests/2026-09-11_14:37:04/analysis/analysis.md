# 1. Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento`
- **message**: RuntimeError: Timeout on locator '#psp-radio-MOONITMMXXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 27, in step_on_page
    navigate_to_page(context, page_url)
  File "src/e2e/checkout/steps/back_navigation.py", line 151, in navigate_to_page
    elif page_url == "/riepilogo-pagamento": naviga_riepilogo_pagamento(context)
  File "src/e2e/checkout/steps/back_navigation.py", line 191, in naviga_riepilogo_pagamento
    locate_and_click(page, "#psp-radio-MOONITMMXXX")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The specified PSP radio button element `#psp-radio-MOONITMMXXX` was not found on the page within the 5-second timeout.

### Category
test data

### Recommended action
Verify if the PSP identifier `MOONITMMXXX` is currently active and available in the UAT environment, or update the test data.

---

# 2. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://uat.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 79, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The 'Indietro' back button could not be located on the root UAT checkout page during the navigation flow test.

### Category
application bug

### Recommended action
Check if recent UI updates modified the back button selector or rendering condition on the root checkout page.

---

# 3. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-WOLLNLB1' after 5000 ms (url: https://uat.checkout.pagopa.it/inserisci-carta)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The Worldpay PSP radio option (`#psp-radio-WOLLNLB1`) failed to render or load within the timeout on the card insertion page.

### Category
test data

### Recommended action
Confirm availability of the Worldpay PSP configuration in the UAT environment and ensure the target PSP ID is still valid.

---

# 4. La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 117, in step_select_psp_radio
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The PSP radio element `#psp-radio-BCITITMM` timed out on the PSP list page during the ascending name sorting test.

### Category
test data

### Recommended action
Verify if PSP `BCITITMM` is active in UAT and returned in the sorting test dataset.

---

# 5. La lista PSP è ordinata per commissione in ordine crescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione in ordine crescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 117, in step_select_psp_radio
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The element `#psp-radio-BCITITMM` failed to appear on the PSP list page during ascending fee sorting verification.

### Category
test data

### Recommended action
Ensure PSP `BCITITMM` is present and available in the fee-sorting test scenario data.

---

# 6. La lista PSP è ordinata per nome nella pagina di selezione PSP
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome nella pagina di selezione PSP`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 5000ms exceeded.
Call log:
  - waiting for locator(".pspFeeName").first to be visible
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 167, in step_psp_selection_page_loaded
    page.locator(".pspFeeName").first.wait_for(state="visible", timeout=5000)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
```
### Root cause
The selector `.pspFeeName` failed to become visible on the PSP selection page, indicating the page contents did not load or render in time.

### Category
application bug

### Recommended action
Investigate frontend performance or rendering issues preventing the PSP selection elements from loading.

---

# 7. La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 117, in step_select_psp_radio
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
Timeout waiting for `#psp-radio-BCITITMM` during the descending name sorting test on the PSP list page.

### Category
test data

### Recommended action
Verify that PSP `BCITITMM` is configured and available in the descending sorting test case.

---

# 8. La lista PSP è ordinata per commissione nella pagina di selezione PSP
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione nella pagina di selezione PSP`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 5000ms exceeded.
Call log:
  - waiting for locator(".pspFeeName").first to be visible
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 167, in step_psp_selection_page_loaded
    page.locator(".pspFeeName").first.wait_for(state="visible", timeout=5000)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
```
### Root cause
The `.pspFeeName` locator failed to load within the timeout during fee-based sorting on the PSP selection page.

### Category
application bug

### Recommended action
Review recent changes in the fee sorting view to ensure elements load consistently without timing out.

---

# 9. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-WOLLNLB1' after 5000 ms (url: https://uat.checkout.pagopa.it/inserisci-carta)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The authenticated Worldpay card payment flow failed because `#psp-radio-WOLLNLB1` was not found.

### Category
test data

### Recommended action
Check Worldpay PSP availability and configuration in authenticated checkout test suites.

---

# 10. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/inserisci-carta)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The Postepay radio button `#psp-radio-PPAYITR1XXX` did not load within 5 seconds during the authenticated payment test.

### Category
test data

### Recommended action
Verify that the Postepay PSP (`PPAYITR1XXX`) is active and properly mapped in the UAT environment.

---

# 11. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/inserisci-carta)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
Timeout locating `#psp-radio-PPAYITR1XXX` on the card insertion page for the Postepay payment test.

### Category
test data

### Recommended action
Ensure the test data corresponds to currently available PSPs in the UAT environment.

---

# 12. Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.6
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Click sul tasto indietro riporta alla pagina precedente del flusso`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 79, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The back button (`button:has-text('Indietro')`) was not present or clickable on the PSP list page.

### Category
application bug

### Recommended action
Verify if the back button rendering logic was recently altered on the PSP list page.

---

# 13. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
```
### Root cause
An upstream creditor institution (Ente Creditore) timeout or error occurred instead of the expected unknown notice error response.

### Category
environment

### Recommended action
Check backend mock/node availability for the specified notice code range in the UAT environment.

---

# 14. Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.2
- **status**: failed
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Click sul tasto indietro riporta alla pagina precedente del flusso`
- **message**: AssertionError: Expected page '/dati-pagamento', but found '/inserisci-dati-avviso'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 29, in step_on_page
    assert current_url == page_url, f"Expected page '{page_url}', but found '{current_url}'"
```
### Root cause
Clicking the back button navigated to an unexpected page (`/inserisci-dati-avviso`) instead of the expected `/dati-pagamento`.

### Category
application bug

### Recommended action
Review history stack and routing logic for the back button on the payment details step.

---

# 15. Navigazione - Conferma pagina di riepilogo
- **status**: failed
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Navigazione - Conferma pagina di riepilogo`
- **message**: AssertionError: Expected page '/dati-pagamento', but found '/inserisci-dati-avviso'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 29, in step_on_page
    assert current_url == page_url, f"Expected page '{page_url}', but found '{current_url}'"
```
### Root cause
Routing discrepancy during summary page confirmation caused the browser to remain on `/inserisci-dati-avviso`.

### Category
application bug

### Recommended action
Verify redirect paths and confirmation event handlers for the summary page.

---

# 16. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BNLIITRR' after 5000 ms (url: https://uat.checkout.pagopa.it/inserisci-carta)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The Wordline PSP radio element `#psp-radio-BNLIITRR` failed to appear within the timeout on the card entry page.

### Category
test data

### Recommended action
Check if the Wordline PSP configuration is active and properly indexed in the UAT environment.

---

# 17. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BNLIITRR' after 5000 ms (url: https://uat.checkout.pagopa.it/inserisci-carta)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
Timeout on locator `#psp-radio-BNLIITRR` during the standard Wordline card payment execution.

### Category
test data

### Recommended action
Verify PSP availability and validity of the `BNLIITRR` identifier in UAT.

---

# 18. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://uat.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 79, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The back button was not found on the root URL during the card flow back-navigation test.

### Category
application bug

### Recommended action
Inspect UI changes affecting back button visibility on the initial checkout landing states.

---

# 19. Flusso lista PSP - indietro da /scegli-metodo (metodo APM)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (metodo APM)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://uat.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/back_navigation.py", line 79, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
Timeout waiting for the 'Indietro' button element on the root checkout page during APM flow testing.

### Category
application bug

### Recommended action
Check if recent updates altered navigation controls on the initial checkout step.

---

# 20. La lista PSP è ordinata per commissione in ordine decrescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione in ordine decrescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 117, in step_select_psp_radio
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
PSP radio `#psp-radio-BCITITMM` timed out during descending fee sorting validation.

### Category
test data

### Recommended action
Verify PSP configuration and availability for `BCITITMM` in the UAT environment.

---

## Common patterns
1. **PSP ID Timeouts**: A significant portion of failures stem from specific PSP radio buttons (`#psp-radio-...`) timing out across various payment and sorting flows, pointing to potential UAT test data unavailability or environment misalignment.
2. **Back Button Location Failures**: Multiple navigation tests fail due to the inability to locate the 'Indietro' button on landing or list pages, suggesting UI selector changes or routing regressions.