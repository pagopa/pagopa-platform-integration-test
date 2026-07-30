# 1. L'utente paga un carrello con cinque RPT con un versamento ciascuna
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con cinque RPT con un versamento ciascuna`
- **message**: AttributeError: 'Settings' object has no attribute 'SERVICES'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 14, in system_up
    for key, value in context.settings.services.items():
                      ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 144, in __getattr__
    value = getattr(self._wrapped, name)
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 332, in __getattribute__
    return super().__getattribute__(name)
           ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
```

### Root cause
The test fails because the 'Settings' object is missing the 'SERVICES' attribute, leading to an AttributeError in the healthcheck.

### Category
application bug

### Recommended action
Ensure that 'SERVICES' is properly set in Settings, or update the code to access the correct attribute name.

---

# 2. L'utente tenta di pagare un carrello multibeneficiario inserito da ACA e in stato valido
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello multibeneficiario inserito da ACA e in stato valido`
- **message**: AttributeError: 'Settings' object has no attribute 'SERVICES'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 14, in system_up
    for key, value in context.settings.services.items():
                      ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 144, in __getattr__
    value = getattr(self._wrapped, name)
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 332, in __getattribute__
    return super().__getattribute__(name)
           ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
```

### Root cause
'SERVICES' attribute is absent from the Settings object, causing a crash in the healthcheck step.

### Category
application bug

### Recommended action
Investigate why 'SERVICES' is missing and initialize it before use, or adapt the code to correct attribute casing/structure.

---

# 3. L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato valido
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato valido`
- **message**: AttributeError: 'Settings' object has no attribute 'SERVICES'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 14, in system_up
    for key, value in context.settings.services.items():
                      ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 144, in __getattr__
    value = getattr(self._wrapped, name)
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 332, in __getattribute__
    return super().__getattribute__(name)
           ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
```

### Root cause
Test fails due to missing 'SERVICES' on Settings, resulting in an AttributeError.

### Category
application bug

### Recommended action
Update initialization to ensure all required settings are present before healthcheck execution.

---

# 4. L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti e marche da bollo oltre il limite
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti e marche da bollo oltre il limite`
- **message**: AttributeError: 'Settings' object has no attribute 'SERVICES'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 14, in system_up
    for key, value in context.settings.services.items():
                      ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 144, in __getattr__
    value = getattr(self._wrapped, name)
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 332, in __getattribute__
    return super().__getattribute__(name)
           ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
```

### Root cause
Failure is triggered by missing 'SERVICES' attribute in the Settings object required for healthcheck.

### Category
application bug

### Recommended action
Correct the configuration to include 'SERVICES' or update the code to reflect the current settings structure.

---

# 5. L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti`
- **message**: AttributeError: 'Settings' object has no attribute 'SERVICES'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 14, in system_up
    for key, value in context.settings.services.items():
                      ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 144, in __getattr__
    value = getattr(self._wrapped, name)
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 332, in __getattribute__
    return super().__getattribute__(name)
           ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
```

### Root cause
Settings object does not contain the 'SERVICES' attribute, which causes the test to fail at healthcheck.

### Category
application bug

### Recommended action
Validate and update the settings loading mechanism to ensure 'SERVICES' exists before usage.

---

# 6. L'utente tenta di pagare un carrello multibeneficiario con due RPT con una marca da bollo, ma fallisce perche una RPT ha la marca da bollo
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello multibeneficiario con due RPT con una marca da bollo, ma fallisce perche una RPT ha la marca da bollo`
- **message**: AttributeError: 'Settings' object has no attribute 'SERVICES'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 14, in system_up
    for key, value in context.settings.services.items():
                      ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 144, in __getattr__
    value = getattr(self._wrapped, name)
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 332, in __getattribute__
    return super().__getattribute__(name)
           ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
```

### Root cause
Error arises due to missing 'SERVICES' in the Settings utilized by healthcheck.

### Category
application bug

### Recommended action
Review initial settings load and healthcheck code to ensure proper attribute availability.

---

# 7. L'utente paga un carrello con singola RPT con cinque versamenti
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con cinque versamenti`
- **message**: AttributeError: 'Settings' object has no attribute 'SERVICES'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 14, in system_up
    for key, value in context.settings.services.items():
                      ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 144, in __getattr__
    value = getattr(self._wrapped, name)
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 332, in __getattribute__
    return super().__getattribute__(name)
           ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
```

### Root cause
The 'SERVICES' attribute is missing from Settings in the context, causing crash in pre-test check.

### Category
application bug

### Recommended action
Fix test bootstrap or settings initialization to correctly provide the 'SERVICES' key.

---

# 8. Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo
- **status**: broken
- **fullName**: `Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo`
- **message**: AttributeError: 'Settings' object has no attribute 'SERVICES'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 14, in system_up
    for key, value in context.settings.services.items():
                      ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 144, in __getattr__
    value = getattr(self._wrapped, name)
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 332, in __getattribute__
    return super().__getattribute__(name)
           ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
```

### Root cause
The initialization of Settings lacks the 'SERVICES' attribute, causing healthcheck failure.

### Category
application bug

### Recommended action
Audit the settings loading sequence or correct the attribute access in the healthcheck step.

---

# 9. L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo`
- **message**: AttributeError: 'Settings' object has no attribute 'SERVICES'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "src/integration/wisp/steps/healthcheck.py", line 14, in system_up
    for key, value in context.settings.services.items():
                      ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 144, in __getattr__
    value = getattr(self._wrapped, name)
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line 332, in __getattribute__
    return super().__getattribute__(name)
           ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
```

### Root cause
Absence of 'SERVICES' from the context Settings object causes AttributeError and failure.

### Category
application bug

### Recommended action
Ensure 'SERVICES' exists in settings context and is loaded as expected during test setup.

---

# 10. L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo`
- **message**: AttributeError: 'Settings' object has no attribute 'SERVICES'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib