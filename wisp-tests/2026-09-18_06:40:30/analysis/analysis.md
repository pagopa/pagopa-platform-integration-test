# 1. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo`
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
The WISP payment flow failed to complete successfully, resulting in the absence of the expected `receipt-ok` event with `RT_SEND_SUCCESS` status.

### Category
application bug

### Recommended action
Inspect the backend WISP and Node services logs to determine why the receipt generation or transmission failed during checkout.

---

# 2. L'utente paga un carrello con singola RPT con quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con quattro versamenti`
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
Cart payment processing failed to generate and successfully send the receipt (`receipt-ok` / `RT_SEND_SUCCESS`) back to the platform.

### Category
application bug

### Recommended action
Verify the multi-payment/cart handling logic in WISP to ensure receipts are properly processed and sent for carts with multiple installments.

---

# 3. L'utente paga un carrello con due RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT per un totale di cinque versamenti`
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
The payment session for a complex cart (multiple RPTs and installments) did not complete with a successful receipt notification event.

### Category
application bug

### Recommended action
Analyze transaction traces for complex cart submissions to identify potential bottlenecks or failures in WISP receipt dispatching.

---

# 4. Utente paga un pagamento singolo con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento semplice e una marca da bollo`
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
Even with a single payment containing a stamp (marca da bollo), the receipt transmission event (`receipt-ok` with status `RT_SEND_SUCCESS`) was not registered.

### Category
application bug

### Recommended action
Check event logs for stamp-inclusive payments to ensure the receipt generation step is not failing on validation or communication errors.

---

## Common patterns
All 4 failures share the exact same assertion failure: `AssertionError: There are not events with business process receipt-ok` during the `check_wisp_session_timers_del_and_rts_were_sent` step. This indicates a systemic issue across different payment types (single payments, carts, with or without stamps) where WISP is failing to complete the receipt sending process (`RT_SEND_SUCCESS`).