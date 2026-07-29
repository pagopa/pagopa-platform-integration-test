# 1. L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti
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
All tests fail due to `Settings` missing the attribute `SERVICES`, likely a misconfiguration.
### Category
environment
### Recommended action
Ensure the test environment loads all required configuration variables for `Settings`, especially `SERVICES`.

---

# 2. Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo
- **status**: broken
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo`
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
Missing configuration attribute in test context, preventing service discovery.
### Category
environment
### Recommended action
Update or regenerate the configuration for the integration environment to include `services`.

---

# 3. Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo
- **status**: broken
- **fullName**: `Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT: Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo`
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
The environment lacks the required `SERVICES` attribute in the settings configuration.
### Category
environment
### Recommended action
Verify dynaconf settings definition (`settings.toml` or env vars) and patch with the `SERVICES` section.

---

# 4. Utente tenta di pagare un pagamento singolo inserito da ACA e in stato valido
- **status**: broken
- **fullName**: `Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT: Utente tenta di pagare un pagamento singolo inserito da ACA e in stato valido`
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
Configuration for `Settings` is missing, causing test setup to fail.
### Category
environment
### Recommended action
Correct settings initialization and ensure all attributes (especially `SERVICES`) are present.

---

# 5. L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo`
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
Test context initialization fails due to absent `SERVICES` attribute.
### Category
environment
### Recommended action
Review and update configuration setup for test environment; possibly recreate `context.settings`.

---

# 6. L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo`
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
Settings not properly injected into test context; cannot access `services`.
### Category
environment
### Recommended action
Check environment variables and dynaconf configuration files for completeness.

---

# 7. L'utente paga un carrello con singola RPT con due versamenti
- **status**: broken
- **fullName**: `L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT: L'utente paga un carrello con singola RPT con due versamenti`
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
Global settings object misconfigured or incomplete.
### Category
environment
### Recommended action
Revisit dynaconf settings file and environment setup, ensuring `services` attribute exists.

---

# 8. Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD
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
Context.settings lacks required configuration, blocking test execution.
### Category
environment
### Recommended action
Validate settings loading logic; assign `services` object before test execution.

---

# 9. Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo
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
Missing attribute in dynamic configuration object.
### Category
environment
### Recommended action
Confirm dynaconf config contains all required keys (`services`).

---

# 10. L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti e marche da bollo oltre il limite
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
  File "/opt/hostedtoolcache/Python/3.14.6/x64/lib/python3.14/site-packages/dynaconf/base.py", line