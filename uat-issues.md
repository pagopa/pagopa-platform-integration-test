# Problemi UAT — WISP Integration Tests (PQ-514)

**Stato**: 12 passati · 56 falliti · 2 saltati (su 70 scenari)

---

## Problema 1 — RT_SEND_SUCCESS non presente negli eventi RE (34 fallimenti)

**Scenari coinvolti**: tutti gli happy path di `nodoInviaRPT_noStamp`, `nodoInviaRPT_withStamp`, `nodoInviaCarrelloRPT_noStamp`, `nodoInviaCarrelloRPT_withStamp`, `nodoInviaCarrelloRPT_multibeneficiary`

**Errore**:
```
Assertion Failed: There are no events with business process receipt-ok 
and field status containing value [RT_SEND_SUCCESS].
```

**Causa**: Dopo `closePayment OK`, il servizio RT-sender in UAT non emette l'evento `RT_SEND_SUCCESS` nel RE entro i 10 secondi di attesa del test. Le chiamate HTTP (nodoInvia*, GPD, closePayment) restituiscono tutte 200 OK.

**Cosa serve per risolvere**:
- Verificare che il servizio **RT-sender** sia correttamente deployato e attivo in UAT
- Verificare che l'endpoint dell'ente creditore configurato in UAT per `15376371009` sia raggiungibile
- In alternativa, aumentare il timeout di attesa nel test (`steps_utils.py`) se il servizio e' semplicemente lento

---

## Problema 2 — GPD restituisce HTTP 400 sulla creazione del debt position (22 fallimenti)

**Scenari coinvolti**: tutti gli scenari di `nodoInviaRPT_existingPaymentPosition` e `nodoInviaCarrelloRPT_existingPaymentPosition`

**Errore**:
```
Assertion Failed: The debt position for RPT with index [first] was not created.
Expected status code [201], Current status code [400].
```

**Causa**: Il test tenta di creare una payment position su GPD UAT per l'ente creditore `15376371009` con segregation code `48` prima dell'esecuzione dello scenario. GPD restituisce 400, indicando che l'ente non e' configurato o che il payload non e' valido per l'ambiente UAT.

**Cosa serve per risolvere**:
- Registrare l'ente creditore **`15376371009`** in UAT GPD con segregation code **`48`**
- Oppure aggiornare `commondata.yaml` con un `creditor_institution` e segregation code validi per UAT

---

## Fix applicato in questo branch

- `steps_utils.py` riga 555: corretto bug sulla chiave dizionario (`status_code` intero usato come chiave invece della stringa `'status_code'`) — non causava fallimenti attuali ma sarebbe emerso una volta risolti i problemi sopra.
