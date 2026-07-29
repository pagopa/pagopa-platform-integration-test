# 1. L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD`
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
'services' attribute not present in Settings object; code expects it for healthcheck.

### Category
application bug

### Recommended action
Check test environment initialization; ensure 'services' attribute is configured for Settings.

---

# 2. Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD
- **status**: broken
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD`
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
Settings object lacks expected 'services' attribute, required by healthcheck step.

### Category
application bug

### Recommended action
Validate dynaconf setup; add missing attribute to Settings before running tests.

---

# 3. L'utente paga un carrello con cinque RPT con un versamento ciascuna
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
During healthcheck, Settings object is missing 'services', causing attribute error.

### Category
application bug

### Recommended action
Ensure Settings is properly populated with 'services' data before test execution.

---

# 4. L'utente paga un carrello con tre RPT per un totale di cinque versamenti
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT per un totale di cinque versamenti`
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
Code expects 'services' in Settings; attribute not set in current context.

### Category
application bug

### Recommended action
Review dynaconf initialization; add 'services' as required before invoking steps.

---

# 5. Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo
- **status**: broken
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo`
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
Settings object missing 'services'; healthcheck step fails due to AttributeError.

### Category
application bug

### Recommended action
Add 'services' attribute to Settings, or adjust step to handle missing config gracefully.

---

# 6. L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato valido
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
Test step fails due to missing 'services' attribute on Settings; not initialized.

### Category
application bug

### Recommended action
Initialize 'services' in dynaconf Settings before tests, and enhance error messaging.

---

# 7. L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD`
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
Settings configuration incomplete; test step accesses missing 'services' attribute.

### Category
application bug

### Recommended action
Review dynaconf config load; ensure 'services' attribute exists and is correctly loaded.

---

# 8. L'utente tenta di pagare un carrello multibeneficiario con due RPT, in cui la seconda ha due versamenti, ma la seconda RPT contiene piu di un versamento
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello multibeneficiario con due RPT, in cui la seconda ha due versamenti, ma la seconda RPT contiene piu di un versamento`
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
Missing 'services' attribute on Settings leads to exception during healthcheck.

### Category
application bug

### Recommended action
Fix Settings initialization path; ensure 'services' is present before running steps.

---

# 9. L'utente tenta di pagare un carrello con due RPT che hanno una quantita di versamenti oltre il limite
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con due RPT che hanno una quantita di versamenti oltre il limite`
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
Context.settings missing 'services', causes AttributeError in healthcheck.

### Category
application bug

### Recommended action
Improve test setup; add 'services' attribute to Settings or handle absence gracefully.

---

# 10. L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti oltre il limite
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti oltre il limite`
- **message**: AttributeError: 'Settings' object has no attribute 'SERVICES'
- **trace**:
```
File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/model.py", line 1329, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/behave/matchers.py", line 98, in run
    self.func(context, *args, **kwargs