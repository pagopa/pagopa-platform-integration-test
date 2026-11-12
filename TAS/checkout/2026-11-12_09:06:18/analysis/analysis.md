# 1. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The back button (`button:has-text('Indietro')`) was not rendered or interactable within 5000 ms on the target page.

### Category
application bug

### Recommended action
Verify back button component rendering logic and state management when navigating back from `/scegli-metodo`.

---

# 2. Navigazione - Scelta metodo di pagamento “Carte di Credito”
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Navigazione - Scelta metodo di pagamento “Carte di Credito”`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 239, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Page load navigation timed out after 15000 ms due to environment unresponsiveness or slow network requests.

### Category
environment

### Recommended action
Investigate dev server response times and API latency during payment method selection navigation.

---

# 3. La lista PSP è ordinata per commissione nella pagina di selezione PSP
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
The pay summary button (`#paymentSummaryButtonPay`) failed to load or appear on `/inserisci-dati-avviso` within 5000 ms.

### Category
application bug

### Recommended action
Check notice data form validation and payment summary button rendering conditions on `/inserisci-dati-avviso`.

---

# 4. Viene mostrato l'errore PAA_PAGAMENTO_SCADUTO per codice avviso non valido nell'intervallo 302990000000000000-302999999999999999 -- @1.2
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
Backend returned a generic error modal instead of the specific `PAA_PAGAMENTO_SCADUTO` message for expired notices.

### Category
application bug

### Recommended action
Fix backend error mapping for notice ranges `302990000000000000-302999999999999999` to return proper expired notice error details.

---

# 5. Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.3
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Click sul tasto indietro riporta alla pagina precedente del flusso`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 239, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Browser navigation failed to complete the 'load' event within 15000 ms upon clicking the back button.

### Category
environment

### Recommended action
Ensure frontend routing handles back navigation gracefully without triggering hanging network calls.

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
Locator `button:has-text('Indietro')` timed out on the landing page URL after an unexpected redirect or missing UI component.

### Category
application bug

### Recommended action
Verify back button presence and route destination consistency when backing out of card insertion.

---

# 7. La lista PSP è ordinata per nome nella pagina di selezione PSP
- **status**: broken
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome nella pagina di selezione PSP`
- **message**: RuntimeError: Timeout on locator '#paymentSummaryButtonPay' after 5000 ms (url: https://dev.checkout.pagopa.it/inserisci-dati-avviso)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The payment action button `#paymentSummaryButtonPay` was not rendered within 5000 ms on `/inserisci-dati-avviso`.

### Category
application bug

### Recommended action
Ensure step progression logic on the notice data page displays `#paymentSummaryButtonPay` reliably.

---

# 8. Opzione login disponibile durante la selezione del metodo di pagamento
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
Test timed out waiting for `#paymentSummaryButtonPay` on the notice page before reaching method selection.

### Category
application bug

### Recommended action
Investigate why notice submission fails to present `#paymentSummaryButtonPay` to proceed.

---

# 9. Flusso lista PSP - indietro da /scegli-metodo (metodo APM)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (metodo APM)`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 239, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Playwright navigation timeout (15000 ms) waiting for page load while navigating back from APM selection.

### Category
environment

### Recommended action
Check dev network stability and APM route transition performance.

---

# 10. Inserimento dati - errori -  Click sul tasto continua con campo non compilato -- @1.3
- **status**: broken
- **fullName**: `Validazione sintattica dei campi nel funnel di Checkout: Inserimento dati - errori -  Click sul tasto continua con campo non compilato`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 239, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Navigation load event timed out after 15000 ms during notice data form validation flow.

### Category
environment

### Recommended action
Verify if page load event hangs when submitting incomplete notice form inputs.

---

# 11. La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo
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
Locator `#paymentSummaryButtonPay` timed out after 5000 ms on `/inserisci-dati-avviso`.

### Category
application bug

### Recommended action
Fix rendering of `#paymentSummaryButtonPay` during the notice data insertion step.

---

# 12. Opzione login disponibile durante l'inserimento dell'email
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
Locator `#paymentSummaryButtonPay` timed out after 5000 ms on `/inserisci-dati-avviso`.

### Category
application bug

### Recommended action
Ensure notice details can be submitted properly to reveal `#paymentSummaryButtonPay`.

---

# 13. Inserimento dati - errori - indirizzo email diverso da ripeti
- **status**: broken
- **fullName**: `Validazione sintattica dei campi nel funnel di Checkout: Inserimento dati - errori - indirizzo email diverso da ripeti`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 239, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Playwright navigation load event timed out after 15000 ms during email field validation test.

### Category
environment

### Recommended action
Investigate frontend client routing and ensure network calls do not block page load events.

---

# 14. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
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
Locator `#paymentSummaryButtonPay` timed out after 5000 ms on `/inserisci-dati-avviso`.

### Category
application bug

### Recommended action
Fix notice details step submission to enable proceeding to Worldpay card payment configuration.

---

# 15. Viene mostrato l'errore PAA_PAGAMENTO_DUPLICATO per codice avviso non valido nell'intervallo 302950100443009424-302950100443009424 -- @1.4
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
Backend error mapping failed to return duplicate payment header, rendering generic error 'Si è verificato un errore imprevisto'.

### Category
application bug

### Recommended action
Ensure duplicate notice backend responses map to `PAA_PAGAMENTO_DUPLICATO` modal text.

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
Locator `#paymentSummaryButtonPay` timed out after 5000 ms on `/inserisci-dati-avviso`.

### Category
application bug

### Recommended action
Investigate notice form submission failure preventing button appearance in Wordline payment flow.

---

# 17. Inserimento dati - errori -  Inserimento indirizzo email non valido -- @1.2
- **status**: broken
- **fullName**: `Validazione sintattica dei campi nel funnel di Checkout: Inserimento dati - errori -  Inserimento indirizzo email non valido`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 239, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Page load navigation timed out after 15000 ms on invalid email syntax test case.

### Category
environment

### Recommended action
Check environment responsiveness and page navigation lifecycle handling during form validation errors.

---

# 18. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
Locator `#paymentSummaryButtonPay` timed out after 5000 ms on `/inserisci-dati-avviso`.

### Category
application bug

### Recommended action
Ensure `#paymentSummaryButtonPay` renders correctly during Postepay authenticated checkout flows.

---

# 19. Navigazione - pagina dati avviso
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Navigazione - pagina dati avviso`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 239, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Page load navigation timed out after 15000 ms navigating to the notice data page.

### Category
environment

### Recommended action
Verify dev environment backend readiness and frontend page load performance.

---

# 20. Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento`
- **message**: playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
=========================== logs ===========================
waiting for navigation until 'load'
============================================================
- **trace**:
```
[... earlier frames omitted ...]
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 239, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Navigation 'load' event timed out after 15000 ms during back button history navigation.

### Category
environment

### Recommended action
Check client history state updates to ensure backward navigation does not hang page loading.

---

## Common patterns

1. **Unrendered Pay Summary Button (`#paymentSummaryButtonPay`)**: Multiple tests across PSP sorting, login options, and payment method flows (Worldpay, Wordline, Postepay) failed due to a 5000 ms timeout waiting for `#paymentSummaryButtonPay` on `/inserisci-dati-avviso`. This points to a recurring UI block or form submission issue on the notice input page.
2. **Page Navigation Timeouts**: A large cluster of navigation tests failed with Playwright's `TimeoutError: Timeout 15000ms exceeded` waiting for the page `load` event. This indicates dev environment latency or slow asset/API loading.
3. **Unhandled Backend Error Responses**: Activation error tests failed because the application displayed a generic modal header ('Si è verificato un errore imprevisto') instead of specific domain error messages like `PAA_PAGAMENTO_SCADUTO` or `PAA_PAGAMENTO_DUPLICATO`.