# 1. Viene mostrato l'errore PAA_PAGAMENTO_DUPLICATO per codice avviso non valido nell'intervallo 302950100443009424-302950100443009424 -- @1.4
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_DUPLICATO per codice avviso non valido nell'intervallo 302950100443009424-302950100443009424`
- **message**: AssertionError: Expected modal header to contain 'Questo avviso è stato già pagato!', but got: 'Si è verificato un errore imprevisto'
- **trace**:
```
[... earlier frames omitted ...]
    assert expected_header in header_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The application returned a generic error modal ('Si è verificato un errore imprevisto') instead of the specific modal header expected for duplicate payment errors.

### Category
application bug

### Recommended action
Verify error mapping logic in the application frontend for `PAA_PAGAMENTO_DUPLICATO` responses to ensure specific modal messages are displayed.

---

# 2. La lista PSP è ordinata per commissione in ordine crescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione in ordine crescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#paymentSummaryButtonPay' after 5000 ms (url: https://dev.checkout.pagopa.it/inserisci-dati-avviso)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The test timed out after 5000 ms waiting for element `#paymentSummaryButtonPay` on the `/inserisci-dati-avviso` page.

### Category
environment

### Recommended action
Check environment responsiveness and network requests on `/inserisci-dati-avviso` to ensure the summary button renders before timeout.

---

# 3. La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#paymentSummaryButtonPay' after 5000 ms (url: https://dev.checkout.pagopa.it/inserisci-dati-avviso)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The test timed out waiting for `#paymentSummaryButtonPay` to appear on `/inserisci-dati-avviso`.

### Category
environment

### Recommended action
Verify background API performance in the dev environment for notice validation steps.

---

# 4. Opzione login disponibile durante la selezione del metodo di pagamento
- **status**: broken
- **fullName**: `Disponibilità opzione login in tutte le fasi del flusso di pagamento: Opzione login disponibile durante la selezione del metodo di pagamento`
- **message**: RuntimeError: Timeout on locator '#paymentSummaryButtonPay' after 5000 ms (url: https://dev.checkout.pagopa.it/inserisci-dati-avviso)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Timeout occurred waiting for element `#paymentSummaryButtonPay` on `/inserisci-dati-avviso`.

### Category
environment

### Recommended action
Ensure dev environment services are healthy and not delaying DOM element rendering.

---

# 5. La lista PSP è ordinata per commissione nella pagina di selezione PSP
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione nella pagina di selezione PSP`
- **message**: RuntimeError: Timeout on locator '#paymentSummaryButtonPay' after 5000 ms (url: https://dev.checkout.pagopa.it/inserisci-dati-avviso)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Timeout waiting for locator `#paymentSummaryButtonPay` to become actionable on `/inserisci-dati-avviso`.

### Category
environment

### Recommended action
Investigate UI loading delays on notice entry pages in the test environment.

---

# 6. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The browser remained at the root URL (`https://dev.checkout.pagopa.it/`) rather than reaching `/inserisci-carta`, causing locator `button:has-text('Indietro')` to fail.

### Category
environment

### Recommended action
Verify flow initialization and page redirect steps prior to asserting navigation elements.

---

# 7. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#paymentSummaryButtonPay' after 5000 ms (url: https://dev.checkout.pagopa.it/inserisci-dati-avviso)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Timeout waiting for `#paymentSummaryButtonPay` locator on page `/inserisci-dati-avviso`.

### Category
environment

### Recommended action
Verify service responsiveness during payment activation steps in dev environment.

---

# 8. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'Si è verificato un errore imprevisto'
- **trace**:
```
[... earlier frames omitted ...]
    assert expected_header in header_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Application displays generic fallback error text ('Si è verificato un errore imprevisto') instead of the expected 'Non riusciamo a trovare l’avviso'.

### Category
application bug

### Recommended action
Fix error handling logic for `PAA_PAGAMENTO_SCONOSCIUTO` to present user-friendly error headers.

---

# 9. La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#paymentSummaryButtonPay' after 5000 ms (url: https://dev.checkout.pagopa.it/inserisci-dati-avviso)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Locator `#paymentSummaryButtonPay` timed out after 5000 ms on `/inserisci-dati-avviso`.

### Category
environment

### Recommended action
Ensure API backend for notice verification is returning expected payloads in a timely manner.

---

# 10. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#paymentSummaryButtonPay' after 5000 ms (url: https://dev.checkout.pagopa.it/inserisci-dati-avviso)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Timeout locating `#paymentSummaryButtonPay` element on initial notice form page.

### Category
environment

### Recommended action
Monitor dev environment latency for authenticated notice submit endpoints.

---

# 11. Inserimento dati - errori -  Inserimento indirizzo email non valido -- @1.3
- **status**: broken
- **fullName**: `Validazione sintattica dei campi nel funnel di Checkout: Inserimento dati - errori -  Inserimento indirizzo email non valido`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl._frame.py", line 239, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Page navigation failed to reach 'load' event within 15000ms limit.

### Category
environment

### Recommended action
Investigate network latency or hung requests stalling page loads in dev environment.

---

# 12. Viene mostrato l'errore PAA_PAGAMENTO_SCADUTO per codice avviso non valido nell'intervallo 302990000000000000-302999999999999999 -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCADUTO per codice avviso non valido nell'intervallo 302990000000000000-302999999999999999`
- **message**: AssertionError: Expected modal header to contain 'L’avviso è scaduto e non è più possibile pagarlo', but got: 'Si è verificato un errore imprevisto'
- **trace**:
```
[... earlier frames omitted ...]
    assert expected_header in header_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Application failed to display specific expired notice error header, showing generic error modal instead.

### Category
application bug

### Recommended action
Update frontend modal mapping for `PAA_PAGAMENTO_SCADUTO` error codes.

---

# 13. Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.5
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Click sul tasto indietro riporta alla pagina precedente del flusso`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl._frame.py", line 239, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Playwright timed out after 15000ms waiting for page load event during navigation.

### Category
environment

### Recommended action
Check environment network conditions and client routing responsiveness.

---

# 14. Opzione login disponibile durante l'inserimento dell'email
- **status**: broken
- **fullName**: `Disponibilità opzione login in tutte le fasi del flusso di pagamento: Opzione login disponibile durante l'inserimento dell'email`
- **message**: RuntimeError: Timeout on locator '#paymentSummaryButtonPay' after 5000 ms (url: https://dev.checkout.pagopa.it/inserisci-dati-avviso)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Element `#paymentSummaryButtonPay` timed out after 5000 ms on `/inserisci-dati-avviso`.

### Category
environment

### Recommended action
Investigate backend bottlenecks delaying element rendering on initial flow steps.

---

# 15. Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl._frame.py", line 239, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Timeout waiting 15000ms for browser 'load' event on back navigation.

### Category
environment

### Recommended action
Review client-side navigation transitions for unresolved requests or slow environment response.

---

# 16. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#paymentSummaryButtonPay' after 5000 ms (url: https://dev.checkout.pagopa.it/inserisci-dati-avviso)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Locator `#paymentSummaryButtonPay` timed out on `/inserisci-dati-avviso`.

### Category
environment

### Recommended action
Check environment stability during authenticated flow activation.

---

# 17. La lista PSP è ordinata per commissione in ordine decrescente nella pagina di riepilogo
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per commissione in ordine decrescente nella pagina di riepilogo`
- **message**: RuntimeError: Timeout on locator '#paymentSummaryButtonPay' after 5000 ms (url: https://dev.checkout.pagopa.it/inserisci-dati-avviso)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Locator `#paymentSummaryButtonPay` timed out on `/inserisci-dati-avviso`.

### Category
environment

### Recommended action
Verify API speed and frontend rendering times on notice input screens.

---

# 18. Navigazione - Conferma pagina di riepilogo
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Navigazione - Conferma pagina di riepilogo`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl._frame.py", line 239, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Navigation load event timed out after 15000ms.

### Category
environment

### Recommended action
Ensure environment stability and evaluate Playwright wait criteria for route changes.

---

# 19. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#paymentSummaryButtonPay' after 5000 ms (url: https://dev.checkout.pagopa.it/inserisci-dati-avviso)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
Timeout on locator `#paymentSummaryButtonPay` at `/inserisci-dati-avviso`.

### Category
environment

### Recommended action
Inspect notice verification endpoint delays in dev environment.

---

# 20. Viene mostrato il codice di errore per ente creditore non raggiungibile -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato il codice di errore per ente creditore non raggiungibile`
- **message**: AssertionError: Expected modal header to contain 'L’Ente Creditore sta avendo problemi nella risposta', but got: 'Si è verificato un errore imprevisto'
- **trace**:
```
[... earlier frames omitted ...]
    assert expected_header in header_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Application displays generic modal header 'Si è verificato un errore imprevisto' instead of unreachable creditor entity specific message.

### Category
application bug

### Recommended action
Ensure domain error codes corresponding to unreachable creditor entities display dedicated UI error messages.

---

## Common patterns

Two primary failure patterns account for all test failures in this run:

1. **Unmapped/Generic Error Modals (Application Bugs)**:
   - **Occurrences**: Tests 1, 8, 12, 20 (`status: failed`).
   - **Pattern**: Tests expecting specific business error messages (e.g., duplicate payment, unknown payment, expired notice, unreachable creditor) consistently receive the generic fallback modal header `'Si è verificato un errore imprevisto'`. This indicates a regression or missing error translation layer in the frontend UI component.

2. **Environment & Navigation Timeouts (Environment Issues)**:
   - **Occurrences**: Tests 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19 (`status: broken`).
   - **Pattern**:
     - *Locator Timeouts*: Repeated timeouts waiting 5000 ms for `#paymentSummaryButtonPay` on `https://dev.checkout.pagopa.it/inserisci-dati-avviso`.
     - *Navigation Timeouts*: Playwright timing out (15000 ms) waiting for page `load` events during navigation transitions.
     These errors suggest severe backend latency or temporary environment unresponsiveness in `dev.checkout.pagopa.it`.