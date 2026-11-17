# 1. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
Navigation failed to reach or maintain the step containing the "Indietro" button within 5 seconds, resetting to the root URL (`https://dev.checkout.pagopa.it/`).

### Category
application bug

### Recommended action
Investigate route transition and session state preservation when navigating backwards in the card insertion flow.

---

# 2. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
The specific Postepay PSP element (`#psp-radio-PPAYITR1XXX`) was missing from the `/lista-psp` page within the 5-second timeout.

### Category
test data

### Recommended action
Verify that the Postepay PSP (`PPAYITR1XXX`) is enabled and available in the target dev environment catalog.

---

# 3. La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo
- **status**: failed
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo`
- **message**: AssertionError: Name list not ascending at index 0: 'NEXI PAYMENTS S.P.A.' > 'Mooney S.p.A.'
Full list: ['NEXI PAYMENTS S.P.A.', 'Mooney S.p.A.', 'Intesa Sanpaolo S.p.A.']
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
The application sorted the PSP list in descending alphabetical order when ascending order was expected.

### Category
application bug

### Recommended action
Fix the ascending sorting comparator logic on the frontend summary page.

---

# 4. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
The backend mock returned a generic creditor institution error header instead of the specific unknown payment notice header (`PAA_PAGAMENTO_SCONOSCIUTO`).

### Category
environment

### Recommended action
Update the backend/mock response mapping for notice codes in range `302400000000000000-302409999999999999` to return the appropriate error code.

---

# 5. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Il pagamento non è andato a buon fine'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
The payment transaction processed through the Worldline configuration failed instead of succeeding.

### Category
application bug

### Recommended action
Inspect payment gateway integration logs for Worldline to determine why the transaction was declined or failed.

---

# 6. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
- **status**: broken
- **fullName**: `Navigazione Lineare per il flusso di Pagamento: Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)`
- **message**: RuntimeError: Timeout on locator 'button:has-text('Indietro')' after 5000 ms (url: https://dev.checkout.pagopa.it/)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
Back navigation from `/scegli-metodo` triggered an unexpected fallback/redirect to the root landing page (`https://dev.checkout.pagopa.it/`), where the back button locator timed out.

### Category
application bug

### Recommended action
Fix history/state handling when navigating back from payment method selection step with saved wallets.

---

# 7. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://dev.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
The Postepay radio button `#psp-radio-PPAYITR1XXX` failed to render on `/lista-psp` during authenticated checkout flows.

### Category
test data

### Recommended action
Ensure the Postepay PSP record `PPAYITR1XXX` is active and returned by backend APIs for authenticated user flows.

---

# 8. La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo
- **status**: failed
- **fullName**: `Ordinamento lista PSP in Checkout: La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo`
- **message**: AssertionError: Name list not descending at index 0: 'Intesa Sanpaolo S.p.A.' < 'Mooney S.p.A.'
Full list: ['Intesa Sanpaolo S.p.A.', 'Mooney S.p.A.', 'NEXI PAYMENTS S.P.A.']
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```
### Root cause
The application sorted the PSP list in ascending alphabetical order when descending order was expected.

### Category
application bug

### Recommended action
Fix the descending sorting comparator logic on the frontend summary page.

---

## Common patterns

1. **Inverted Frontend PSP Sorting**: Failures #3 and #8 demonstrate that the PSP list sorting logic on the summary page is completely inverted (ascending request returns descending order, and descending request returns ascending order).
2. **Missing Postepay PSP in API/Environment**: Failures #2 and #7 both fail to locate `#psp-radio-PPAYITR1XXX` on `/lista-psp`, indicating that the Postepay PSP provider data is missing or inactive in the dev environment configuration.
3. **Unexpected Redirect to Root during Back Navigation**: Failures #1 and #6 fail because navigating back unexpectedly resets the page URL to `https://dev.checkout.pagopa.it/` instead of staying within the checkout wizard context.