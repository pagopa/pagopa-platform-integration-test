# 1. L'utente paga un carrello con quattro RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con quattro RPT con un versamento ciascuna`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
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
The asynchronous generation or logging of the `receipt-ok` event (`RT_SEND_SUCCESS`) failed to register within the timeout period.

### Category
application bug

### Recommended action
Investigate the downstream receipt generation service (e.g., `pagopa-node` or `pagopa-receipt-pdf-generator`) to ensure RTs are successfully dispatched and logged.

---

# 2. L'utente paga un carrello multibeneficiario con due RPT con un totale di due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di due versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
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
Multibeneficiary cart checkout failed to complete the receipt dispatch phase (`RT_SEND_SUCCESS`), causing missing business process events.

### Category
application bug

### Recommended action
Check backend logs for multibeneficiary cart payment processing errors during the closure phase.

---

# 3. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
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
The retry mechanism following a failed payment closure did not successfully complete and publish the final `receipt-ok` event.

### Category
application bug

### Recommended action
Verify payment retry handling logic in WISP/Nodo to ensure subsequent closure attempts correctly trigger receipt generation.

---

# 4. L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
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
Missing `receipt-ok` event for multibeneficiary cart payments involving multiple transfers.

### Category
application bug

### Recommended action
Debug cart receipt generation services for complex multi-transfer payloads.

---

# 5. L'utente paga un carrello multibeneficiario con due RPT con un totale di due versamenti
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_multibeneficiary.L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT.L'utente paga un carrello multibeneficiario con due RPT con un totale di due versamenti`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento multibeneficiario ... failed in 39.543s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_multibeneficiary.feature:19
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fc06405c7c0>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179326983490604', 'state': 'OK'}]}
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fc06405f9c0>
INFO:root:Waiting [10] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK'}
INFO:root:Waiting [20] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
ERROR:root:[Assert Error] There are not events with business process receipt-ok.
```
### Root cause
The RE events verification step timed out waiting for the `receipt-ok` event after a successful multibeneficiary checkout flow.

### Category
application bug

### Recommended action
Inspect event store/indexer latency or check if the RT forwarding job failed to execute for multibeneficiary payments.

---

# 6. L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_multibeneficiary.L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT.L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento multibeneficiario ... failed in 39.089s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_multibeneficiary.feature:43
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fc06405f560>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179326992097043', 'state': 'OK'}]}
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fc06409d120>
INFO:root:Waiting [10] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK'}
INFO:root:Waiting [20] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
ERROR:root:[Assert Error] There are not events with business process receipt-ok.
```
### Root cause
Timeout waiting for `receipt-ok` RE event logging during multi-transfer multibeneficiario cart payment validation.

### Category
application bug

### Recommended action
Verify application logs for failures during the finalization step of multi-transfer multibeneficiary carts.

---

# 7. L'utente paga un carrello con quattro RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_noStamp.L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT.L'utente paga un carrello con quattro RPT con un versamento ciascuna`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 44.468s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_noStamp.feature:89
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fc06411c770>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179327027676116', 'state': 'OK'}, {'fiscalCode': '15376371009', 'noticeNumber': '351179327027665091', 'state': 'OK'}, {'fiscalCode': '15376371009', 'noticeNumber': '351179327027672472', 'state': 'OK'}, {'fiscalCode': '15376371009', 'noticeNumber': '351179327027668735', 'state': 'OK'}]}
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fc06411fab0>
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fc06411cd60>
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fc06411d760>
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fc06411f920>
INFO:root:Waiting [10] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK'}
INFO:
```
### Root cause
The RE event collection check failed to find the `receipt-ok` event within the allocated polling window for a 4-RPT cart payment without stamps.

### Category
application bug

### Recommended action
Check backend components responsible for generating and persisting receipt events for large carts (`nodoInviaCarrelloRPT`).

---

# 8. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_noStamp.L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT.L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento multibeneficiario ... failed in 44.929s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_noStamp.feature:156
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fc06405c9f0>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179327051943351', 'state': 'OK'}, {'fiscalCode': '15376371009', 'noticeNumber': '351179327051938604', 'state': 'OK'}]}
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fc063f3e200>
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fc064110130>
INFO:root:Waiting [10] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK'}
INFO:root:Waiting [20] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7fc064110540>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 
```
### Root cause
The payment retry scenario failed to emit the expected `receipt-ok` RE event upon successful completion after an initial closure failure.

### Category
application bug

### Recommended action
Trace the payment retry state machine in WISP to ensure receipt generation triggers correctly after a failed closure attempt.

---

## Common patterns
All 8 failures share the exact same root cause pattern: an AssertionError where the test suite fails to find the `receipt-ok` event (`RT_SEND_SUCCESS`) within the RE events log after completing a `nodoInviaCarrelloRPT` flow (covering multi-RPT, multi-beneficiary, and retry scenarios). This points to a systemic platform or backend issue regarding receipt generation or RE event logging for cart-based payment flows.