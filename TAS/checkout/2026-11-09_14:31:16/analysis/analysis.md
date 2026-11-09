# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The PSP selection radio element `#psp-radio-PPAYITR1XXX` failed to load on `/lista-psp` within 5 seconds, indicating missing PSP configuration in DEV environment.

### Category
test data

### Recommended action
Verify that the Postepay PSP (`PPAYITR1XXX`) is seeded and returned by the PSP list backend service in the DEV environment.

---

# 2. Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
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
The application unexpectedly redirected back to the root landing page (`https://dev.checkout.pagopa.it/`) where the 'Indietro' button does not exist.

### Category
application bug

### Recommended action
Investigate client-side route state management when navigating backward from `/inserisci-carta` with `enablePspPage=true` enabled.

---

# 3. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
The backend returned a generic Creditor Institution error instead of the expected `PAA_PAGAMENTO_SCONOSCIUTO` error mapping for notice codes in the specified range.

### Category
application bug

### Recommended action
Verify error mapping logic in the API gateway/backend service for notice code ranges to ensure `PAA_PAGAMENTO_SCONOSCIUTO` is correctly mapped.

---

# 4. Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
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
The application lost checkout session state and redirected to the root URL (`https://dev.checkout.pagopa.it/`) where the back button is unavailable.

### Category
application bug

### Recommended action
Ensure session state and previous route history are correctly preserved when back action is triggered from `/scegli-metodo`.

---

# 5. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
The PSP radio option `#psp-radio-PPAYITR1XXX` was not present on `/lista-psp` during the authenticated user flow.

### Category
test data

### Recommended action
Verify Postepay PSP availability in the DEV backend service response for authenticated user contexts.

---

## Common patterns

1. **Missing Postepay PSP Config (Failures 1 & 5)**: Both standard and authenticated Postepay payment scenarios fail because locator `#psp-radio-PPAYITR1XXX` is missing from `/lista-psp`. This points to missing or misconfigured test data for PSP `PPAYITR1XXX` in the DEV environment.
2. **Unexpected Fallback Redirect to Root (Failures 2 & 4)**: Navigation flows testing backward movement (`Indietro`) fail because the application drops checkout session context and redirects users back to the root URL (`https://dev.checkout.pagopa.it/`), where navigation buttons no longer exist.