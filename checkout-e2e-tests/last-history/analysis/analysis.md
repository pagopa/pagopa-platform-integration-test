# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The PSP radio button for Postepay failed to load or render within the 5-second timeout window on the UAT environment.

### Category
environment

### Recommended action
Increase the locator timeout threshold or check UAT environment stability/PSP availability endpoints.

---

# 2. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Postepay" viene completato con successo`
- **message**: RuntimeError: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 188, in step_select_psp
    locate_and_click(page, f"#psp-radio-{psp_id}")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 129, in locate_and_click
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The PSP selection element failed to appear on the page before the timeout limit was reached due to slow page rendering or network latency.

### Category
environment

### Recommended action
Investigate UAT backend performance and network latency during PSP list loading.

---

# 3. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The target Creditor Institution (Ente Creditore) returned a general service error instead of the expected not-found response for an invalid notice code.

### Category
application bug

### Recommended action
Verify node/mock creditor institution configurations for handling invalid notice code ranges in the UAT environment.

---

# 4. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Worldpay" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Il pagamento non è andato a buon fine'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The payment gateway (Worldpay simulation) rejected the transaction or failed to complete processing, returning a payment failure message.

### Category
environment

### Recommended action
Check Worldpay sandbox gateway availability, merchant configuration, and test card authorization status.

---

# 5. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `features.checkout_npg.Attivazione pagamento Checkout.Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1`
- **message**: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
Failing step: E L'utente seleziona il PSP con id "PPAYITR1XXX" ... failed in 5.084s
Location: src/e2e/checkout/features/checkout_npg.feature:35
Traceback (most recent call last):
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 93, in locate_and_click
    to_click.wait_for(state="visible", timeout=timeout)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
           ~~~~~~~~~~~^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/_impl/_locator.py", line 692, in wait_for
    await self._frame.wait_for_selector(
        self._selector, strict=True, timeout=timeout, state=state
    )
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
    await self._channel.send(
        "waitForSelector", self._timeout, locals_to_params(locals())
    )
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 69, in 
```
### Root cause
UI element `#psp-radio-PPAYITR1XXX` was not rendered within the timeout limit on the PSP list page.

### Category
environment

### Recommended action
Review page load performance metrics and consider raising the default Playwright selector timeout.

---

# 6. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `features.checkout_npg.Attivazione pagamento Checkout.Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1`
- **message**: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
Failing step: E L'intestazione della modale di errore contiene "Non riusciamo a trovare l’avviso" ... failed in 0.009s
Location: src/e2e/checkout/features/checkout_npg.feature:57
Assertion Failed: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
```
### Root cause
Downstream Node/EC integration returned a timeout/error response instead of the expected application-level notice-not-found error.

### Category
application bug

### Recommended action
Verify the mock response configuration for invalid notice codes on the backend services.

---

# 7. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
- **status**: broken
- **fullName**: `features.checkout_npg_auth.Attivazione pagamento Checkout autenticato.Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1`
- **message**: Timeout on locator '#psp-radio-PPAYITR1XXX' after 5000 ms (url: https://uat.checkout.pagopa.it/lista-psp)
- **trace**:
```
Failing step: E L'utente seleziona il PSP con id "PPAYITR1XXX" ... failed in 5.062s
Location: src/e2e/checkout/features/checkout_npg_auth.feature:36
Traceback (most recent call last):
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/helper.py", line 93, in locate_and_click
    to_click.wait_for(state="visible", timeout=timeout)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/sync_api/_generated.py", line 17975, in wait_for
    self._sync(self._impl_obj.wait_for(timeout=timeout, state=state))
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/_impl/_sync_base.py", line 115, in _sync
    return task.result()
           ~~~~~~~~~~~^^
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/_impl/_locator.py", line 692, in wait_for
    await self._frame.wait_for_selector(
        self._selector, strict=True, timeout=timeout, state=state
    )
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/_impl/_frame.py", line 369, in wait_for_selector
    await self._channel.send(
        "waitForSelector", self._timeout, locals_to_params(locals())
    )
  File "/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 69
```
### Root cause
The Postepay PSP option failed to render on the authenticated checkout flow page within the allowed timeout.

### Category
environment

### Recommended action
Inspect checkout frontend API responses for PSP list retrieval and ensure stable UAT environment conditions.

---

# 8. Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3
- **status**: failed
- **fullName**: `features.checkout_npg_auth.Attivazione pagamento Checkout autenticato.Un pagamento con configurazione carta "Worldpay" viene completato con successo -- @1.3`
- **message**: Expected 'Hai pagato' in result message, but got: 'Il pagamento non è andato a buon fine'
- **trace**:
```
Failing step: Allora Viene mostrato un messaggio di pagamento completato con successo ... failed in 43.939s
Location: src/e2e/checkout/features/checkout_npg_auth.feature:39
Assertion Failed: Expected 'Hai pagato' in result message, but got: 'Il pagamento non è andato a buon fine'
Captured logging:
INFO:src.e2e.checkout.helper:Performing login
```
### Root cause
The authenticated Worldpay payment flow resulted in a transaction failure message instead of a success confirmation.

### Category
environment

### Recommended action
Check Worldpay gateway sandbox credentials and transaction logs to diagnose the payment rejection cause.

---

## Common patterns

- **PSP Selection Timeout**: Multiple failures across authenticated and unauthenticated flows stem from timeouts when waiting for `#psp-radio-PPAYITR1XXX` to appear on the PSP list page. *Action*: Investigate UAT environment performance/network latency and consider increasing the element wait timeout.
- **Payment Gateway Failures**: Worldpay card payment tests failed due to transaction rejection messages. *Action*: Verify Worldpay sandbox service status and test card validity.
- **Creditor Institution Error Mappings**: Invalid notice code tests received generic service error messages instead of specific "notice not found" error headers. *Action*: Check backend/mock configuration for error handling and response mappings.