## Suite: wisp

# 1. L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD
- **status**: failed
- **fullName**: `ExistingPaymentPosition_L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
                        f'There are not events with business process {business_process}.')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
```
### Root cause
Missing `receipt-ok` event in event streaming/storage service following successful payment flow.

### Category
application bug

### Recommended action
Verify receipt-ok event generation and publication pipeline in payment engine logs for the scenario execution.

---

# 2. Utente paga un pagamento singolo con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Un utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
                        f'There are not events with business process {business_process}.')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
```
### Root cause
Missing `receipt-ok` event in event streaming/storage service following successful payment flow.

### Category
application bug

### Recommended action
Check message broker/event listener logs to ensure receipt-ok event processing is functioning properly.

---

# 3. L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo
- **status**: failed
- **fullName**: `WithStamp_L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
                        f'There are not events with business process {business_process}.')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
```
### Root cause
Missing `receipt-ok` event in event streaming/storage service following successful payment flow.

### Category
application bug

### Recommended action
Investigate event hub indexing latency or failures in triggering receipt-ok business process.

---

# 4. L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti
- **status**: failed
- **fullName**: `MultiBeneficiario_L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
                        f'There are not events with business process {business_process}.')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
```
### Root cause
Missing `receipt-ok` event in event streaming/storage service following successful payment flow.

### Category
application bug

### Recommended action
Validate receipt emission mechanisms specifically for multi-beneficiary RPT payment flows.

---

# 5. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo
- **status**: failed
- **fullName**: `NoStamp_L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
    steputils.send_closePaymentV2_request(context)
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 908, in send_closePaymentV2_request
    check_status_code(context, 'creditor istitution', '200')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 35, in check_status_code
    assert int(expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
```
### Root cause
`closePaymentV2` API endpoint returned HTTP 500 Internal Server Error (activityId `0a27b72c-d60b-4fc5-b982-ce08e8a2ee00`).

### Category
application bug

### Recommended action
Inspect server logs for `closepayment` service matching activityId `0a27b72c-d60b-4fc5-b982-ce08e8a2ee00` to resolve unhandled backend error.

---

# 6. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `WithStamp_L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
                        f'There are not events with business process {business_process}.')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
```
### Root cause
Missing `receipt-ok` event in event streaming/storage service following successful payment flow.

### Category
application bug

### Recommended action
Check whether stamp-only payment processing suppresses or fails to emit standard receipt-ok events.

---

# 7. L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `WithStamp_L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
                        f'There are not events with business process {business_process}.')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
```
### Root cause
Missing `receipt-ok` event in event streaming/storage service following successful payment flow.

### Category
application bug

### Recommended action
Verify event generation logic during multi-RPT mixed simple/stamp payment processing.

---

# 8. L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `ExistingPaymentPosition_L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 431, in check_event
    assert_show_message(len(needed_process_events) > 0,
                        f'There are not events with business process {business_process}.')
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.py", line 7, in assert_show_message
    assert assertion_value, message
```
### Root cause
Missing `receipt-ok` event in event streaming/storage service following successful payment flow.

### Category
application bug

### Recommended action
Inspect event dispatcher for GPD existing debt position payment paths.

---

## Common patterns
- **Missing `receipt-ok` events (7 out of 8 failures)**: The vast majority of failures across single/multi RPT, GPD existing positions, and stamp-based payment scenarios stem from missing `receipt-ok` events in `check_event`. This indicates a potential systemic issue in event generation or indexing during payment finalization.
- **`closePaymentV2` HTTP 500 error (1 failure)**: A distinct failure occurred during payment retry handling due to an internal server error in `closepayment` (Activity ID: `0a27b72c-d60b-4fc5-b982-ce08e8a2ee00`).

## Cross-suite correlation
Only a single suite (`wisp`) was analyzed in this report. Across the patterns within this suite, two main actionable tracks exist:
1. **Event Streaming Pipeline**: Investigate event publication for business process `receipt-ok` across payment handlers.
2. **Backend ClosePayment API**: Address HTTP 500 internal server exceptions in `closePaymentV2`.