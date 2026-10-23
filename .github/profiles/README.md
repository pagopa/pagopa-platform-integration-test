# Profili

I profili YAML contengono valori di progetto usati dalle
[istruzioni](../instructions/README.md). Non sono configurazioni di ambiente,
launcher o validatori automatici: leggerli non esegue controlli.
Risolvere i percorsi dalla root del repository; un profilo mancante, malformato
o contraddittorio blocca le modifiche dipendenti, senza valori inventati.

## Catalogo

| Profilo | Usato da | Valori principali |
| --- | --- | --- |
| [gherkin.profile.yaml](gherkin.profile.yaml) | [Istruzioni Gherkin](../instructions/gherkin.instructions.md), QA-analyst | Lingua italiana; massimo 12 definizioni Scenario/Outline per file; naming, indentazione, tag e tracking. Regex in dialetto Python `re`, con gruppi nominati. |
| [behave-steps.profile.yaml](behave-steps.profile.yaml) | [Istruzioni Behave](../instructions/behave-steps.instructions.md), QA-engineer | README delle utility da leggere e template `src/<test-type>/<suite>/utility`, risolto con tipo e suite effettivi. |

Le istruzioni governano semantica e compatibilita; i profili ne forniscono i
parametri. Non duplicare qui regole null, ownership o autorizzazioni.
Non esistono in questa cartella profili dedicati a Python generico o al runner.

## Esempi d'uso

- **Gherkin:** `FEAT_001_FdR3_Aggiungi_pagamenti.feature` usa il token suite
  `FdR3`; i tag corrispondenti possono essere `@fdr3_001_Aggiungi_pagamenti`
  e `@fdr3_001_01`. Sono esempi di forma: allocare ID/tracking reali e preservare
  quelli esistenti. Un Outline conta come una definizione, non come le sue righe.
- **Behave:** con tipo `api` e suite `cart`, il template risolve
  `src/api/cart/utility`. Prima di aggiungere un helper leggere i README
  elencati e cercare riuso. La risoluzione non autorizza a creare directory,
  migrare helper legacy o modificare utility assegnate a un altro writer.

Per modificare una convenzione, aggiornare il profilo pertinente e valutarne i
consumatori; non dedurre una migrazione globale dei file esistenti.
