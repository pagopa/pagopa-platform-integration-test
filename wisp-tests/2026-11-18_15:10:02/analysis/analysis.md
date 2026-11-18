## Suite: wisp

# 1. L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato valido`
- **message**: AssertionError: There are no events with business process redirect and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
The expected `RT_SEND_SUCCESS` event with business process redirect/receipt was not produced during the cart payment flow.

### Category
application bug

### Recommended action
Verify the backend service handling `nodoInviaCarrelloRPT` to ensure RT messages are successfully processed and dispatched.

---

# 2. Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo`
- **message**: AssertionError: There are no events with business process receipt-ok and field status containing value [RT_SEND_SUCCESS].
- **trace**:
```
[... earlier frames omitted ...]
    assert assertion_value, message
           ^^^^^^^^^^^^^^^
```
### Root cause
Single payment execution via `nodoInviaRPT` failed to trigger the expected `RT_SEND_SUCCESS` event.

### Category
application bug

### Recommended action
Check the payment gateway integration and event emission logic for single payments with stamps.

---

## Cross-suite correlation
- **Failure Pattern**: All WISP suite failures consistently fail on `AssertionError` regarding missing `RT_SEND_SUCCESS` events across various payment modalities (`nodoInviaCarrelloRPT`, `nodoInviaRPT`).
- **Recommended Action**: Perform a comprehensive audit of the event notification and RT generation pipeline within the WISP module to ensure proper propagation and status updating.