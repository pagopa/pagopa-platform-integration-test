# Istruzioni

Le istruzioni definiscono regole di lavoro; non sono skill da invocare.
Il frontmatter `applyTo`, quando presente, indica lo scope per il client;
ogni agente deve comunque leggere esplicitamente i file assegnati dal
[contratto del repository](../../AGENTS.md#agent-instruction-loading-policy).
Non caricare indiscriminatamente istruzioni o lezioni di altri ruoli.

## Regole operative

| File | Scope / utilizzatore | Contenuto |
| --- | --- | --- |
| [gherkin.instructions.md](gherkin.instructions.md) | `src/**/*.feature`; QA-analyst | Design Gherkin, identita/tag stabili, copertura, outline e celle vuote come null. Legge il [profilo Gherkin](../profiles/gherkin.profile.yaml). |
| [python-scripts.instructions.md](python-scripts.instructions.md) | `**/*.py`; chi crea/modifica Python, inclusi engineer e utility engineer | Docstring, tipi, compatibilita, riuso, errori, risorse e verifica proporzionata. Non concede permessi di esecuzione. |
| [behave-steps.instructions.md](behave-steps.instructions.md) | `src/**/steps/**/*.py`; QA-engineer | Binding/matcher, context lifecycle, input strutturati, assertion, attese e riuso utility. Si aggiunge alle regole Python e legge il [profilo Behave](../profiles/behave-steps.profile.yaml). |
| [run-tests.instructions.md](run-tests.instructions.md) | Esecuzione/diagnosi; QA-runner | Interprete, selezione suite, configurazione effettiva, evidenze, exit code, preflight e interruzioni. Gli esempi non autorizzano run o installazioni. |

QA-orchestrator legge le istruzioni operative previste per il coordinamento;
QA-closer usa le skill di pubblicazione/documentazione assegnate, senza acquisire
permessi di implementazione o esecuzione.

## Lezioni ACE per ruolo

| File | Destinatario |
| --- | --- |
| [ace-qa-orchestrator.instructions.md](ace-qa-orchestrator.instructions.md) | QA-orchestrator |
| [ace-qa-analyst.instructions.md](ace-qa-analyst.instructions.md) | QA-analyst |
| [ace-qa-engineer.instructions.md](ace-qa-engineer.instructions.md) | QA-engineer |
| [ace-qa-runner.instructions.md](ace-qa-runner.instructions.md) | QA-runner |
| [ace-qa-closer.instructions.md](ace-qa-closer.instructions.md) | Qa-closer |

Sono lezioni generate, lette solo dal ruolo assegnato prima del lavoro; citare
gli eventuali `P-NNN` applicati. Non editarle manualmente o usarle per superare
regole e approvazioni. Python-utility-engineer non carica lezioni di un altro ruolo.

## Esempio

Richiesta a QA-engineer:

> Modifica solo gli step Python allegati. Leggi le istruzioni Python e Behave e
> il profilo associato; conserva testo dei binding e semantica dei dati null.
> Restituisci modifiche e verifiche proposte, senza eseguire test.

Le convenzioni guidano l'implementazione; scope, ownership e permessi restano
nel contratto dell'[agente](../agents/README.md).
