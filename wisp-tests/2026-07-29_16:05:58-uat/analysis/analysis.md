# 1. Utente paga un pagamento singolo con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
```
### Root cause
Missing 'receipt-ok' event during business process, indicating receipt generation failed or was not tracked.

### Category
application bug

### Recommended action
Validate receipt generation logic and event tracking; check if downstream services are functioning and emitting events as expected.

---

# 2. L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
```
### Root cause
Receipt event not generated or not visible for carrello with multiple RPT and bollo, possibly due to process error.

### Category
application bug

### Recommended action
Investigate multi-RPT handling and event emission, with focus on receipt and bollo scenarios.

---

# 3. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
```
### Root cause
'Receipt-ok' event not produced; may be due to incorrect handling of GPD pre-existing positions.

### Category
application bug

### Recommended action
Review payment flows for GPD positions and event publishing; add logging for missed receipt events.

---

# 4. L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
```
### Root cause
No receipt event for pre-existing GPD position; edge-case logic may be missing.

### Category
application bug

### Recommended action
Enhance edge-case handling in GPD workflows, ensure event emission for bollo and non-bollo items.

---

# 5. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
```
### Root cause
Single-payment flow fails to publish receipt event, indicating missing or failed integration.

### Category
application bug

### Recommended action
Inspect single-payment processing and integration points for missing receipt event; confirm downstream communication.

---

# 6. L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
```
### Root cause
Receipt event not posted for multi-payment GPD positions; likely missing in event emission logic.

### Category
application bug

### Recommended action
Audit GPD flow for multi-payment scenarios; add error handling and event coverage.

---

# 7. L'utente paga un carrello con singola RPT con un versamento
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
```
### Root cause
No 'receipt-ok' event for single RPT carrello; process signaling missing.

### Category
application bug

### Recommended action
Check carrello handler for single RPT and ensure receipt trigger is present.

---

# 8. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
```
### Root cause
Unusual case—no versamento with marca da bollo—results in missed receipt emission.

### Category
application bug

### Recommended action
Validate process for rare input combinations (no versamento + bollo); enforce event output.

---

# 9. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 197, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
```
### Root cause
Retry logic may not trigger receipt event if initial payment closure failed.

### Category
application bug

### Recommended action
Implement robust receipt event handling post-retry; audit rollback and retry flows.

---

# 10. Utente paga un pagamento singolo con nessun versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con nessun versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
```
### Root cause
Handling for payments with only bollo and no versamento does not emit receipt event.

### Category
application bug

### Recommended action
Correct receipt logic for 'bollo only' cases; add test coverage.

---

# 11. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/