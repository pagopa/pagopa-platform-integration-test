# 1. L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo`
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
The checkout redirection returned a 200 OK status code instead of the expected 302 redirect.

### Category
application bug

### Recommended action
Investigate the checkout service routing or controller logic handling redirection for multi-RPT carts.

---

# 2. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
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
Received HTTP 200 instead of HTTP 302 during checkout redirection for a single RPT cart with a stamp.

### Category
application bug

### Recommended action
Check backend logs to see why the checkout endpoint returns 200 OK without issuing a redirect.

---

# 3. L'utente paga un carrello con cinque RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con cinque RPT con un versamento ciascuna`
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
The checkout step failed because the service responded with status 200 instead of the expected 302 redirect.

### Category
application bug

### Recommended action
Verify application behavior for carts containing five RPTs.

---

# 4. L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo`
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
Redirect to checkout returned HTTP 200 instead of HTTP 302.

### Category
application bug

### Recommended action
Examine why stamp-only carts fail to trigger the proper redirection response.

---

# 5. L'utente paga un carrello con due RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT per un totale di cinque versamenti`
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
Unexpected HTTP 200 response received during the checkout redirection step instead of HTTP 302.

### Category
application bug

### Recommended action
Check the API response mapping for cart creation requests with multiple transfers.

---

# 6. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD
- **status**: broken
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD`
- **message**: requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 97, in generate_payment_position
    status_code, body, _ = execute_request(url, 'post', headers, payment_positions,
                           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                           type=constants.ResponseType.JSON,
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                           description=req_description)
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/utils.py", line 35, in execute_request
    object_response = response.json()
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/requests/models.py", line 982, in json
    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)
```
### Root cause
The API response was empty or non-JSON, causing a `JSONDecodeError` when trying to parse the body.

### Category
environment

### Recommended action
Check if the target service (GPD) is up and returning valid responses or if an upstream gateway is returning an empty error page.

---

# 7. L'utente paga un carrello con singola RPT con cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con cinque versamenti`
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
The checkout redirection step received status 200 instead of 302.

### Category
application bug

### Recommended action
Investigate why single RPT carts with multiple transfers do not redirect correctly.

---

# 8. L'utente paga un carrello con tre RPT per un totale di dieci versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di dieci versamenti`
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
HTTP 200 received instead of the expected 302 redirect during checkout.

### Category
application bug

### Recommended action
Check backend constraints and handling for carts with high transfer counts.

---

# 9. L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 197, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 403, in check_event
    assert_show_message(len(needed_process_events) > 0,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        f'There are not events with business process {business_process}.')
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.p
```
### Root cause
The expected `receipt-ok` business event (`RT_SEND_SUCCESS`) was not generated for the multi-beneficiary cart.

### Category
application bug

### Recommended action
Inspect the event publisher and receipt generation flow for multi-beneficiary payments.

---

# 10. Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD
- **status**: broken
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD`
- **message**: requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 97, in generate_payment_position
    status_code, body, _ = execute_request(url, 'post', headers, payment_positions,
                           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                           type=constants.ResponseType.JSON,
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                           description=req_description)
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/utils.py", line 35, in execute_request
    object_response = response.json()
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/requests/models.py", line 982, in json
    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)
```
### Root cause
Failed to parse JSON response because the API returned an empty or invalid payload during payment position generation.

### Category
environment

### Recommended action
Check service availability and logs for the GPD integration endpoint.

---

# 11. L'utente paga un carrello con quattro RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con quattro RPT con un versamento ciascuna`
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
Received HTTP 200 instead of HTTP 302 during checkout redirection.

### Category
application bug

### Recommended action
Review request handling for carts with four RPT elements.

---

# 12. L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo`
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
Checkout redirection returned status 200 instead of 302.

### Category
application bug

### Recommended action
Analyze controller logic for mixed RPT carts containing stamps and transfers.

---

# 13. L'utente paga un carrello con singola RPT con tre versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con tre versamenti`
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
Expected HTTP 302 redirect but received HTTP 200.

### Category
application bug

### Recommended action
Verify checkout flow configuration for single RPT carts with multiple transfers.

---

# 14. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce`
- **message**: AssertionError: The status code is not 302. Current value: 200.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 206, in user_redirected_to_checkout
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
The payment closure failure scenario failed early because the redirect returned 200 instead of 302.

### Category
application bug

### Recommended action
Ensure the initial checkout redirection status code is correct before testing closure failure flows.

---

# 15. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
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
Received HTTP 200 instead of HTTP 302 during checkout redirection.

### Category
application bug

### Recommended action
Check handling of stamp-only single RPT carts in the checkout redirection logic.

---

# 16. L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 197, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 403, in check_event
    assert_show_message(len(needed_process_events) > 0,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        f'There are not events with business process {business_process}.')
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.p
```
### Root cause
The business event `receipt-ok` (`RT_SEND_SUCCESS`) was not emitted for the multi-beneficiary transaction.

### Category
application bug

### Recommended action
Verify event generation and message broker integration for multi-beneficiary receipt delivery.

---

# 17. L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo`
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
Checkout step received HTTP 200 instead of the expected HTTP 302 redirect.

### Category
application bug

### Recommended action
Check the redirection rules for single RPT carts combining multiple transfers and a stamp.

---

# 18. L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo`
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
Redirection returned HTTP 200 instead of HTTP 302.

### Category
application bug

### Recommended action
Review endpoint response codes for multi-RPT carts with stamps.

---

# 19. L'utente paga un carrello con singola RPT con due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti`
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
Received HTTP 200 instead of HTTP 302 during checkout redirection.

### Category
application bug

### Recommended action
Investigate checkout controller logic for single RPT carts with dual transfers.

---

# 20. L'utente paga un carrello con tre RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT con un versamento ciascuna`
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
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py`, line 21, in check_status_code
    assert int(
           ^^^^
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Checkout redirection returned HTTP 200 instead of HTTP 302.

### Category
application bug

### Recommended action
Check backend routing and response codes for three-RPT cart submissions.

---

## Common patterns
- **Checkout Redirection Failures (`nodoInviaCarrelloRPT`)**: A large portion of failures stem from the checkout redirection step expecting an HTTP 302 redirect but receiving an HTTP 200 OK instead. This points to a widespread issue in how cart submission responses are handled or routed in the application layer.
- **JSON Decoding Errors**: Failures related to `JSONDecodeError` indicate environment or service availability issues where downstream dependencies (such as GPD) return empty or non-JSON error pages instead of valid payloads.