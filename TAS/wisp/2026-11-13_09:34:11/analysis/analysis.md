# 1. Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
The endpoint returned an HTTP 500 Internal Server Error instead of the expected 200 OK during RPT payment execution.

### Category
application bug

### Recommended action
Investigate backend application logs for HTTP 500 stack traces during RPT payment processing.

---

# 2. L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 returned when processing a single RPT cart with an existing stamp duty position in GPD.

### Category
application bug

### Recommended action
Check backend integration between nodoInviaCarrelloRPT and GPD service for handling existing stamp duties.

---

# 3. Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 internal error thrown when submitting a single RPT payment with two transfers and no stamp duty.

### Category
application bug

### Recommended action
Review server logs for multi-transfer single RPT request handling.

---

# 4. Utente paga un pagamento singolo con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento semplice e una marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 error encountered when processing single RPT payments containing a stamp duty.

### Category
application bug

### Recommended action
Inspect service logs for errors during stamp duty parsing or processing in nodoInviaRPT.

---

# 5. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Server returned HTTP 500 when processing single payment for an existing GPD debt position without stamp duty.

### Category
application bug

### Recommended action
Check GPD integration and database lookups for pre-existing debt positions.

---

# 6. L'utente paga un carrello con singola RPT con due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 internal server error during cart payment with single RPT and multiple transfers.

### Category
application bug

### Recommended action
Examine nodoInviaCarrelloRPT logs for unhandled exceptions when processing multiple transfers.

---

# 7. Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 returned when attempting single payment containing multiple transfers and multiple stamp duties.

### Category
application bug

### Recommended action
Validate backend logic handling multiple stamp duties within single RPT requests.

---

# 8. L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 failure when submitting multi-RPT carts where each RPT contains stamp duties.

### Category
application bug

### Recommended action
Inspect cart handling backend service for errors when aggregating multiple RPTs with stamp duties.

---

# 9. L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
Server returned HTTP 500 during multi-beneficiary cart processing with 5 total transfers.

### Category
application bug

### Recommended action
Check backend logs for errors in multi-beneficiary allocation logic across multi-RPT carts.

---

# 10. L'utente paga un carrello con tre RPT per un totale di dieci versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di dieci versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 error when submitting large multi-RPT carts (3 RPTs, 10 transfers).

### Category
application bug

### Recommended action
Investigate server logs to determine if payload size or transfer processing limits trigger the 500 error.

---

# 11. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 internal failure during retry flow after payment closure failure.

### Category
application bug

### Recommended action
Analyze payment closure and retry state machine logic in backend service logs.

---

# 12. L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 error processing multi-RPT cart with pre-existing stamp duty debt positions in GPD.

### Category
application bug

### Recommended action
Verify GPD synchronization logic when resolving existing debt positions with stamp duties.

---

# 13. L'utente paga un carrello con tre RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di cinque versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 error returned on multi-RPT cart execution (3 RPTs, 5 transfers).

### Category
application bug

### Recommended action
Check backend system log for errors occurring during multi-RPT submission.

---

# 14. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 internal server error returned for basic single payment flow via nodoInviaRPT.

### Category
application bug

### Recommended action
Check core service availability and error logs for basic nodoInviaRPT execution.

---

# 15. Utente tenta il pagamento, poi riprova il flusso ma fallisce
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente tenta il pagamento, poi riprova il flusso ma fallisce`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 error during execution of retry attempt scenario for single payment flow.

### Category
application bug

### Recommended action
Examine application retry handling and state preservation between consecutive attempts.

---

# 16. L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 response during multi-beneficiary cart processing across 4 transfers.

### Category
application bug

### Recommended action
Inspect logs for failure in multi-beneficiary payment orchestration.

---

# 17. Utente tenta due volte di pagare la stessa RPT ma la conversione al nuovo modello fallisce
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente tenta due volte di pagare la stessa RPT ma la conversione al nuovo modello fallisce`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 returned during duplicate RPT payment conversion flow.

### Category
application bug

### Recommended action
Investigate backend model conversion service and idempotency handling for duplicate RPT requests.

---

# 18. L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 error when processing single RPT cart linked to an existing GPD debt position without stamp duty.

### Category
application bug

### Recommended action
Check service-to-service communication logs between WISP/Nodo and GPD service.

---

# 19. L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 error during cart processing with two RPTs and multiple transfers against existing GPD positions.

### Category
application bug

### Recommended action
Review server handling of multi-transfer existing debt positions during cart submission.

---

# 20. L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```
[... earlier frames omitted ...]
        expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
### Root cause
HTTP 500 failure when executing single RPT cart payment with multiple transfers mapped to existing GPD positions.

### Category
application bug

### Recommended action
Inspect backend logs for exception details when querying and mapping GPD debt positions.

---

## Common patterns
- **Systemic HTTP 500 Failures**: All failed test cases across `nodoInviaRPT` and `nodoInviaCarrelloRPT` endpoints failed due to receiving HTTP 500 Internal Server Error instead of HTTP 200 OK.
- **Unstable Core Services / Integration Endpoint**: The uniformity of HTTP 500 errors across diverse test configurations (single/multi RPT, with/without stamp duties, GPD position lookups) points to an unhandled backend runtime exception, microservice outage, or misconfigured integration environment dependency.