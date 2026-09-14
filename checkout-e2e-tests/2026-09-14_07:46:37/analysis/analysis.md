# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The PSP radio option `#psp-radio-PPAYITR1XXX` was not rendered on the `/inserisci-carta` page within the 5-second timeout.

### Category
environment

### Recommended action
Verify backend availability and configuration for Postepay (`PPAYITR1XXX`) in the UAT environment.

---

# 2. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
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
The PSP selection radio element `#psp-radio-WOLLNLB1` failed to appear on the page before timing out.

### Category
environment

### Recommended action
Ensure Worldpay PSP (`WOLLNLB1`) is enabled and properly returning data from the backend API in UAT.

---

# 3. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
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
```
### Root cause
The 'Indietro' button element was not visible or present on the root route (`https://uat.checkout.pagopa.it/`).

### Category
application bug

### Recommended action
Investigate frontend navigation logic to ensure the back button correctly renders on root path transitions.

---

# 4. La lista PSP è ordinata per commissione nella pagina di selezione PSP
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
The PSP fee label element (`.pspFeeName`) failed to render within the 5000ms timeout window.

### Category
environment

### Recommended action
Check backend response latency for retrieving PSP list and fee structures in the UAT environment.

---

# 5. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
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
```
### Root cause
The back button (`button:has-text('Indietro')`) was expected on page URL `/` but was not found within 5 seconds.

### Category
application bug

### Recommended action
Verify application routing when pressing back from `/inserisci-carta` to ensure correct rendering of header components.

---

# 6. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
Locator `#psp-radio-PPAYITR1XXX` timed out on `/inserisci-carta` before being clicked.

### Category
environment

### Recommended action
Inspect UAT network response for loading available PSP options and ensure Postepay is configured correctly.

---

# 7. Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.6
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
  File "src/e2e/checkout/steps/back_navigation.py", line 79, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
```
### Root cause
The 'Indietro' button could not be located on `/lista-psp` within 5 seconds.

### Category
application bug

### Recommended action
Check back button DOM selectors and visibility state on the `/lista-psp` page view.

---

# 8. Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento
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
  File "src/e2e/checkout/steps/back_navigation.py", line 151, in navigate_to_page
```
### Root cause
Target PSP `#psp-radio-MOONITMMXXX` was not present in the PSP list on `/lista-psp`.

### Category
test data

### Recommended action
Verify whether PSP ID `MOONITMMXXX` is present in the test environment fixtures for this scenario.

---

# 9. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
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
The Worldline PSP radio button `#psp-radio-BNLIITRR` did not appear on `/inserisci-carta` before locator timeout.

### Category
environment

### Recommended action
Check UAT service responses for Wordline PSP availability (`BNLIITRR`).

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
Navigating back redirected the application to `/inserisci-dati-avviso` instead of expected `/dati-pagamento`.

### Category
application bug

### Recommended action
Review back-navigation state machine logic to ensure proper route history is maintained.

---

# 11. La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo
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
Locator `#psp-radio-BCITITMM` timed out on `/lista-psp`.

### Category
test data

### Recommended action
Confirm if PSP code `BCITITMM` is configured in the environment setup for sorting tests.

---

# 12. Flusso lista PSP - indietro da /scegli-metodo (metodo APM)
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
```
### Root cause
The 'Indietro' button element timed out on page URL `/`.

### Category
application bug

### Recommended action
Fix root path UI behavior so back-navigation elements are correctly displayed when returning from APM selection.

---

# 13. La lista PSP è ordinata per nome nella pagina di selezione PSP
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
Timeout waiting for `.pspFeeName` elements to render on the PSP selection screen.

### Category
environment

### Recommended action
Investigate API latency for fetching PSP fees in UAT.

---

# 14. Navigazione - Conferma pagina di riepilogo
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
Navigating back from summary redirected to `/inserisci-dati-avviso` instead of `/dati-pagamento`.

### Category
application bug

### Recommended action
Audit application routing logic on payment confirmation step.

---

# 15. La lista PSP è ordinata per commissione in ordine decrescente nella pagina di riepilogo
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
The `#psp-radio-BCITITMM` radio button did not appear on `/lista-psp` before the 5s timeout expired.

### Category
test data

### Recommended action
Check PSP mock dataset for missing `BCITITMM` entity.

---

# 16. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
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
Timeout locating element `#psp-radio-WOLLNLB1` on `/inserisci-carta`.

### Category
environment

### Recommended action
Validate health and configuration of Worldpay PSP services in UAT.

---

# 17. La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo
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
Element `#psp-radio-BCITITMM` timed out on `/lista-psp`.

### Category
test data

### Recommended action
Verify `BCITITMM` availability in fixture lists used for sorting scenarios.

---

# 18. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
Application returned a generic creditor error modal instead of the specific 'unknown notice' error message.

### Category
application bug

### Recommended action
Ensure correct mapping of `PAA_PAGAMENTO_SCONOSCIUTO` error codes to user-facing modal headers in UI frontend.

---

# 19. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: playwright._impl._errors.TimeoutError: Timeout 80000ms exceeded.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 147, in step_fill_card_number
    page.wait_for_load_state("networkidle")
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 9117, in wait_for_load_state
```
### Root cause
Playwright timed out waiting 80 seconds for `networkidle` state during card entry step.

### Category
flaky

### Recommended action
Replace `page.wait_for_load_state("networkidle")` with explicit DOM element assertions to prevent hanging on continuous background network traffic.

---

# 20. La lista PSP è ordinata per commissione in ordine crescente nella pagina di riepilogo
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
Target radio element `#psp-radio-BCITITMM` timed out on `/lista-psp`.

### Category
test data

### Recommended action
Confirm `BCITITMM` PSP test entity exists and is returned by UAT mocks during execution.

---

## Common patterns

1. **Missing / Unrendered PSP Radio Selectors (`#psp-radio-*`)**:
   - **Occurrences**: Failures #1, #2, #6, #8, #9, #11, #15, #16, #17, #20 (10 out of 20 tests).
   - **Pattern**: Tests time out after 5000 ms waiting to click specific PSP options (`PPAYITR1XXX`, `WOLLNLB1`, `BNLIITRR`, `BCITITMM`, `MOONITMMXXX`). This points to either missing test data in mock setups or backend API slowness/failures in rendering the PSP options list in UAT.

2. **Navigation and Route Handling Flaws**:
   - **Occurrences**: Failures #3, #5, #7, #10, #12, #14 (6 out of 20 tests).
   - **Pattern**: Back-navigation steps are failing either because the `Indietro` button is missing when redirected to the root path `/` or because the client application redirects back to `/inserisci-dati-avviso` instead of `/dati-pagamento`.

3. **DOM Visibility & Load Timeout Dependencies**:
   - **Occurrences**: Failures #4, #13, #19 (3 out of 20 tests).
   - **Pattern**: UI elements such as `.pspFeeName` fail to display within 5 seconds, or explicit calls to `wait_for_load_state("networkidle")` cause 80s execution timeouts due to background polling/connections.