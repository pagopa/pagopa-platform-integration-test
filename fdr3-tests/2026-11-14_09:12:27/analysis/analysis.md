## Suite: checkout

# 1. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato me con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
```
### Root cause
Payment confirmation timed out or remained pending, returning an intermediate status message ('Attendi la conferma del pagamento') instead of final success.

### Category
flaky

### Recommended action
Increase the polling/wait duration for final payment status confirmation before asserting the UI text.

---

# 2. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The PSP option `#psp-radio-PPAYITR1XXX` failed to load/render on the `/lista-psp` page within the 5-second timeout.

### Category
environment

### Recommended action
Verify availability of the Postepay PSP configuration in UAT or adjust DOM wait explicit timeout.

---

# 3. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
```
### Root cause
The PSP option `#psp-radio-PPAYITR1XXX` failed to load on the `/lista-psp` page within the timeout during unauthenticated checkout.

### Category
environment

### Recommended action
Check backend services serving the PSP list in UAT environment.

---

# 4. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Attendi la conferma del pagamento'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
```
### Root cause
Payment confirmation stayed in pending state during authenticated payment flow for Wordline provider.

### Category
flaky

### Recommended action
Implement an explicit wait retry mechanism for the asynchronous payment finalization status.

---

# 5. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
```
### Root cause
The mock/upstream service returned a generic Creditor Entity error instead of the specific unknown notice error modal text.

### Category
application bug

### Recommended action
Verify error mapping for `PAA_PAGAMENTO_SCONOSCIUTO` in the gateway/backend service.

---

## Common patterns
- **Asynchronous status delays**: Tests expecting immediate payment completion encountered pending UI states.
- **PSP list UI timeouts**: Missing or delayed rendering of specific PSP elements (`#psp-radio-PPAYITR1XXX`).


## Suite: fdr3

No test failures found in the 'FDR-3' suite execution.


## Suite: wisp

# 1. L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "7ecfddb0-4df4-4b2d-83ab-b1862dbb2046" }
- **trace**:
```

```
### Root cause
Backend API threw an unhandled internal server error (HTTP 500) and returned JSON instead of expected XML response.

### Category
application bug

### Recommended action
Inspect backend application logs using activityId `7ecfddb0-4df4-4b2d-83ab-b1862dbb2046` to identify the root cause of the crash.

---

# 2. Utente paga un pagamento singolo con cinque versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con cinque versamenti e nessuna marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "405ab2ac-58d0-4ffe-9ed7-20dbf6738346" }
- **trace**:
```

```
### Root cause
Backend endpoint returned HTTP 500 Internal Server Error when processing single payment with multiple transfers.

### Category
application bug

### Recommended action
Investigate backend logs for activityId `405ab2ac-58d0-4ffe-9ed7-20dbf6738346`.

---

# 3. L'utente paga un carrello con due RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT per un totale di cinque versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "77d14630-c791-4a3c-b36a-83fbbb6d8a7e" }
- **trace**:
```

```
### Root cause
Backend service failed with HTTP status 500 during multi-RPT cart processing.

### Category
application bug

### Recommended action
Check backend system logs using activityId `77d14630-c791-4a3c-b36a-83fbbb6d8a7e`.

---

# 4. L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "2ef41177-524c-48cd-bfb7-909eedc32542" }
- **trace**:
```

```
### Root cause
HTTP status 500 returned during multi-beneficiary cart operations.

### Category
application bug

### Recommended action
Examine server-side logs for activityId `2ef41177-524c-48cd-bfb7-909eedc32542`.

---

# 5. L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "472dd2d1-f81a-4cc6-8d56-24a2ea499fb7" }
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) thrown when interacting with existing debt position in GPD.

### Category
application bug

### Recommended action
Debug backend handling for GPD integration via activityId `472dd2d1-f81a-4cc6-8d56-24a2ea499fb7`.

---

# 6. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "c7c77d16-1201-4c4c-b255-df816235552a" }
- **trace**:
```

```
### Root cause
HTTP status 500 returned for payment request containing stamp duty (marca da bollo).

### Category
application bug

### Recommended action
Investigate server logs with activityId `c7c77d16-1201-4c4c-b255-df816235552a`.

---

# 7. Utente paga un pagamento singolo con due versamenti semplici e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti semplici e una marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "cea99c12-905f-4a89-8589-9b5cb9959349" }
- **trace**:
```

```
### Root cause
Backend returned internal server error when processing RPT with single payment and stamp duty.

### Category
application bug

### Recommended action
Check backend service logs using activityId `cea99c12-905f-4a89-8589-9b5cb9959349`.

---

# 8. Utente tenta il pagamento, poi riprova il flusso ma fallisce
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente tenta il pagamento, poi riprova il flusso ma fallisce`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "c4cdc4c9-c428-40a7-a649-8097b8dc11b6" }
- **trace**:
```

```
### Root cause
HTTP 500 returned upon retrying payment workflow.

### Category
application bug

### Recommended action
Analyze server activity for activityId `c4cdc4c9-c428-40a7-a649-8097b8dc11b6`.

---

# 9. Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "dd8ca334-f320-472e-a6bf-738c01f55bad" }
- **trace**:
```

```
### Root cause
System failure resulting in HTTP 500 on multi-stamp payment execution.

### Category
application bug

### Recommended action
Review application logs corresponding to activityId `dd8ca334-f320-472e-a6bf-738c01f55bad`.

---

# 10. L'utente paga un carrello con tre RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT con un versamento ciascuna`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "a95d8fd8-ad1a-4df8-8782-4443578048e6" }
- **trace**:
```

```
### Root cause
HTTP status 500 on triple-RPT cart payment execution.

### Category
application bug

### Recommended action
Trace activityId `a95d8fd8-ad1a-4df8-8782-4443578048e6` in application telemetry.

---

# 11. L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "b495d2cf-a75a-4224-bf35-f8da7ad5cff3" }
- **trace**:
```

```
### Root cause
Internal server error (HTTP 500) during execution of cart containing mixed RPT payments and stamps.

### Category
application bug

### Recommended action
Investigate logs for activityId `b495d2cf-a75a-4224-bf35-f8da7ad5cff3`.

---

# 12. L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "a7120478-cd8b-4905-b7fc-f5ad39ed64f5" }
- **trace**:
```

```
### Root cause
Backend 500 Internal Server Error when processing existing GPD stamp duty position.

### Category
application bug

### Recommended action
Inspect service logs associated with activityId `a7120478-cd8b-4905-b7fc-f5ad39ed64f5`.

---

# 13. L'utente paga un carrello con singola RPT con un versamento
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "89fb8ca3-ac51-458c-b0bb-cf08737864aa" }
- **trace**:
```

```
### Root cause
Backend returned HTTP status 500 instead of a valid XML response for simple RPT cart.

### Category
application bug

### Recommended action
Check backend system telemetry for activityId `89fb8ca3-ac51-458c-b0bb-cf08737864aa`.

---

# 14. L'utente paga un carrello con cinque RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con cinque RPT con un versamento ciascuna`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "bda6d06a-b5fc-45f6-8009-4f47f8e3d2e8" }
- **trace**:
```

```
### Root cause
HTTP 500 error raised during multi-RPT cart processing.

### Category
application bug

### Recommended action
Examine server logs using activityId `bda6d06a-b5fc-45f6-8009-4f47f8e3d2e8`.

---

# 15. L'utente paga un carrello con tre RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di cinque versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "129854a3-5625-4df5-afb4-fc8e9cead4f8" }
- **trace**:
```

```
### Root cause
Unhandled backend server error returning HTTP status 500.

### Category
application bug

### Recommended action
Analyze server logs associated with activityId `129854a3-5625-4df5-afb4-fc8e9cead4f8`.

---

# 16. L'utente paga un carrello con tre RPT per un totale di dieci versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di dieci versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "95489345-7e7e-4e75-acbb-278de0dac76a" }
- **trace**:
```

```
### Root cause
HTTP status 500 returned on complex multi-RPT payment request.

### Category
application bug

### Recommended action
Trace activityId `95489345-7e7e-4e75-acbb-278de0dac76a` in backend logs.

---

# 17. L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "90b52019-5951-4efa-a97a-8e768348810c" }
- **trace**:
```

```
### Root cause
Server crash/error (HTTP 500) processing multi-transfer cart existing in GPD.

### Category
application bug

### Recommended action
Check backend logs for activityId `90b52019-5951-4efa-a97a-8e768348810c`.

---

# 18. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "5d637965-d6fa-4dd8-b690-5baede13dfcc" }
- **trace**:
```

```
### Root cause
Backend returned HTTP status 500 during simple `nodoInviaRPT` execution.

### Category
application bug

### Recommended action
Inspect application logs for activityId `5d637965-d6fa-4dd8-b690-5baede13dfcc`.

---

# 19. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "6601d215-29c7-4d62-8098-f3019b9e7976" }
- **trace**:
```

```
### Root cause
HTTP 500 error response returned for single RPT cart with stamp duty.

### Category
application bug

### Recommended action
Investigate backend activityId `6601d215-29c7-4d62-8098-f3019b9e7976`.

---

# 20. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 500. Body: { "statusCode": 500, "message": "Internal server error", "activityId": "c7c2bf01-109e-4ff8-8e47-8d94f322e9fd" }
- **trace**:
```

```
### Root cause
HTTP 500 response returned on cart execution targeting existing GPD positions.

### Category
application bug

### Recommended action
Check application logs for activityId `c7c2bf01-109e-4ff8-8e47-8d94f322e9fd`.

---

## Common patterns
- **Systemic Backend 500 Internal Server Errors**: All failing tests across WISP endpoints (`nodoInviaRPT`, `nodoInviaCarrelloRPT`) received JSON HTTP status 500 responses instead of standard XML SOAP envelopes, pointing to a single backend crash or downstream service outage affecting SOAP payload handlers.


## Cross-suite correlation

- **WISP Systemic Outage**: WISP suite experienced widespread catastrophic backend failures (45 tests failing with HTTP 500 across SOAP endpoints), indicating an unhandled exception or microservice failure in the WISP API layer.
- **Checkout Functional/E2E Issues**: Checkout suite failures were isolated to UI element timeouts (Postepay PSP missing) and asynchronous payment state synchronization delays.
- **FDR-3 Suite Stability**: The FDR-3 suite passed completely without issues, indicating core FDR services were unaffected by issues observed in Checkout or WISP.