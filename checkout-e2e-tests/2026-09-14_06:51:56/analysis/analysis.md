# 1. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-WOLLNLB1' after 5000 ms (url: https://uat.checkout.pagopa.it/inserisci-carta)
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
```
### Root cause
The radio button locator `#psp-radio-WOLLNLB1` was not found on the `/inserisci-carta` page within the 5000ms timeout.

### Category
environment

### Recommended action
Verify if Worldpay (`WOLLNLB1`) PSP is properly configured and available in the UAT environment.

---

# 2. La lista PSP è ordinata per nome nella pagina di selezione PSP
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome nella pagina di selezione PSP`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 5000ms exceeded.
Call log:
  - waiting for locator(".pspFeeName").first to be visible
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 167, in step_psp_selection_page_loaded
    page.locator(".pspFeeName").first.wait_for(state="visible", timeout=5000)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
```
### Root cause
Timeout waiting for `.pspFeeName` element to become visible on the PSP selection page.

### Category
flaky

### Recommended action
Ensure the PSP list network call completes before assertion or increase element visibility timeout.

---

# 3. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/inserisci-carta)
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
```
### Root cause
The radio button locator `#psp-radio-PPAYITR1XXX` was not visible on the `/inserisci-carta` page before timeout.

### Category
environment

### Recommended action
Check Postepay (`PPAYITR1XXX`) configuration and availability in UAT.

---

# 4. Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.2
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
Clicking the back button redirected the user back to `/inserisci-dati-avviso` instead of `/dati-pagamento`.

### Category
application bug

### Recommended action
Fix client-side navigation history logic to ensure accurate backward routing.

---

# 5. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
The backend response triggered a generic creditor error instead of the specific unknown notice error message modal.

### Category
application bug

### Recommended action
Verify notice error mapping for code range `302400000000000000-302409999999999999` in the API service.

---

# 6. Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.6
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Click sul tasto indietro riporta alla pagina precedente del flusso`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 80, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
```
### Root cause
The 'Indietro' button was not present or visible on the `/lista-psp` page within 5000 ms.

### Category
application bug

### Recommended action
Check UI implementation on `/lista-psp` to ensure the back button is visible and accessible.

---

# 7. La lista PSP è ordinata per commissione in ordine crescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione in ordine crescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 117, in step_select_psp_radio
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
```
### Root cause
The PSP radio element `#psp-radio-BCITITMM` did not render on `/lista-psp` within timeout.

### Category
environment

### Recommended action
Verify that PSP `BCITITMM` is configured and served in UAT environment catalogs.

---

# 8. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-WOLLNLB1' after 5000 ms (url: https://uat.checkout.pagopa.it/inserisci-carta)
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
```
### Root cause
The radio button locator `#psp-radio-WOLLNLB1` was missing on `/inserisci-carta` in authenticated flow.

### Category
environment

### Recommended action
Ensure Worldpay PSP (`WOLLNLB1`) is enabled for authenticated checkout flows in UAT.

---

# 9. La lista PSP è ordinata per commissione nella pagina di selezione PSP
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione nella pagina di selezione PSP`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 5000ms exceeded.
Call log:
  - waiting for locator(".pspFeeName").first to be visible
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 167, in step_psp_selection_page_loaded
    page.locator(".pspFeeName").first.wait_for(state="visible", timeout=5000)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
```
### Root cause
Timeout waiting for `.pspFeeName` element to be visible during PSP list loading.

### Category
flaky

### Recommended action
Increase visibility wait timeout or wait for response network event before asserting element presence.

---

# 10. La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 117, in step_select_psp_radio
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
```
### Root cause
Locator `#psp-radio-BCITITMM` timed out on `/lista-psp`.

### Category
environment

### Recommended action
Confirm availability of PSP `BCITITMM` in UAT mock/catalog data.

---

# 11. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/inserisci-carta)
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
```
### Root cause
PSP radio button `#psp-radio-PPAYITR1XXX` was missing on `/inserisci-carta` in authenticated flow.

### Category
environment

### Recommended action
Verify Postepay PSP configuration in UAT for authenticated sessions.

---

# 12. Flusso lista PSP - indietro da /scegli-metodo (metodo APM)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (metodo APM)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 80, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
```
### Root cause
The back button matching locator `button:has-text('Indietro')` was not found on `/lista-psp`.

### Category
application bug

### Recommended action
Ensure the back button element is consistently rendered on `/lista-psp`.

---

# 13. La lista PSP è ordinata per commissione in ordine decrescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione in ordine decrescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 117, in step_select_psp_radio
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
```
### Root cause
The locator `#psp-radio-BCITITMM` timed out on `/lista-psp`.

### Category
environment

### Recommended action
Ensure PSP `BCITITMM` is correctly returned by UAT backend services.

---

# 14. Navigazione - Scelta metodo di pagamento “Carte di Credito”
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
  File "src/e2e/checkout/steps/back_navigation.py", line 81, in step_click_button
    page.wait_for_load_state("networkidle", timeout=5000)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 9117, in wait_for_load_state
```
### Root cause
`wait_for_load_state("networkidle")` timed out after 5000ms due to active or pending network connections.

### Category
flaky

### Recommended action
Replace `networkidle` state waits with specific target element visibility assertions.

---

# 15. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BNLIITRR' after 5000 ms (url: https://uat.checkout.pagopa.it/inserisci-carta)
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
```
### Root cause
Locator `#psp-radio-BNLIITRR` timed out on `/inserisci-carta` in authenticated flow.

### Category
environment

### Recommended action
Verify Wordline PSP (`BNLIITRR`) availability in UAT checkout configuration.

---

# 16. Navigazione - Conferma pagina di riepilogo
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
Summary confirmation navigation landed on `/inserisci-dati-avviso` instead of `/dati-pagamento`.

### Category
application bug

### Recommended action
Audit application routing and session preservation steps during payment summary confirmation.

---

# 17. La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 117, in step_select_psp_radio
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
```
### Root cause
The PSP radio `#psp-radio-BCITITMM` timed out on `/lista-psp`.

### Category
environment

### Recommended action
Ensure PSP `BCITITMM` is configured and served in UAT environment catalogs.

---

# 18. Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento`
- **message**: RuntimeError: Timeout on locator '#psp-radio-MOONITMMXXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 27, in step_on_page
    navigate_to_page(context, page_url)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 152, in navigate_to_page
```
### Root cause
Helper navigation timed out looking for `#psp-radio-MOONITMMXXX` on `/lista-psp`.

### Category
environment

### Recommended action
Verify configuration and availability of PSP `MOONITMMXXX` in UAT mock data.

---

# 19. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BNLIITRR' after 5000 ms (url: https://uat.checkout.pagopa.it/inserisci-carta)
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
```
### Root cause
Radio locator `#psp-radio-BNLIITRR` was missing on `/inserisci-carta` within 5 seconds timeout.

### Category
environment

### Recommended action
Check UAT deployment setup for Wordline PSP (`BNLIITRR`).

---

## Common patterns

Across the 19 test failures in the Checkout E2E integration test suite, three primary failure patterns emerged:

1. **Missing PSP Option Elements in UAT Environment (12/19 failures):**
   The majority of failures (#1, #3, #7, #8, #10, #11, #13, #15, #17, #18, #19) are caused by `RuntimeError: Timeout on locator '#psp-radio-<PSP_ID>'` on either `/inserisci-carta` or `/lista-psp`. Specific PSPs (`WOLLNLB1`, `PPAYITR1XXX`, `BCITITMM`, `BNLIITRR`, `MOONITMMXXX`) are either missing from the UAT backend catalog or failing to render within 5000 ms.

2. **Navigation and Routing Defects (4/19 failures):**
   Failures #4, #6, #12, and #16 represent routing or UI structure issues in navigation flows:
   - Back navigation step unexpectedly landed on `/inserisci-dati-avviso` instead of `/dati-pagamento` (#4, #16).
   - Missing or non-interactable `Indietro` back button on `/lista-psp` (#6, #12).

3. **Flaky / Playwright Timing Assertions (3/19 failures):**
   Failures #2, #9, and #14 failed due to strict synchronization timeouts (`.pspFeeName` visibility or `wait_for_load_state("networkidle")`). These timeouts occur when asynchronous background network calls take longer than 5 seconds in UAT.