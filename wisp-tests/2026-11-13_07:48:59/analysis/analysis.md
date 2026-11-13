## Suite: wisp

# 1. L'utente paga un carrello con singola RPT con due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by the Checkout service during the `checkPosition` step.

### Category
application bug

### Recommended action
Inspect Checkout application logs using `activityId: 9413800e-53f2-465e-b048-9…` to trace the unhandled internal server error.

---

# 2. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by the Checkout service during the `checkPosition` step.

### Category
application bug

### Recommended action
Inspect Checkout application logs using `activityId: 34cb1f09-bed7-4548-b36b-1…` to identify the root cause of the failure.

---

# 3. Utente paga un pagamento singolo con nessun versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con nessun versamento semplice e una marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Investigate Checkout logs filtered by `activityId: e8cb3a87-2d88-4c23-a73c-c…` for exception stack traces.

---

# 4. L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Check Checkout backend logs using `activityId: b33ec098-740d-415c-a4bc-8…`.

---

# 5. L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Check Checkout service logs for `activityId: 880f9499-7292-44b8-942c-0…`.

---

# 6. L'utente paga un carrello con singola RPT con tre versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con tre versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Inspect Checkout logs corresponding to `activityId: 073ffeae-3edf-4c46-a0f3-6…`.

---

# 7. Utente tenta il pagamento, poi riprova il flusso ma fallisce
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente tenta il pagamento, poi riprova il flusso ma fallisce`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Search Checkout logs using `activityId: 1e658da1-551f-4177-b02f-d…` to trace the failure.

---

# 8. L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Examine Checkout logs for `activityId: 20fb6e36-a284-4f78-a691-d…`.

---

# 9. Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Check Checkout backend logs for `activityId: 4a845038-e747-4141-acfe-c…`.

---

# 10. L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Inspect Checkout logs using `activityId: c98e6d0f-ddfc-44df-bd56-d…`.

---

# 11. L'utente paga un carrello con tre RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di cinque versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Review Checkout logs for `activityId: 71db4f72-c8b3-45fb-8347-c…`.

---

# 12. L'utente paga un carrello con singola RPT con cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con cinque versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Examine Checkout logs using `activityId: 9617c26a-f75e-444c-99f7-b…`.

---

# 13. Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Investigate Checkout logs with `activityId: d4a7d4fb-b0e9-4d96-8fb6-b…`.

---

# 14. L'utente paga un carrello con singola RPT con un versamento
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Search Checkout backend logs for `activityId: 9d33109a-9e3e-41db-bd44-0…`.

---

# 15. Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Analyze Checkout logs using `activityId: da2b5046-0495-417a-b56d-9…`.

---

# 16. L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Check Checkout service logs for `activityId: 8b1663c9-3dab-4601-b180-3…`.

---

# 17. L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Review Checkout backend logs for `activityId: e5c7fe5d-6b4a-43c2-9784-2…`.

---

# 18. L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Inspect Checkout logs for `activityId: 63a99f93-0e72-49d3-87d0-3…`.

---

# 19. L'utente paga un carrello con cinque RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con cinque RPT con un versamento ciascuna`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Trace Checkout backend execution using `activityId: 371d63ed-5c28-42ad-9c42-3…`.

---

# 20. L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti`
- **message**: AssertionError: The status code is not 200. Current value: 500.
- **trace**:
```

```
### Root cause
HTTP 500 Internal Server Error returned by Checkout during the `checkPosition` step.

### Category
application bug

### Recommended action
Check Checkout application logs using `activityId: 7450e831-3a0e-4540-ab2e-9…`.

---

## Common patterns
- **Checkout Service HTTP 500 Error**: All reported failures across single payment, cart, and existing GPD position scenarios fail during the redirection step to Checkout (`checkPosition`) due to an internal server error (HTTP 500).

## Cross-suite correlation
- **Systemic WISP / Checkout Service Issue**: The failures across all tested scenarios in the WISP suite share the same pattern—an unhandled HTTP 500 error returned by the Checkout service when verifying payment position (`checkPosition`). This indicates a critical downstream service outage or internal fault in Checkout affecting payment redirection.