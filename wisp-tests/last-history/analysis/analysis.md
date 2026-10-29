# 1. L'utente paga un carrello con singola RPT con un versamento
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 403, in check_event
    assert_show_message(len(needed_process_events) > 0,
```
### Root cause
The asynchronous receipt generation process (`receipt-ok` with status `RT_SEND_SUCCESS`) did not complete or register within the expected polling timeout window during checkout completion.

### Category
application bug

### Recommended action
Investigate the backend service responsible for processing and dispatching receipts (`RT`) to ensure it is not experiencing delays or downstream failures.

---

# 2. L'utente paga un carrello multibeneficiario con due RPT con un totale di due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di due versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/integration/wisp/steps/steps.py", line 197, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 403, in check_event
    assert_show_message(len(needed_process_events) > 0,
```
### Root cause
The asynchronous receipt generation process (`receipt-ok` with status `RT_SEND_SUCCESS`) did not complete or register within the expected polling timeout window during checkout completion.

### Category
application bug

### Recommended action
Investigate the backend service responsible for processing and dispatching receipts (`RT`) to ensure it is not experiencing delays or downstream failures.

---

# 3. L'utente paga un carrello con cinque RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con cinque RPT con un versamento ciascuna`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 403, in check_event
    assert_show_message(len(needed_process_events) > 0,
```
### Root cause
The asynchronous receipt generation process (`receipt-ok` with status `RT_SEND_SUCCESS`) did not complete or register within the expected polling timeout window during checkout completion.

### Category
application bug

### Recommended action
Investigate the backend service responsible for processing and dispatching receipts (`RT`) to ensure it is not experiencing delays or downstream failures.

---

# 4. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 403, in check_event
    assert_show_message(len(needed_process_events) > 0,
```
### Root cause
The asynchronous receipt generation process (`receipt-ok` with status `RT_SEND_SUCCESS`) did not complete or register within the expected polling timeout window during checkout completion.

### Category
application bug

### Recommended action
Investigate the backend service responsible for processing and dispatching receipts (`RT`) to ensure it is not experiencing delays or downstream failures.

---

# 5. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 403, in check_event
    assert_show_message(len(needed_process_events) > 0,
```
### Root cause
The asynchronous receipt generation process (`receipt-ok` with status `RT_SEND_SUCCESS`) did not complete or register within the expected polling timeout window during checkout completion.

### Category
application bug

### Recommended action
Investigate the backend service responsible for processing and dispatching receipts (`RT`) to ensure it is not experiencing delays or downstream failures.

---

# 6. Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
  File "/opt/hostedtoolcache/Python/3.15.1/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 403, in check_event
    assert_show_message(len(needed_process_events) > 0,
```
### Root cause
The asynchronous receipt generation process (`receipt-ok` with status `RT_SEND_SUCCESS`) did not complete or register within the expected polling timeout window during checkout completion.

### Category
application bug

### Recommended action
Investigate the backend service responsible for processing and dispatching receipts (`RT`) to ensure it is not experiencing delays or downstream failures.

---

# 7. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_existingPaymentPosition.L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT.L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 39.494s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_existingPaymentPosition.feature:19
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f8485a31080>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '348179328792217551', 'state': 'OK'}]}
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f8485a318f0>
INFO:root:Waiting [10] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK'}
INFO:root:Waiting [20] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
ERROR:root:[Assert Error] There are not events with business process receipt-ok.
```
### Root cause
Timeout waiting for the RE (Runtime Events) logs to record the `receipt-ok` event (`RT_SEND_SUCCESS`) following checkout completion.

### Category
application bug

### Recommended action
Check the event-logging subsystem and the receipt generation worker queues to ensure events are being correctly dispatched and written without undue latency.

---

# 8. L'utente paga un carrello multibeneficiario con due RPT con un totale di due versamenti
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_multibeneficiary.L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT.L'utente paga un carrello multibeneficiario con due RPT con un totale di due versamenti`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento multibeneficiario ... failed in 39.445s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_multibeneficiary.feature:19
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f8485a8f8d0>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179328828745450', 'state': 'OK'}]}
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f8485b2dcb0>
INFO:root:Waiting [10] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK'}
INFO:root:Waiting [20] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
ERROR:root:[Assert Error] There are not events with business process receipt-ok.
```
### Root cause
Timeout waiting for the RE (Runtime Events) logs to record the `receipt-ok` event (`RT_SEND_SUCCESS`) following checkout completion.

### Category
application bug

### Recommended action
Check the event-logging subsystem and the receipt generation worker queues to ensure events are being correctly dispatched and written without undue latency.

---

# 9. L'utente paga un carrello con singola RPT con un versamento
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_noStamp.L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT.L'utente paga un carrello con singola RPT con un versamento`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 38.306s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_noStamp.feature:18
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f8485ad6ca0>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179328847225358', 'state': 'OK'}]}
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f8485ad5da0>
INFO:root:Waiting [10] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK'}
INFO:root:Waiting [20] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
ERROR:root:[Assert Error] There are not events with business process receipt-ok.
```
### Root cause
Timeout waiting for the RE (Runtime Events) logs to record the `receipt-ok` event (`RT_SEND_SUCCESS`) following checkout completion.

### Category
application bug

### Recommended action
Check the event-logging subsystem and the receipt generation worker queues to ensure events are being correctly dispatched and written without undue latency.

---

# 10. L'utente paga un carrello con cinque RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_noStamp.L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT.L'utente paga un carrello con cinque RPT con un versamento ciascuna`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 48.308s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_noStamp.feature:104
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f8485afbf60>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179328878489130', 'state': 'OK'}, {'fiscalCode': '15376371009', 'noticeNumber': '351179328878500551', 'state': 'OK'}, {'fiscalCode': '15376371009', 'noticeNumber': '351179328878496915', 'state': 'OK'}, {'fiscalCode': '15376371009', 'noticeNumber': '351179328878493069', 'state': 'OK'}, {'fiscalCode': '15376371009', 'noticeNumber': '351179328878485284', 'state': 'OK'}]}
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f8485afb4c0>
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f8485afa930>
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f8485afa070>
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f8485afbe20>
INFO:root:Response status code: 200
```
### Root cause
Timeout waiting for the RE (Runtime Events) logs to record the `receipt-ok` event (`RT_SEND_SUCCESS`) following checkout completion for multiple RPTs.

### Category
application bug

### Recommended action
Verify system performance under heavier payload scenarios (multi-RPT carts) to ensure the receipt notification pipeline processes and logs events without timing out.

---

# 11. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `features.nodoInviaCarrelloRPT.nodoInviaCarrelloRPT_withStamp.L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT.L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 38.610s
Location: src/integration/wisp/features/nodoInviaCarrelloRPT/nodoInviaCarrelloRPT_withStamp.feature:18
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f84867e0040>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179328912386519', 'state': 'OK'}]}
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f8485afb600>
INFO:root:Waiting [10] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK'}
INFO:root:Waiting [20] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
ERROR:root:[Assert Error] There are not events with business process receipt-ok.
```
### Root cause
Timeout waiting for the RE (Runtime Events) logs to record the `receipt-ok` event (`RT_SEND_SUCCESS`) following checkout completion.

### Category
application bug

### Recommended action
Check the event-logging subsystem and the receipt generation worker queues to ensure events are being correctly dispatched and written without undue latency.

---

# 12. Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo
- **status**: failed
- **fullName**: `features.nodoInviaRPT.nodoInviaRPT_withStamp.Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT.Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo`
- **message**: There are not events with business process receipt-ok.
- **trace**:
```
Failing step: Allora l'utente viene reindirizzato su Checkout completando il pagamento ... failed in 38.901s
Location: src/integration/wisp/features/nodoInviaRPT/nodoInviaRPT_withStamp.feature:47
Assertion Failed: There are not events with business process receipt-ok.
Captured logging:
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f8485afb5ba0>
INFO:root:Waiting [2] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK', 'positionslist': [{'fiscalCode': '15376371009', 'noticeNumber': '351179329005106812', 'state': 'OK'}]}
INFO:root:Response status code: 200
INFO:root:Response body: <Element 'Envelope' at 0x7f84859341d0>
INFO:root:Waiting [10] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
INFO:root:Response status code: 200
INFO:root:Response body: {'outcome': 'OK'}
INFO:root:Waiting [20] secondto wait for Nodo to write RE events
INFO:root:Wait time ended
ERROR:root:[Assert Error] There are not events with business process receipt-ok.
```
### Root cause
Timeout waiting for the RE (Runtime Events) logs to record the `receipt-ok` event (`RT_SEND_SUCCESS`) following checkout completion.

### Category
application bug

### Recommended action
Check the event-logging subsystem and the receipt generation worker queues to ensure events are being correctly dispatched and written without undue latency.

---

## Common patterns

All 12 failures across the WISP test suite share an identical root cause: **failure to find the `receipt-ok` event with status `RT_SEND_SUCCESS` within the expected polling timeout**. This indicates a systemic platform issue where payment receipts (`RT`) are either failing to generate, failing to dispatch, or taking longer than the configured test timeout to be recorded in the RE logging system.