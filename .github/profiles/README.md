# Profili

I profili YAML contengono valori di progetto usati dalle
[istruzioni](../instructions/README.md). Non sono configurazioni di ambiente,
launcher o validatori automatici: leggerli non esegue controlli.
Risolvere i percorsi dalla root del repository; un profilo mancante, malformato
o contraddittorio blocca le modifiche dipendenti, senza valori inventati.

## Catalogo

| Profilo | Usato da | Valori principali |
| --- | --- | --- |
| [gherkin.profile.yaml](gherkin.profile.yaml) | [Istruzioni Gherkin](../instructions/gherkin.instructions.md), QA-analyst | Lingua italiana per nuovo contenuto; massimo 12 definizioni Scenario/Outline per file; naming, indentazione e tag QA Hub. Regex in dialetto Python `re`, con gruppi nominati. |
| [behave-steps.profile.yaml](behave-steps.profile.yaml) | [Istruzioni Behave](../instructions/behave-steps.instructions.md), QA-engineer | README delle utility da leggere e template `src/<test-type>/<suite>/utility`, risolto con tipo e suite effettivi. |

Le istruzioni governano semantica e compatibilità; i profili ne forniscono i
parametri. Non duplicare qui regole null, ownership o autorizzazioni.
Non esistono in questa cartella profili dedicati a Python generico o al runner.

## Esempi d'uso

- **Gherkin:** `# qa-hub: FEAT_001_FdR3` è la fonte dell’identità; i tag
  corrispondenti sono `@FDR3_001` e `@FDR3_001_01`. Gli identificativi numerici
  di tracking precedenti sono deprecati. Un Outline conta come una definizione,
  non come le sue righe.
- **Behave:** con tipo `api` e suite `cart`, il template risolve
  `src/api/cart/utility`. Prima di aggiungere un helper leggere i README
  elencati e cercare riuso. La risoluzione non autorizza a creare directory,
  migrare helper legacy o modificare utility assegnate a un altro writer.

Per modificare una convenzione, aggiornare il profilo pertinente e valutarne i
consumatori; non dedurre una migrazione globale dei file esistenti.
