# 1. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
```
### Root cause
The receipt generation process did not produce the expected `receipt-ok` event with status `RT_SEND_SUCCESS` during WISP session cleanup and verification.

### Category
application bug

### Recommended action
Inspect the receipt generation service and event log queue to check why `receipt-ok` RT dispatch events are failing to register.

---

# 2. L'utente paga un carrello con singola RPT con un versamento
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
```
### Root cause
The payment execution completed, but the expected `receipt-ok` event failed to publish with `RT_SEND_SUCCESS`.

### Category
application bug

### Recommended action
Verify downstream receipt creation logic for single RPT cart payments in the application's event processing pipeline.

---

# 3. Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
```
### Root cause
Single payment with multiple transfers (`nodoInviaRPT`) failed to register the `receipt-ok` business process event.

### Category
application bug

### Recommended action
Check backend logs for errors during RT (Ricevuta Telematica) transmission when multiple payments/transfers are involved.

---

# 4. Utente paga un pagamento singolo con due versamenti semplici e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti semplici e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
```
### Root cause
Verification failed due to missing `receipt-ok` events following payment completion with revenue stamps via `nodoInviaRPT`.

### Category
application bug

### Recommended action
Investigate the receipt creation handler and EventHub/message broker for dropped or unhandled RT receipt notifications.

---

# 5. L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
```
### Root cause
The multi-RPT payment cart completed checkout, but the `receipt-ok` business process event was not emitted.

### Category
application bug

### Recommended action
Audit multi-RPT cart payment receipt dispatch routines to ensure RTs are correctly generated and sent to the notification queue.

---

## Common patterns

- **Systemic Failure in Receipt Event Emission**: All 5 failures share the exact same assertion error (`AssertionError: There are not events with business process receipt-ok.`).
- **Failure Point**: The error consistently originates from `steputils.check_wisp_session_timers_del_and_rts_were_sent` in `steps_utils.py` (line 898), specifically inside the `check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')` call.
- **Scope**: The failure is agnostic to the payload variations—it impacts single RPT (`nodoInviaRPT`), multi-RPT carts (`nodoInviaCarrelloRPT`), simple payments, and payments containing revenue stamps (`marca da bollo`).
- **Conclusion**: This points to a broken or unresponsive background process, queue handler, or API endpoint responsible for triggering/publishing the `receipt-ok` RT dispatch event upon checkout completion across WISP integration workflows.