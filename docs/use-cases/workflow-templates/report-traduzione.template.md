---
schema: uc-translation-report/v1
artifact: translation-report
producer_skill: uc-to-feature
task_id: "{task-id}"
uc_id: "{uc-id}"
uc_slug: "{slug-uc}"
run_id: "{run-id}"
uc_input: "{path-or-stable-chat-reference}"
uc_revision: "{human-confirmed-revision}"
environment: unknown
revision: 1
updated_at: "{ISO-8601-with-offset}"
derived_from:
  - path: "{run-directory}/01-context.md"
    revision: 1
  - path: "{run-directory}/02-test-data.md"
    revision: 1
  - path: "{run-directory}/03-feature-report.md"
    revision: 1
findings: 0
proposals: 0
---

# REPORT {slug-uc}

## README
Questo file raccoglie, a valle della traduzione UC -> feature, i dubbi, le
criticita, gli open point e le friction emersi mentre si creava la feature
`{slug-uc}`. Non e una specifica, non e un report del workflow `uc-workflow/v1`
e non e una fonte per nessuna skill: la feature e stata scritta senza attendere
le risposte qui elencate.

Ogni voce e un **FINDING**, identificato da `FND-XXX`: un dubbio o un'osservazione
che non ha impedito di scrivere la feature, per lo piu di natura implementativa
(API da chiamare, URL, configurazione, componenti UI, tecnologia, come indurre
un errore o preparare uno stato). Servono alla fase successiva, quella
dell'implementazione Python/Behave. Ogni finding riporta `Tipo`
(`implementativo`, `dato`, `funzionale-aperto`, `friction`), `Riferimento`,
`Dubbio o criticita`, `Fonte`, `Proposta` ed `Effetto sulla feature`.

Dopo il separatore `---` sono elencate le **proposte di scenari non coperti
dallo UC**, identificate da `SP-XXX`: scenari suggeriti dalla documentazione ma
assenti dallo UC. Non sono nella feature e non vanno implementate senza che lo
UC li copra.

Gli id `FND-XXX` e `SP-XXX` sono locali a questo file e non vanno confusi con gli
F/S (evidenza e fonti) dei report `01-context.md` e `02-test-data.md`. Fuori da questo file citarli
come `report_traduzione_{slug-uc}.md#FND-001`.

## {slug-uc}
{Sinossi dei problemi trovati: quanti finding, di quali tipi, quali scenari
della feature toccano. `Nessuno` se non ce ne sono.}

### FND-001
- **Tipo**: {implementativo | dato | funzionale-aperto | friction}
- **Riferimento**: {elemento UC, step e scenario della feature interessati}
- **Dubbio o criticita**: {descrizione}
- **Fonte**: {locator della documentazione, oppure `nessuna`}
- **Proposta**: {cosa suggerire alla fase implementativa o a chi mantiene UC e documentazione}
- **Effetto sulla feature**: {nessuno | placeholder `__TODO_D001__` | check non coperto}

### FND-002
{...}

---

## PROPOSTE DI SCENARI NON COPERTI DALLO UC
{Sinossi di quanto seguirebbe: da quale documentazione nasce ciascuna proposta
e quale ancoraggio ha nello UC. `Nessuno` se non ce ne sono.}

### SP-001
{Motivo, fonte e ancoraggio nello UC, poi lo scenario:}

```gherkin
Scenario: {titolo}
  Dato che {...}
  Quando {...}
  Allora {...}
```

### SP-002
{...}
