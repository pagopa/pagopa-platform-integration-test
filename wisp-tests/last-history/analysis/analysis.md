## Suite: wisp

# 1. L'utente tenta di pagare un carrello con due RPT che hanno una quantita di versamenti e marche da bollo oltre il limite
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT che hanno una quantita di versamenti e marche da bollo oltre il limite`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 2. L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 3. L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato valido`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 4. L'utente tenta di pagare un carrello con singola RPT gia esistente in GPD in stato non valido
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con singola RPT gia esistente in GPD in stato non valido`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 5. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 6. L'utente paga un carrello con singola RPT con cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con cinque versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 7. L'utente paga un carrello con tre RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT con un versamento ciascuna`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 8. L'utente tenta di pagare un carrello multibeneficiario con due RPT con una marca da bollo, ma fallisce perche una RPT ha la marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello multibeneficiario con due RPT con una marca da bollo, ma fallisce perche una RPT ha la marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 9. Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 10. L'utente paga un carrello con singola RPT con due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con two versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 11. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 12. L'utente tenta di pagare un carrello con due RPT che hanno una quantita di versamenti oltre il limite
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT che hanno una quantita di versamenti oltre il limite`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 13. L'utente paga un carrello con tre RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di cinque versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 14. Utente paga un pagamento singolo con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento semplice e una marca da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 15. L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 16. L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti oltre il limite
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti oltre il limite`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 17. L'utente paga un carrello multibeneficiario con due RPT con un totale di due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di due versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 18. L'utente paga un carrello con singola RPT con tre versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con tre versamenti`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 19. Utente tenta di pagare un pagamento singolo inserito da ACA e in stato non valido
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente tenta di pagare un pagamento singolo inserito da ACA e in stato non valido`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

# 20. L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD`
- **message**: AssertionError: Response is not valid XML. HTTP status: 401. Body: { "statusCode": 401, "message": "Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription." }
- **trace**:
```

```
### Root cause
HTTP 401 Unauthorized returned by API Gateway/APIM due to invalid or missing subscription key.

### Category
environment

### Recommended action
Verify and update the API subscription key in the test configuration/secrets manager for the WISP environment.

---

## Common patterns
- **Invalid API Gateway Subscription Key**: All 69 failures in the `wisp` suite failed uniformly with HTTP 401 and JSON error message `"Access denied due to invalid subscription key. Make sure to provide a valid key for an active subscription."`.

## Cross-suite correlation
Only one test suite (`wisp`) was analyzed. The single root cause observed across all failures in this run is an environment configuration issue where requests to APIM are rejected due to an expired or missing subscription key. 

**Recommended Action**: Check the CI/CD pipeline environment variables/secrets for the `wisp` suite and provision a valid API Management subscription key.