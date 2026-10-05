# 1. Utente paga un pagamento singolo con due versamenti semplici e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti semplici e una marca da bollo`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 2. L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 3. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 4. Utente tenta due volte di pagare la stessa RPT ma la conversione al nuovo modello fallisce
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente tenta due volte di pagare la stessa RPT ma la conversione al nuovo modello fallisce`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 5. Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 6. L'utente paga un carrello con singola RPT con due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 7. L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 8. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo`
- **message**: AssertionError: The status code is not 302. Current value: 200.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 166, in user_redirected_to_checkout
    steputils.exec_nm1_to_nmu(context, actor)
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 838, in exec_nm1_to_nmu
    check_status_code(context, actor, expected_status)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 21, in check_status_code
    assert int(
           ^^^^
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The request returned HTTP 200 instead of the expected redirect status code (302) during the flow execution.

### Category
application bug

### Recommended action
Check the API response mapping and routing logic for redirection handling during the NM1 to NMU phase.

---

# 9. L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 10. L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 194, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 11. L'utente paga un carrello con due RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT per un totale di cinque versamenti`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 12. L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 13. Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 14. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 15. L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 16. Utente tenta il pagamento, poi riprova il flusso ma fallisce
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente tenta il pagamento, poi riprova il flusso ma fallisce`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 265, in send_activatePaymentNoticeV2_request
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
       
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 17. L'utente paga un carrello con tre RPT per un totale di dieci versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di dieci versamenti`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 18. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 209, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 19. L'utente paga un carrello con quattro RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con quattro RPT con un versamento ciascuna`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

# 20. L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo`
- **message**: AssertionError: The field [paymentToken] does not exists.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 169, in user_redirected_to_checkout
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 865, in send_index_activatePaymentNoticeV2_request
    check_field_with_non_null_value(context, 'paymentToken')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 362, in check_field_with_non_null_value
    assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
           ^^^^^
```
### Root cause
The payment activation request failed to return a `paymentToken`, causing subsequent steps relying on checkout redirection to fail.

### Category
application bug

### Recommended action
Investigate the upstream activation service (activatePaymentNoticeV2) response handling and check backend logs for error propagation.

---

## Common patterns
The vast majority of failures stem from the `activatePaymentNoticeV2` request failing to generate or return a valid `paymentToken`. This indicates a systemic failure in the payment activation backend or node service during the test run, blocking all downstream checkout redirection and completion steps across single payments, carts, and multi-beneficiary flows.