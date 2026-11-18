# 1. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
  File "src/e2e/checkout/steps/back_navigation.py", line 88, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
Element locator for the back button timed out due to page load delay or UI changes on the root URL.

### Category
environment

### Recommended action
Increase the timeout threshold or ensure the element is fully rendered before clicking.

---

# 2. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
  File "src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The Postepay PSP radio button was not rendered within the 5-second timeout on the PSP selection page.

### Category
application bug

### Recommended action
Investigate backend API latency for loading available PSPs or adjust wait times.

---

# 3. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Il pagamento non è andato a buon fine'
- **trace**:
```
  File "src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
```
### Root cause
The payment gateway rejected the transaction, returning a failure message instead of success.

### Category
test data

### Recommended action
Verify the validity of the Worldline test credentials and mock responses in the staging environment.

---

# 4. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
  File "src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
```
### Root cause
The creditor institution (Ente Creditore) mock returned a generic upstream error instead of the expected not-found error.

### Category
environment

### Recommended action
Check the stub/mock configuration for invalid notice codes in the dev environment.

---

# 5. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
  File "src/e2e/checkout/steps/back_navigation.py", line 88, in step_click_button
    locate_and_click(page, BUTTON_SELECTORS[button_text])
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
Timeout trying to locate the 'Indietro' button on the initial checkout page load.

### Category
environment

### Recommended action
Ensure environment stability and adequate network performance during test execution.

---

# 6. La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo
- **status**: failed
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo`
- **message**: AssertionError: Name list not ascending at index 0: 'NEXI PAYMENTS S.P.A.' > 'Mooney S.p.A.'
Full list: ['NEXI PAYMENTS S.P.A.', 'Mooney S.p.A.', 'Intesa Sanpaolo S.p.A.']
- **trace**:
```
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 301, in step_name_list_ascending
    assert cmp <= 0, (
```
### Root cause
The PSP list rendered on the summary page failed to sort alphabetically in ascending order.

### Category
application bug

### Recommended action
File a bug against the frontend sorting logic for the PSP summary page.

---

# 7. La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo
- **status**: failed
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo`
- **message**: AssertionError: Name list not descending at index 0: 'Intesa Sanpaolo S.p.A.' < 'Mooney S.p.A.'
Full list: ['Intesa Sanpaolo S.p.A.', 'Mooney S.p.A.', 'NEXI PAYMENTS S.P.A.']
- **trace**:
```
  File "src/e2e/checkout/steps/psp_sorting_npg.py", line 284, in step_name_list_descending
    assert cmp >= 0, (
```
### Root cause
The PSP list rendered on the summary page failed to sort alphabetically in descending order.

### Category
application bug

### Recommended action
File a bug against the frontend sorting logic for the PSP summary page.

---

# 8. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
  File "src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
Postepay radio button element failed to load on the PSP list page within the allotted timeout.

### Category
application bug

### Recommended action
Investigate intermittent rendering issues or API delays when fetching PSP options.

---

## Common patterns
- **UI Timeouts / Locators**: Multiple failures are caused by element timeouts (`locate_and_click`), specifically for navigation buttons and PSP radio options, pointing towards environment sluggishness or rendering delays.
- **PSP Selection & Sorting**: Failures related to Postepay and PSP sorting indicate issues in the PSP integration layer and frontend data presentation.