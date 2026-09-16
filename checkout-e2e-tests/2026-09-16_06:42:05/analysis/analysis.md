# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
```
### Root cause
The PSP element `#psp-radio-PPAYITR1XXX` was not loaded or visible on the PSP selection page within the 5-second timeout limit.

### Category
environment

### Recommended action
Verify whether the Postepay PSP (`PPAYITR1XXX`) service configuration is active in the UAT environment and returned by the backend API.

---

# 2. Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://uat.checkout.pagopa.it/riepilogo-pagamento)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 120, in step_click_back_button
    step_click_button(context, "Indietro")
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "src/e2e/checkout/steps/back_navigation.py", line 88, in step_click_button
```
### Root cause
The 'Indietro' button could not be located on the `/riepilogo-pagamento` page within 5 seconds, likely due to a UI selector change or rendering delay.

### Category
application bug

### Recommended action
Inspect the frontend DOM on `/riepilogo-pagamento` to confirm if the 'Indietro' button text or locator strategy has changed.

---

# 3. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
The application displayed a generic Creditor Institution error modal instead of the expected payment notice error message for `PAA_PAGAMENTO_SCONOSCIUTO`.

### Category
application bug

### Recommended action
Verify error mapping logic in the frontend/backend services to ensure `PAA_PAGAMENTO_SCONOSCIUTO` maps to 'Non riusciamo a trovare l’avviso'.

---

# 4. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
```
### Root cause
The locator `#psp-radio-PPAYITR1XXX` failed to load on `/lista-psp` within the 5000 ms timeout during the authenticated checkout flow.

### Category
environment

### Recommended action
Ensure the Postepay PSP option (`PPAYITR1XXX`) is enabled for both standard and authenticated flows in the UAT environment.

---

## Common patterns

- **PSP Availability Issue in UAT Environment**: Tests #1 and #4 failed with the exact same error (`RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms`). This indicates that the Postepay PSP (`PPAYITR1XXX`) is missing or unavailable on `https://uat.checkout.pagopa.it/lista-psp` across both standard and authenticated payment flows.
- **UI Locator Timeout Sensitivity**: 3 out of 4 test failures (#1, #2, #4) are broken due to strict 5000 ms timeouts waiting for UI locators, suggesting potential latency or rendering slowdowns in the UAT environment.