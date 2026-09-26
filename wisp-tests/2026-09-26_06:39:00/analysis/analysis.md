# 1. Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 2. L'utente paga un carrello con singola RPT con un versamento
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 3. L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 4. L'utente paga un carrello con singola RPT con due versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 5. Utente paga un pagamento singolo con un versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento semplice e una marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/steps.py", line 172, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_timers_del_and_rts_were_sent
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/integration/wisp/utility/steps_utils.py", line 403, in check_event
    assert_show_message(len(needed_process_events) > 0,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        f'There are not events with business process {business_process}.')
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/pagopa-platform-integration-test/pagopa-platform-integration-test/src/utility/assertions.p
```
### Root cause
The expected `receipt-ok` event with status `RT_SEND_SUCCESS` was not generated or captured during the checkout process flow.

### Category
application bug

### Recommended action
Inspect the backend receipt generation service logs to see why the receipt process event was missing or failed to trigger.

---

# 6. L'utente paga un carrello con singola RPT con cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con cinque versamenti`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 7. Utente esegue un primo reindirizzamento, poi ripete il reindirizzamento e completa il flusso di pagamento
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente esegue un primo reindirizzamento, poi ripete il reindirizzamento e completa il flusso di pagamento`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 8. L'utente paga un carrello con singola RPT con tre versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con tre versamenti`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 9. L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 10. Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 11. L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 12. Utente tenta di pagare un pagamento singolo inserito da ACA e in stato valido
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente tenta di pagare un pagamento singolo inserito da ACA e in stato valido`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 13. L'utente paga un carrello con cinque RPT con un versamento ciascuna
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con cinque RPT con un versamento ciascuna`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 14. Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 15. L'utente paga un carrello con due RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT per un totale di cinque versamenti`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 16. Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 17. L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 18. L'utente tenta di pagare un carrello multibeneficiario con tre RPT con un versamento ciascuna, ma il carrello ha piu di 2 RPT
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello multibeneficiario con tre RPT con un versamento ciascuna, ma il carrello ha piu di 2 RPT`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 19. L'utente paga un carrello con tre RPT per un totale di cinque versamenti
- **status**: failed
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di cinque versamenti`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

# 20. Utente paga un pagamento singolo con nessun versamento semplice e una marca da bollo
- **status**: failed
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con nessun versamento semplice e una marca da bollo`
- **message**: AssertionError: health-check systems or subscription-key errors
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.7/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 26, in system_up
    assert responses, f'health-check systems or subscription-key errors'
           ^^^^^^^^^
```
### Root cause
The test suite health-check step failed, indicating that dependent backend systems are down or API subscription keys are invalid.

### Category
environment

### Recommended action
Verify the availability of the target environment's services and check if the API subscription keys are correctly configured.

---

## Common patterns
The vast majority of failures across the test suite stem from the environment health-check step failing (`AssertionError: health-check systems or subscription-key errors`). This points to a global infrastructure or authentication/credential issue (such as expired or incorrect subscription keys, or downstream microservices being completely unavailable) rather than isolated test code bugs.