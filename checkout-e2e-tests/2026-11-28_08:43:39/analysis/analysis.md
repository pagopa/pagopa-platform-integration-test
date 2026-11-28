## Suite: checkout

# 1. Un pagamento con configurazione carta "Poste" viene completato con successo -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento: Un pagamento con configurazione carta "Poste" viene completato con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Il pagamento non è andato a buon fine'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The payment attempt using the "Poste" card configuration failed during gateway/NPG processing, causing Checkout to display a payment error message instead of success.

### Category
application bug

### Recommended action
Inspect NPG gateway logs and transaction processing backend services for the failed "Poste" card payment flow to identify the failure cause during authorization.

---

# 2. Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999 -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento: Viene mostrato l'errore PAA_PAGAMENTO_SCONOSCIUTO per codice avviso non valido nell'intervallo 302400000000000000-302409999999999999`
- **message**: AssertionError: Expected modal header to contain 'Non riusciamo a trovare l’avviso', but got: 'L’Ente Creditore sta avendo problemi nella risposta'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 245, in step_error_modal_header
    assert expected_header in header_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The payment activation failed with a generic Creditor Institution timeout/unreachable response error instead of returning the expected specific `PAA_PAGAMENTO_SCONOSCIUTO` error response.

### Category
environment

### Recommended action
Verify mock/stub response configurations for the Creditor Institution (PA) mock handling notice codes in range 302400000000000000-302409999999999999.

---

# 3. Un pagamento con configurazione carta "Poste" viene completato con successo -- @1.1
- **status**: failed
- **fullName**: `Attivazione pagamento Autenticato: Un pagamento con configurazione carta "Poste" viene completato me con successo`
- **message**: AssertionError: Expected 'Hai pagato' in result message, but got: 'Il pagamento non è andato a buon fine'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/e2e/checkout/steps/checkout_npg.py", line 309, in step_check_payment_success
    assert "Hai pagato" in message_text, (
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Authenticated payment using the "Poste" card configuration failed during gateway/NPG processing, causing Checkout to display a payment error message instead of success.

### Category
application bug

### Recommended action
Investigate authenticated user session handling and authorization logs for NPG "Poste" card transactions to resolve authorization errors.

---

## Common patterns
- **Poste Card Payment Failure**: Multiple tests (#1, #3) fail due to payments failing specifically when using the "Poste" card configuration in both guest and authenticated flows.
- **Unexpected Error Modal Mapping**: Test #2 fails due to receiving a generic PA failure modal rather than the specific unknown payment notice error modal.

## Cross-suite correlation
Only the `checkout` suite was analyzed in this report. Across the single suite, failures are isolated to payment gateway processing errors for specific card configurations ("Poste") and upstream mock dependency issues for Creditor Institution error mappings.