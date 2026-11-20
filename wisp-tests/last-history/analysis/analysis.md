## Suite: wisp

# 1. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```

### Root cause
The test expected a `receipt-ok` event with status `RT_SEND_SUCCESS`, but no such event was found in the event stream for the payment session.

### Category
application bug

### Recommended action
Investigate why the receipt generation/delivery service failed to emit the `receipt-ok` event with status `RT_SEND_SUCCESS` during WISP checkout flow.

---

# 2. L'utente paga un carrello con singola RPT con un versamento
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```

### Root cause
Missing `receipt-ok` event with `RT_SEND_SUCCESS` status following payment completion of a single RPT cart without digital stamps.

### Category
application bug

### Recommended action
Check backend receipt notification delivery logs to verify if RT transmission was interrupted or asynchronous event ingestion was delayed.

---

# 3. Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```

### Root cause
Missing `receipt-ok` event with status `RT_SEND_SUCCESS` after single RPT payment execution containing four transfers.

### Category
application bug

### Recommended action
Verify receipt-ok event generation logic in the event hub/bus for multi-transfer single RPT payments via `nodoInviaRPT`.

---

# 4. L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
[... earlier frames omitted ...]
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.15.2/x64/lib/python3.15/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
```

### Root cause
Missing `receipt-ok` event with `RT_SEND_SUCCESS` status during checkout verification for RPT cart containing two transfers and a digital stamp.

### Category
application bug

### Recommended action
Inspect event publisher and receipt status handler for multi-transfer RPT carts with digital stamps.

---

## Common patterns
All 4 test failures across `wisp` share the identical failure pattern: `AssertionError: There are not events with business process receipt-ok.`. In each case, the checkout flow step `check_wisp_session_timers_del_and_rts_were_sent` failed to find a `receipt-ok` event marked with `RT_SEND_SUCCESS`. This points to a systematic failure or processing latency in emitting or persisting `receipt-ok` events in the test environment during payment receipt processing.


## Cross-suite correlation
Only one test suite (`wisp`) was analyzed. All observed failures are uniform and tied to missing `receipt-ok` event occurrences within the WISP receipt processing flow.