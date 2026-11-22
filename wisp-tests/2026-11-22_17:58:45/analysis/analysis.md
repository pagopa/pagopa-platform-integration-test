## Suite: wisp

# 1. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo`
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
The asynchronous event processor did not emit or record the business process event `receipt-ok` with status `RT_SEND_SUCCESS` within the expected step execution time.

### Category
application bug

### Recommended action
Verify whether the receipt generation component or message bus experienced delays/failures in processing `receipt-ok` events, or adjust test step polling time if this is due to async timing.

---

# 2. L'utente paga un carrello con singola RPT con cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con cinque versamenti`
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
Missing `receipt-ok` event (`RT_SEND_SUCCESS`) during checkout flow validation for single RPT cart with multiple payments.

### Category
application bug

### Recommended action
Investigate backend receipt transmission logs for multi-payment single RPT carts to check why `RT_SEND_SUCCESS` events are omitted.

---

# 3. L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, con quantita diverse di versamenti简单的 e marche da bollo`
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
Failure to assert `receipt-ok` event presence when processing multi-RPT carts containing revenue stamps.

### Category
application bug

### Recommended action
Check backend workflow processing for carts with mixed RPT types and revenue stamps to ensure receipts are correctly dispatched and logged.

---

# 4. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
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
Missing `receipt-ok` event (`RT_SEND_SUCCESS`) during checkout flow validation for single RPT with a revenue stamp.

### Category
application bug

### Recommended action
Verify event bus handling for RT send success notifications on revenue stamp payments.

---

# 5. L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD
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
Missing `receipt-ok` event (`RT_SEND_SUCCESS`) when processing carts with pre-existing GPD debt positions.

### Category
application bug

### Recommended action
Inspect GPD integration services to verify if existing debt position processing prevents receipt generation/publishing.

---

# 6. L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD`
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
Missing `receipt-ok` event (`RT_SEND_SUCCESS`) during single RPT with GPD revenue stamp payment.

### Category
application bug

### Recommended action
Check backend logs for receipt delivery failures when handling existing GPD stamp items.

---

# 7. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
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
Missing `receipt-ok` event (`RT_SEND_SUCCESS`) when processing single RPT existing in GPD.

### Category
application bug

### Recommended action
Check application logs to confirm if `RT_SEND_SUCCESS` events are delayed or suppressed for pre-existing GPD positions.

---

## Common patterns

- **Systemic Receipt Event Failure (`receipt-ok` / `RT_SEND_SUCCESS`)**: All 7 failures in the `wisp` suite share an identical failure point in `check_wisp_session_timers_del_and_rts_were_sent`, specifically failing the assertion that events with business process `receipt-ok` and status `RT_SEND_SUCCESS` exist. This indicates a widespread outage or breaking change in the receipt dispatching service or event streaming pipeline supporting WISP flow integration tests.

## Cross-suite correlation

Only one suite (`wisp`) was analyzed in this run. No cross-suite correlations across multiple suites can be established at this time.