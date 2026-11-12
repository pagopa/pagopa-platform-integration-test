# 1. Navigazione - pagina dati avviso
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
Navigation step exceeded Playwright's 15000ms timeout waiting for the page load event.

### Category
environment

### Recommended action
Investigate frontend bundle loading speeds and backend API latency in dev environment, or increase test navigation timeout.

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
Page navigation timed out after 15000ms while transitioning to payment method selection.

### Category
environment

### Recommended action
Check environment performance and API responsiveness during payment method selection transitions.

---

# 3. Click sul tasto indietro riporta alla pagina precedente del flusso -- @1.5
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
Backward navigation exceeded the 15000ms threshold waiting for the page load state.

### Category
environment

### Recommended action
Review server response times and frontend routing overhead when navigating back.

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
The action failed on `/inserisci-dati-avviso` because selector `#paymentSummaryButtonPay` was not rendered within 5000ms.

### Category
application bug

### Recommended action
Inspect notice input form submission logic and verify if the pay button DOM selector or condition changed.

---

# 5. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
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
The test unexpectedly redirected to root URL `https://dev.checkout.pagopa.it/` where `button:has-text('Indietro')` was missing.

### Category
application bug

### Recommended action
Fix client-side routing logic for back navigation from `/inserisci-carta` when `enablePspPage=true`.

---

# 6. Inserimento dati - errori - Inserimento indirizzo email non valido -- @1.2
- **status**: broken
- **fullName**: `Validazione sintattica dei campi nel funnel di Checkout: Inserimento dati - errori - Inserimento indirizzo email non valido`
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
Navigation load event timed out after 15000ms during email input validation test setup.

### Category
environment

### Recommended action
Verify host responsiveness and stabilize test environment load capacity.

---

# 7. La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo
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
Failed to proceed from `/inserisci-dati-avviso` because `#paymentSummaryButtonPay` locator timed out.

### Category
application bug

### Recommended action
Ensure form validation on notice data step completes and pay button renders correctly.

---

# 8. Flusso lista PSP - indietro da /scegli-metodo (metodo APM)
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
Navigation timeout (15000ms) exceeded during APM back-navigation sequence.

### Category
environment

### Recommended action
Investigate network degradation and API delays when triggering back navigation from payment choice.

---

# 9. Navigazione - Conferma pagina di riepilogo
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Navigazione - Conferma pagina di riepilogo`
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
Page load event timed out while attempting to navigate to summary confirmation page.

### Category
environment

### Recommended action
Audit backend service response times during summary page retrieval.

---

# 10. La lista PSP è ordinata per commissione nella pagina di selezione PSP
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
Element `#paymentSummaryButtonPay` was not available on `/inserisci-dati-avviso` page within timeout.

### Category
application bug

### Recommended action
Check notice entry form handler to ensure transition button renders properly.

---

# 11. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#paymentSummaryButtonPay' after 5000 ms (url: https://dev.checkout.pagopa.it/inserisci-dati-avviso)
- **trace**:
```
[... earlier frames omitted ...]
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The payment activation test stalled on `/inserisci-dati-avviso` due to `#paymentSummaryButtonPay` locator timeout.

### Category
application bug

### Recommended action
Verify notice input submit functionality and ensure form submission payload format is valid.

---

# 12. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
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
Authenticated user flow stuck on `/inserisci-dati-avviso` due to `#paymentSummaryButtonPay` missing from DOM.

### Category
application bug

### Recommended action
Ensure authenticated state does not disable or alter the pay button locator.

---

# 13. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
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
Locator `#paymentSummaryButtonPay` timed out after 5000ms while processing notice data.

### Category
application bug

### Recommended action
Fix notice details form submit flow to render the next page/action button correctly.

---

# 14. La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo
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
Unable to progress past `/inserisci-dati-avviso` due to `#paymentSummaryButtonPay` timeout.

### Category
application bug

### Recommended action
Investigate front-end state management on `/inserisci-dati-avviso`.

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
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/playwright/_impl/_frame.py", line 239, in continuation
    event = await waiter.result()
            ^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Playwright navigation timeout exceeded 15000ms during successive back navigation actions.

### Category
environment

### Recommended action
Inspect history navigation handling and network load during back navigation.

---

# 16. La lista PSP è ordinata per commissione in ordine decrescente nella pagina di riepilogo
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
Locator `#paymentSummaryButtonPay` timed out after 5000ms on `/inserisci-dati-avviso`.

### Category
application bug

### Recommended action
Debug notice input form behavior preventing progression to the PSP summary list.

---

# 17. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
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
Locator `#paymentSummaryButtonPay` failed to appear within 5000ms during authenticated payment flow.

### Category
application bug

### Recommended action
Ensure notice details page handles authenticated state correctly and renders the pay button.

---

# 18. Viene mostrato l'errore PAA_PAGAMENTO_DUPLICATO per codice avviso non valido nell'intervallo 302950100443009424-302950100443009424 -- @1.4
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
Application returned generic error modal ('Si è verificato un errore imprevisto') instead of specific duplicate payment error message.

### Category
application bug

### Recommended action
Fix backend/frontend mapping for `PAA_PAGAMENTO_DUPLICATO` error code to display the expected duplicate notice message modal.

---

# 19. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
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
The back button click caused an unexpected redirect to root URL `https://dev.checkout.pagopa.it/`, where 'Indietro' button does not exist.

### Category
application bug

### Recommended action
Correct client routing when navigating back from `/scegli-metodo` with saved wallet and `enablePspPage=true`.

---

# 20. Inserimento dati - errori - Click sul tasto continua con campo non compilato -- @1.3
- **status**: broken
- **fullName**: `Validazione sintattica dei campi nel funnel di Checkout: Inserimento dati - errori - Click sul tasto continua con campo non compilato`
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
Page navigation timed out after 15000ms waiting for the page load event.

### Category
environment

### Recommended action
Check environment performance and increase global Playwright navigation timeout setting.

---

## Common patterns

1. **Notice Form Blocked (`#paymentSummaryButtonPay` locator timeout):**
   - 9 failures (Tests #4, #7, #10, #11, #12, #13, #14, #16, #17) failed at URL `https://dev.checkout.pagopa.it/inserisci-dati-avviso` because selector `#paymentSummaryButtonPay` was not rendered within 5000ms. This indicates a major regression or blocking issue on the notice input form.

2. **Navigation Load Timeouts (`Timeout 15000ms exceeded`):**
   - 8 failures (Tests #1, #2, #3, #6, #8, #9, #15, #20) were caused by Playwright timing out while waiting for navigation `load` events, pointing to high environment latency or unhandled background requests in `dev.checkout.pagopa.it`.

3. **Unexpected Redirect on Back-Navigation:**
   - Tests #5 and #19 failed because triggering back navigation sent the application back to the root path (`https://dev.checkout.pagopa.it/`) where expected action buttons were absent, revealing a client-side routing regression when `enablePspPage=true`.