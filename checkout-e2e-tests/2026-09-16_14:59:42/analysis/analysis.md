# 1. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The Postepay PSP option did not load or render within the 5-second timeout on the PSP selection page.

### Category
environment

### Recommended action
Check if the upstream PSP gateway or UAT environment is experiencing slowness, and consider slightly increasing the timeout or adding an explicit wait for element visibility.

---

# 2. Un pagamento con configurazione carta "Postepay" viene completato con successo -- @1.1
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
    raise RuntimeError(
        f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
    ) from exc
```
### Root cause
The Postepay PSP option failed to appear on the PSP list page within the allotted timeout.

### Category
environment

### Recommended action
Investigate UAT environment performance or network stability during PSP list retrieval.

---

# 3. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout autenticato: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Il pagamento non è andato a buon fine'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The payment transaction processed via Worldline failed unexpectedly at the gateway level instead of completing successfully.

### Category
application bug

### Recommended action
Review Worldline sandbox/UAT logs and application payment processing logs to determine why the transaction was declined.

---

# 4. Un pagamento con configurazione carta "Wordline" viene completato con successo -- @1.2
- **status**: failed
- **fullName**: `Attivazione pagamento Checkout: Un pagamento con configurazione carta "Wordline" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Il pagamento non è andato a buon fine'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 1329, in run
    ...
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The payment transaction processed via Worldline was rejected or failed to settle.

### Category
application bug

### Recommended action
Verify integration parameters with Worldline and check backend transaction error logs.

---

# 5. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
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
The creditor institution (Ente Creditore) returned a general error message instead of the expected unknown payment notice error.

### Category
test data

### Recommended action
Check if the test notice code used is currently active or properly mocked to return the specific `PAA_PAGAMENTO_SCONOSCIUTO` error code in the target environment.

---

## Common patterns
Failures in this test run are split evenly between infrastructure/environment bottlenecks (timeouts loading PSP options), external gateway failures (Worldline payment refusals in both authenticated and unauthenticated flows), and unexpected error mapping from creditor institutions during negative test cases.