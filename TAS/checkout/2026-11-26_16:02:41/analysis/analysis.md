# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The PSP radio button for Postepay failed to load or render within the 5-second timeout on the UAT environment.

### Category
environment

### Recommended action
Check if the PSP configuration or downstream service is responding slowly, and consider increasing the locator timeout or investigating environment stability.

---

# 2. Inserimento dati - errori -  Inserimento codice avviso errato -- @1.2
- **status**: broken
- **fullName**: `Validazione sintattica dei campi: Inserimento dati - errori -  Inserimento codice avviso errato`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 59, in value
    raise exception
```
### Root cause
Navigation did not complete within 15 seconds after clicking the button, leading to a Playwright timeout error.

### Category
environment

### Recommended action
Verify if the target page or backend service is experiencing latency or if the expected navigation event was triggered correctly.

---

# 3. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://uat.checkout.pagopa.it/)
- **trace**:
```
  File "src/e2e/checkout/steps/back_navigation.py", line 88, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The 'Indietro' button could not be found on the page within the 5-second timeout during the navigation flow.

### Category
application bug

### Recommended action
Ensure the UI renders the back button correctly on the `/scegli-metodo` page or update the selector if the UI text/structure changed.

---

# 4. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The PSP radio button for Postepay failed to load or render within the 5-second timeout on the UAT environment.

### Category
environment

### Recommended action
Check environment stability and PSP service availability, or adjust the locator timeout.

---

# 5. Inserimento dati - errori -  Click sul tasto continua con campo non compilato -- @1.4
- **status**: broken
- **fullName**: `Validazione sintattica dei campi: Inserimento dati - errori -  Click sul tasto continua con campo non compilato`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 59, in value
    raise exception
```
### Root cause
Navigation timed out while waiting for the page load event after interacting with the form validation.

### Category
environment

### Recommended action
Investigate potential performance bottlenecks or slow responses during form validation steps in the UAT environment.

---

# 6. Inserimento dati - errori -  Inserimento CF ente errato -- @1.2
- **status**: broken
- **fullName**: `Validazione sintattica dei campi: Inserimento dati - errori -  Inserimento CF ente errato`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 59, in value
    raise exception
```
### Root cause
The page failed to complete navigation within the 15-second threshold after submitting an invalid creditor tax code (CF ente).

### Category
environment

### Recommended action
Check environment performance and ensure network conditions or service mocks are responding in a timely manner.

---

# 7. Inserimento dati - errori -  Inserimento indirizzo email non valido -- @1.3
- **status**: broken
- **fullName**: `Validazione sintattica dei campi: Inserimento dati - errori -  Inserimento indirizzo email non valido`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 59, in value
    raise exception
```
### Root cause
Timeout reached while waiting for page navigation to complete following the input of an invalid email address.

### Category
environment

### Recommended action
Re-run the test or check UAT environment responsiveness during email validation execution.

---

# 8. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://uat.checkout.pagopa.it/)
- **trace**:
```
  File "src/e2e/checkout/steps/back_navigation.py", line 88, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The back button was not rendered or interactive within the 5-second timeout on the card insertion page.

### Category
application bug

### Recommended action
Verify frontend rendering conditions for the 'Indietro' button when `enablePspPage=true` is set.

---

# 9. Inserimento dati - errori - indirizzo email diverso da ripeti
- **status**: broken
- **fullName**: `Validazione sintattica dei campi: Inserimento dati - errori - indirizzo email diverso da ripeti`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
  File "src/e2e/checkout/steps/back_navigation.py", line 87, in step_click_button
    with page.expect_navigation(timeout=15000):
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_sync_base.py", line 59, in value
    raise exception
```
### Root cause
Navigation event timed out after submitting mismatched email fields.

### Category
environment

### Recommended action
Investigate UAT environment load times and network latency during error validation tests.

---

# 10. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
```
### Root cause
The system returned a generic creditor error ("L’Ente Creditore sta avendo problemi nella risposta") instead of the specific unknown payment error message.

### Category
application bug

### Recommended action
Check backend error mapping for the specified notice code range to ensure the correct error message is displayed to the user.

---

## Common patterns
- **Environment Timeouts**: A significant portion of failures are `broken` tests caused by Playwright navigation timeouts (`Timeout 15000ms exceeded`) or element location timeouts (`Timeout on locator ... after 5000 ms`), indicating potential instability or performance issues in the UAT environment.
- **UI Navigation/Locators**: Multiple failures relate to missing or slow-to-load buttons (such as the 'Indietro' button and Postepay PSP radio buttons), pointing to either frontend rendering regressions or flaky element detection.