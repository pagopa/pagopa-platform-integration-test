# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The specific PSP radio button element `#psp-radio-PPAYITR1XXX` did not load within the 5000ms timeout on the PSP list page.

### Category
environment

### Recommended action
Verify if the target PSP service/configuration (`PPAYITR1XXX`) is active in the DEV environment and increase the wait timeout if rendering is slow.

---

# 2. La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The PSP radio element `#psp-radio-BCITITMM` failed to render within the default 5-second timeout.

### Category
environment

### Recommended action
Ensure PSP list API endpoints are returning mock/real PSP entries promptly in the DEV environment.

---

# 3. La lista PSP è ordinata per commissione nella pagina di selezione PSP
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione nella pagina di selezione PSP`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 5000ms exceeded.
Call log:
  - waiting for locator(".pspFeeName").first to be visible
- **trace**:
```
[... earlier frames omitted ...]
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_connection.py", line 558, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
```
### Root cause
Elements with class `.pspFeeName` did not become visible within 5000ms, indicating the PSP list failed to populate or load.

### Category
environment

### Recommended action
Check backend response times for PSP fees and adjust explicit wait timeouts in test assertions.

---

# 4. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
[... earlier frames omitted ...]
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Mismatch in error handling logic: system returned a general Creditor Entity error instead of the expected unknown payment modal header.

### Category
application bug

### Recommended action
Investigate API error code mapping for unknown notice codes (PAA_PAGAMENTO_SCONOSCIUTO) and update application error modal display.

---

# 5. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Locator `#psp-radio-PPAYITR1XXX` was not clickable within 5000ms on the PSP list page during authenticated flow.

### Category
environment

### Recommended action
Investigate PSP list API latency and stability in the test environment.

---

# 6. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The back button `button:has-text('Indietro')` was not found/visible after redirecting to `https://dev.checkout.pagopa.it/`.

### Category
application bug

### Recommended action
Verify navigation routing behavior when clicking back from `/inserisci-carta` to ensure the landing page renders expected controls.

---

# 7. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-WOLLNLB1' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The locator `#psp-radio-WOLLNLB1` timed out waiting to appear on the PSP selection screen.

### Category
environment

### Recommended action
Check backend services serving Worldpay PSP options on `dev.checkout.pagopa.it`.

---

# 8. La lista PSP è ordinata per commissione in ordine decrescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione in ordine decrescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Locator `#psp-radio-BCITITMM` did not render within 5000ms timeout on the PSP list page.

### Category
environment

### Recommended action
Ensure environment stability and review API latency for retrieving PSP list data.

---

# 9. La lista PSP è ordinata per nome nella pagina di selezione PSP
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome nella pagina di selezione PSP`
- **message**: playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 5000ms exceeded.
Call log:
  - waiting for locator(".pspFeeName").first to be visible
- **trace**:
```
[... earlier frames omitted ...]
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/playwright/_impl/_connection.py", line 558, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
```
### Root cause
Timeout waiting for `.pspFeeName` locator on PSP selection page due to unpopulated or slow loading list.

### Category
environment

### Recommended action
Investigate PSP list rendering performance and extend timeout duration for dynamic PSP fee elements.

---

# 10. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BNLIITRR' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Locator `#psp-radio-BNLIITRR` timed out on `/lista-psp` page after 5000ms.

### Category
environment

### Recommended action
Verify configuration and availability of Wordline PSP (`BNLIITRR`) in the test environment.

---

# 11. Flusso lista PSP - indietro da /scegli-metodo (metodo APM)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (metodo APM)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The back button `button:has-text('Indietro')` was not found on the `/lista-psp` page within 5000ms.

### Category
application bug

### Recommended action
Check UI layout and button locator text on the `/lista-psp` page to ensure back navigation control is rendered properly.

---

# 12. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-WOLLNLB1' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Element `#psp-radio-WOLLNLB1` was missing or timed out on `/lista-psp` page during authenticated checkout flow.

### Category
environment

### Recommended action
Confirm backend PSP availability for authenticated users in the dev environment.

---

# 13. La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Locator `#psp-radio-BCITITMM` timed out after 5000ms waiting to be displayed on `/lista-psp`.

### Category
environment

### Recommended action
Verify responsiveness of PSP list API endpoints under test load.

---

# 14. Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.6
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Click sul tasto indietro riporta alla pagina precedente del flusso`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The step helper failed to locate `button:has-text('Indietro')` on page `/lista-psp` within 5000ms timeout.

### Category
application bug

### Recommended action
Audit DOM structure on `/lista-psp` to confirm the back button selector matches application code.

---

# 15. Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento`
- **message**: RuntimeError: Timeout on locator '#psp-radio-MOONITMMXXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, "#psp-radio-MOONITMMXXX")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Locator `#psp-radio-MOONITMMXXX` failed to appear within 5000ms on the PSP selection screen.

### Category
environment

### Recommended action
Ensure test configuration for `MOONITMMXXX` PSP is valid in the test database.

---

# 16. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BNLIITRR' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Timeout locating `#psp-radio-BNLIITRR` on the PSP list page during authenticated flow execution.

### Category
environment

### Recommended action
Check backend services serving Wordline PSP options for authenticated users.

---

# 17. La lista PSP è ordinata per commissione in ordine crescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione in ordine crescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-BCITITMM' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Locator `#psp-radio-BCITITMM` timed out after 5 seconds on the PSP selection page.

### Category
environment

### Recommended action
Investigate PSP list rendering delays in the DEV integration environment.

---

# 18. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
[... earlier frames omitted ...]
    locate_and_click(page, BUTTON_SELECTORS[button_text])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The back button `button:has-text('Indietro')` was not found within 5000ms after navigating to `https://dev.checkout.pagopa.it/`.

### Category
application bug

### Recommended action
Verify back button visibility and page state during navigation back from `/scegli-metodo`.

---

## Common patterns

1. **PSP List Element Loading Failure (Environment / Latency)**: 13 out of 18 failures stem from timeouts trying to locate specific PSP radio buttons (`#psp-radio-*`) or PSP list items (`.pspFeeName`) on the `/lista-psp` page within the default 5000ms timeout window. This indicates backend PSP service slowdowns or missing mock PSP data in `dev.checkout.pagopa.it`.
2. **Missing Back Navigation Button (Application Bug)**: 4 tests failed due to timeouts locating `button:has-text('Indietro')` across linear navigation flows (at root URL `/` and `/lista-psp`), pointing to UI layout regressions or missing elements during backward navigation.
3. **Error Modal Message Mismatch (Application Bug)**: Failure #4 highlights an incorrect modal message displayed for an unknown payment notice code, returning generic entity errors instead of the specific user-facing message.