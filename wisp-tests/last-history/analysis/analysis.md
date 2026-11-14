## Suite: wisp

# 1. L'utente paga un carrello con tre RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT con un versamento ciascuna`
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
The payment receipt processing service failed to generate or emit the expected `receipt-ok` event with `RT_SEND_SUCCESS` status.

### Category
application bug

### Recommended action
Verify downstream receipt delivery services and event bus messaging to ensure `receipt-ok` events are published upon RT dispatch.

---

# 2. L'utente paga un carrello con due RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT per un totale di cinque versamenti`
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
The system failed to trigger the required `receipt-ok` event with status `RT_SEND_SUCCESS` for multi-RPT carts.

### Category
application bug

### Recommended action
Check the event publisher logs and receipt handling component for multi-item cart payment flows.

---

# 3. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
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
Missing `receipt-ok` event with `RT_SEND_SUCCESS` status when processing existing GPD debt position payments.

### Category
application bug

### Recommended action
Investigate the integration between GPD payment receipt status updates and the event generation service.

---

## Common patterns
All 3 failures across the WISP suite share identical assertion failures (`AssertionError: There are not events with business process receipt-ok.`) during the check for receipt transmission (`check_wisp_session_timers_del_and_rts_were_sent`). This indicates a systematic break in the receipt creation or event propagation pipeline for WISP payment flows.

---

## Cross-suite correlation
Only the `wisp` suite was provided in this run. All failures stem from a single systemic issue: missing `receipt-ok` event generation with status `RT_SEND_SUCCESS` across various payment cart configurations (single RPT, multi-RPT, and GPD debt position payments).