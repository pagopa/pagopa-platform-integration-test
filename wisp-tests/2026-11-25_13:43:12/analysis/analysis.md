## Suite: checkout

No test failures found in the 'Checkout E2E' suite; execution was complete and no tests were skipped.

## Suite: fdr3

No test failures found in the 'FDR-3' suite; execution was complete and no tests were skipped.

## Suite: wisp

# 1. L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
  File "src/integration/wisp/steps/steps.py", line 197, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 926, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
                        f'There are not events with business process {business_process}.')
```
### Root cause
The asynchronous event processing service failed to generate or publish the expected `receipt-ok` event with status `RT_SEND_SUCCESS` after transaction processing.

### Category
application bug

### Recommended action
Investigate the receipt generation service logs for transaction processing errors and verify if event delivery to the event stream/bus timed out or failed.

---

# 2. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 926, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
                        f'There are not events with business process {business_process}.')
```
### Root cause
The system failed to publish the `receipt-ok` event (`RT_SEND_SUCCESS`) during payment flow for an existing debt position in GPD.

### Category
application bug

### Recommended action
Check the integration between GPD and the receipt notification pipeline to ensure payment receipts (RT) are dispatched correctly for existing debt positions.

---

# 3. L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
  File "src/integration/wisp/steps/steps.py", line 197, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 926, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
                        f'There are not events with business process {business_process}.')
```
### Root cause
The system failed to register the `receipt-ok` event (`RT_SEND_SUCCESS`) during execution of multi-beneficiary carts with five payments.

### Category
application bug

### Recommended action
Inspect WISP receipt processing for multi-beneficiary RPT carts to confirm all receipt messages are being generated and dispatched to the event consumer.

---

# 4. Utente paga un pagamento singolo con due versamenti semplici e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti semplici e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 926, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
                        f'There are not events with business process {business_process}.')
```
### Root cause
The missing `receipt-ok` event (`RT_SEND_SUCCESS`) prevented verification of successful receipt handling for single payments containing digital stamps ("marca da bollo").

### Category
application bug

### Recommended action
Verify whether payments involving digital stamp attachments encounter silent failures during receipt (RT) generation or event stream publishing.

---

## Common patterns
All 4 failures in the **wisp** suite share a single identical root cause: `AssertionError: There are not events with business process receipt-ok.` occurring within `check_wisp_session_timers_del_and_rts_were_sent`. This indicates a centralized breakdown or systemic latency in the downstream event emission or ingestion mechanism responsible for recording successful receipt (`RT_SEND_SUCCESS`) events across various payment scenarios.

---

## Cross-suite correlation

- **checkout**: 0 failures (Execution complete).
- **fdr3**: 0 failures (Execution complete).
- **wisp**: 4 failures (100% caused by missing `receipt-ok` / `RT_SEND_SUCCESS` events across diverse payment flows).

### Consolidated Analysis & Recommendation
The failures are strictly isolated to the **wisp** suite, while **checkout** and **fdr3** passed cleanly. Because all failing tests across different flow types (multi-beneficiary, GPD-linked, and digital stamp payments) share the exact same assertion error on `receipt-ok`, the issue is not specific to business domain variations. 

**Action Item**: Check the health and logs of the WISP event streamer/bus and receipt delivery service (RT processor) in the test environment. If the service is healthy, verify whether recent updates introduced latency, requiring an increased polling dynamic wait/retry timeout in `check_event` within `steps_utils.py`.