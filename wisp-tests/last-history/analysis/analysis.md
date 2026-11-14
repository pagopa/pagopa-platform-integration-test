## Suite: wisp

# 1. Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 926, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
```
### Root cause
The expected event with business process `receipt-ok` and status `RT_SEND_SUCCESS` was not emitted or published within the expected window.

### Category
application bug

### Recommended action
Investigate receipt emission services and message queues to verify why `receipt-ok` events with status `RT_SEND_SUCCESS` are failing to generate.

---

# 2. L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 926, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
```
### Root cause
The expected event with business process `receipt-ok` and status `RT_SEND_SUCCESS` was not registered during multi-RPT cart processing.

### Category
application bug

### Recommended action
Verify downstream receipt processing logic for cart payments involving existing GPD debt positions.

---

# 3. L'utente paga un carrello con tre RPT per un totale di dieci versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di dieci versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 926, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
```
### Root cause
The receipt generation process failed to emit `receipt-ok` events (`RT_SEND_SUCCESS`) when handling carts with multiple RPTs and high payment counts.

### Category
application bug

### Recommended action
Check backend logs for receipt processing delays or failures when handling multi-RPT payment transactions.

---

## Common patterns
- **Missing `receipt-ok` events**: All failures in the WISP suite stem from `check_wisp_session_timers_del_and_rts_were_sent` failing to find business process events matching `receipt-ok` with status `RT_SEND_SUCCESS`.

## Cross-suite correlation
- All reported failures belong to a single suite (`wisp`) and share identical assertion failures regarding missing `receipt-ok` events (`RT_SEND_SUCCESS`).
- **Shared Root Cause**: WISP receipt generation/event notification system failed to post `receipt-ok` completion events.
- **Recommended Action**: Inspect the receipt processor/event handler service to ensure `RT_SEND_SUCCESS` events are correctly emitted and persisted during checkout flows.