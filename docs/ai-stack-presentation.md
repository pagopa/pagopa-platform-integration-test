---
marp: true
html: true
title: Stack AI operativo per QA e agentic coding
description: Presentazione tecnica di 18-20 minuti sullo stack AI del repository, sugli asset Markdown e sul workflow agentico.
theme: default
paginate: true
size: 16:9
footer: Stack AI operativo | pagopa-platform-integration-test - Daniele Quero
style: |
  :root {
    --color-primary:   #1565c0;
    --color-secondary: #1e88e5;
    --color-accent:    #29b6f6;
    --color-light:     #e3f2fd;
    --color-bg:        #f0f7ff;
  }

  section {
    background: linear-gradient(160deg, var(--color-bg) 0%, #ffffff 100%);
    color: #0d2a4a;
    font-size: 18px;
    font-family: 'Segoe UI', Arial, sans-serif;
    padding-bottom: 52px;
    box-sizing: border-box;
  }

  h1 {
    color: var(--color-primary);
    border-bottom: 3px solid var(--color-accent);
    padding-bottom: 6px;
    font-size: 1.85em;
    margin-bottom: 0.35em;
  }

  h2 {
    color: var(--color-secondary);
    font-size: 1.25em;
    margin-top: 0.2em;
  }

  strong {
    color: var(--color-primary);
  }

  code {
    background: var(--color-light);
    color: #0d2a4a;
    border-radius: 3px;
    padding: 0 3px;
  }

  pre {
    background: var(--color-light);
    border-left: 4px solid var(--color-accent);
    font-size: 1em;
    overflow: hidden;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.95em;
  }

  th {
    background: var(--color-primary);
    color: #ffffff;
    padding: 5px 8px;
  }

  td {
    border: 1px solid var(--color-light);
    padding: 4px 8px;
  }

  tr:nth-child(even) td {
    background: var(--color-light);
  }

  footer {
    background: transparent;
    color: #7a9ab8;
    font-size: 0.75em;
    padding: 6px 18px;
    height: 36px;
    display: flex;
    align-items: center;
  }

  section::after {
    color: var(--color-secondary);
    font-size: 1em;
  }

  ul, ol {
    margin-top: 0.3em;
    margin-bottom: 0.3em;
  }

  section.extra-slide {
    background: #1e88e5;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding-bottom: 0;
  }

  section.extra-slide h1 {
    color: #ffffff;
    border-bottom: none;
    margin: 0;
    padding-bottom: 0;
    font-size: 6em;
    line-height: 1;
  }

  section.flow-slide {
    padding-top: 44px;
  }

  section.flow-slide h1 {
    font-size: 1.35em;
    margin-bottom: 0.2em;
  }

  section.flow-slide p {
    margin: 0.15em 0 0;
  }

  section.flow-slide img {
    display: block;
    width: 100%;
    max-width: 100%;
    max-height: 70vh;
    height: auto;
    margin: 0 auto;
    object-fit: contain;
  }

  
  section.video-slide {
    padding-top: 44px;
  }

  section.video-slide h1 {
    font-size: 1.35em;
    margin-bottom: 0.25em;
  }

  section.video-slide video {
    display: block;
    width: 100%;
    max-width: 100%;
    max-height: 70vh;
    height: auto;
    margin: 0 auto;
    border-radius: 10px;
    background: #000000;
  }
---

<!--
Durata target: 18-20 minuti.
Formato: 16 slide, circa 60-75 secondi per slide.
Pubblico: tecnico, ma non necessariamente esperto di AI o agentic coding.
Obiettivo narrativo: spiegare cosa abbiamo costruito, perché funziona, come viene usato dai modelli e quali possibilità apre.
-->

# Stack AI operativo per QA e agentic coding

## Un sistema governato di agenti, policy e handoff - Daniele Quero
<br><br><br>

**pagopa-platform-integration-test**
*AI-enhanced presentation deck* 

<!--
Speaker note (1:00): Aprire con il messaggio principale: non stiamo presentando un singolo prompt, ma uno stack operativo. Lo stack consente a un modello di lavorare dentro regole, ruoli e processi verificabili.
-->

---

# Obiettivo della presentazione

1. Esplorare le risorse AI introdotte nel repository
2. Chiarire come prompt, agenti e instruction cooperano
3. Comprendere dettagli tecnici
4. Sintetizzare il lavoro che ha portato al risultato
5. Mostrare potenzialità, limiti e prossimi passi

<!--
Speaker note (0:50): Impostare le aspettative: sarà una lettura tecnica, ma guidata. I dettagli servono per rendere il sistema comprensibile e mantenibile, non per fare teoria astratta sui modelli.
-->

---

# A cosa serve uno stack AI

Molte attività sono *ripetitive*, *noiose* e *prone a errori*. L'AI può aiutare a concentrarci sull'aspetto `creativo` del lavoro.

Nel repository convivono test API, integrazione ed end-to-end. I flussi QA richiedono:

- analisi di requisiti e scenari Gherkin
- implementazione di step (Python)
- esecuzione Behave e diagnosi dei failure
- reportistica Allure
- commit e pull request coerenti con policy di progetto

```markdown
Utente
  |
1. .github/prompts       comandi riusabili: /qa, /commit, /pr, /promptize
  |
2. .github/agents        ruoli operativi: Analyst, Engineer, Runner, Closer
  |
3. .github/instructions  policy applicate per tipo file o workflow
```
## Senza governance, un agente AI tende a essere utile ma **imprevedibile**.

<!--
Speaker note (1:05): Collegare al contesto reale del repo: Behave, Gherkin, Python, Allure, workflow GitHub Actions. Il problema non è solo generare codice: è coordinare responsabilità, scope, test, report e chiusura.
-->

---


# Livello 1: prompt riusabili

I file `.prompt.md` trasformano richieste ricorrenti in comandi stabili.

Esempi:

- `qa.prompt.md`: avvia il processo QA iterativo
- `commit.prompt.md`: crea commit conformi alle linee guida
- `pr.prompt.md`: crea PR con template e metadati corretti
- `promptize.prompt.md`: trasforma una richiesta libera in istruzioni operative

<br>

## Il **valore**: l'utente non deve ricordare ogni dettaglio procedurale da digitare in chat.

<!--
Speaker note (1:00): Spiegare che un prompt file è come un comando di alto livello. Non sostituisce il processo: lo incapsula e lo rende ripetibile.
-->

---

# Com'è fatto un prompt file

## `/qa`
```yaml
---
#Front matter (yml)
description: 'Iterative quality assurance process using the QA Loop'
agent: "QA-orchestrator"
argument-hint: "Task ID, suite name, and objective"
---
```
```markdown
<!-- Prompt (md)-->
If no text prompt is provided with the `/qa` command,
use the chat context to determine the implicit request.

${input:Describe the QA task or process to execute}
```

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">

<div>

**Il prompt contiene:**
• metadati per VS Code/Copilot (`front matter`)
• istruzioni testuali per il modello
• placeholder per input utente

</div>

<div>

**Il front matter serve a dichiarare:**
• quale `modello` preferire
• quali `tool` sono consentiti
• quali `agenti` possono essere coinvolti
• se sono previsti `handoffs` verso altri agenti

</div>

</div>

<!--
Speaker note (1:15): Qui introdurre il concetto di file Markdown eseguibile dal punto di vista operativo: non è codice, ma diventa contesto strutturato che il modello riceve quando il prompt viene invocato.
-->

---

# Livello 2: agenti come ruoli

Un **agente** è un sistema in cui un LLM non risponde solo una volta, ma **opera in un ciclo** fino a completare un obiettivo. L'agente può:
  - Pianificare
  - Usare tool
  - Osservare risultati
  - Adattare il piano
  - Ripetere fino al completamento
  
<center>Ogni <code>.agent.md</code> definisce una responsabilità specifica.</center>

<div style="display:flex;gap:24px;align-items:flex-start;margin-top:0.4em;">
<div style="flex:27;">
Un agente combina tre parti:<br>
• <strong>Front matter</strong> (yaml)<br>
• <strong>Workflow</strong> (md): passi <code>da seguire</code><br>
• <strong>Constraints</strong> (md): cosa <code>non fare</code>
</div>
<div style="flex:28;background:#e3f2fd;border-left:4px solid #1565c0;border-radius:6px;padding:14px 16px;font-size:0.9em;">
<strong>Il modello non deve "fare tutto"</strong>, ma interpretare uno specifico ruolo.<br>
Indicazioni generiche portano a:<br>
• <strong>modifiche fuori scope</strong><br>
• <strong>perdita di contesto</strong><br>
• <strong>scarsa precisione</strong><br>
<br>
Definire ruoli senza overlap riduce side effect e aumenta ripetibilità.
</div>
<div style="flex:45;">

<table>
<thead><tr><th>Agente</th><th>Responsabilità principale</th></tr></thead>
<tbody>
<tr><td><code>QA-orchestrator</code></td><td>coordina il ciclo end-to-end</td></tr>
<tr><td><code>QA-analyst</code></td><td>produce o rivede feature Gherkin</td></tr>
<tr><td><code>QA-engineer</code></td><td>implementa step Python</td></tr>
<tr><td><code>QA-runner</code></td><td>esegue test e diagnostica failure</td></tr>
<tr><td><code>QA-closer</code></td><td>aggiorna docs, commit, push e PR</td></tr>
</tbody>
</table>
</div>
</div>

<!--
Speaker note (1:10): Evidenziare la separazione dei ruoli. Questo riduce side effect: il runner non modifica codice, l'analyst non scrive Python, il closer non cambia feature.
-->


---


# Handoff: passare lavoro tra agenti

Un handoff è un passaggio controllato da un agente a un altro.

## `from QA-analyst.agent.md`
```yaml
handoffs:
  - label: Implement step definitions
    agent: QA-engineer
    prompt: "Implement the Python step definitions..."
    send: false
```

Ne esistono due modalità:

- **invisibile**: orchestratore delega a sub-agent senza intervento utente
    ```text
    esplicitamente indicato nel suo workflow o desunto dall'analisi del contesto.
    ```
- **visibile**: agente propone un passaggio può avverarsi tramite intervento umano o in automatico (vedi `send: false/true`)
    ```text
    definendo la property handoff.
    ```

L'**handoff** conserva contesto e responsabilità, evitando passaggi informali.

<!--
Speaker note (1:20): Spiegare bene send: false: l'agente prepara un'azione suggerita, ma non la invia automaticamente. Nel percorso orchestrato invece la delega può essere interna e non richiede click.
-->

---
# Livello 3: instruction come policy

Gli `.instructions.md` sono regole applicate per scope.
Nel *front matter* si dichiara `applyTo: <pattern>` per indicare a quali file o percorsi si applicano, ma *non è obbligatorio.*

Alcuni esempi:

- `python-scripts.instructions.md` si applica a `**/*.py`  - **istruzioni generali per script Python**
- `behave-steps.instructions.md` si applica a `src/**/steps/**/*.py` - **istruzioni per step Python di Behave**
- `gherkin.instructions.md` si applica a `src/**/*.feature` - **linee guida per file Gherkin**
- `git-pr.instructions.md` governa PR - **istruzioni per PR coerenti con le policy di progetto**

<br>

## Le regole diventano una memoria operativa condivisa e versionata. 

Più pulite e specifiche rispetto a istruzioni di sistema:

<div style="display:flex;gap:24px;align-items:flex-start;margin-top:0.4em;">
<div style="flex:1;">
<div style="background:#e8f5e9;border-left:4px solid #2e7d32;border-radius:6px;padding:12px 16px;font-size:0.88em;">
Gli <code>.instructions.md</code> valgono per i <strong>pattern</strong> indicati o per i <strong>workflow</strong> che ne sepecificano la <strong>necessità</strong>.
</div>
</div>
<div style="flex:1;">
<div style="background:#fce4ec;border-left:4px solid #c62828;border-radius:6px;padding:12px 16px;font-size:0.88em;">
I file <code>AGENTS.md</code> e <code>INSTRUCTIONS.md</code> valgono per <strong>tutti</strong> gli agenti, sia che ne abbiano bisogno esplicitamente o meno.
</div>
</div>
</div>

<!--
Speaker note (1:15): Chiarire applyTo: è una regola di scope. Quando un agente lavora su un file che matcha quel pattern, deve caricare quelle istruzioni e seguirle.
-->


---

# Ciclo QA agentico

```text
Input utente
  |
QA-orchestrator
  ├─► QA-analyst (subagent)  -> feature Gherkin e spiegazione scenari
  ├─► QA-engineer (subagent) -> step definitions Python
  ├─► QA-runner (subagent)   -> esecuzione, diagnosi, fix loop
  └─► QA-closer (subagent)   -> README, failure report, commit, PR 
```

Il ciclo esplicita chi decide, chi implementa, chi verifica e chi chiude.

## Esempio realistico: nuova suite QA

1. L'utente invia task ID, suite e obiettivo tramite `/qa`
2. `QA-orchestrator` verifica branch e condivide un piano
3. `QA-analyst` crea o valida le `.feature`
4. `QA-engineer` implementa gli step seguendo instruction Python e Behave
5. `QA-runner` esegue Behave con Allure/JUnit e analizza l'esito
6. Se <span style="font-weight:bold;font-style:italic;color:#00cc00">verde</span>, `QA-closer` aggiorna documentazione e apre PR se previsto

<!--
Speaker note (1:05): Legare al valore pratico: il flusso riproduce un team QA reale. L'orchestratore non fa tutto; coordina competenze specializzate.
-->

---

# Il lavoro che ha portato al risultato

Dal prompt... 
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...**allo stack**.

È stato necessario:

- mappare le convenzioni esistenti
- separare responsabilità tra ruoli QA
- trasformare pratiche implicite in instruction versionate
- ricavare prompt riusabili per task frequenti
- documentare handoff e condizioni di stop
- allineare agenti, prompt, instruction, README e `AGENTS.md`

<br>

## In pratica: codificare il modo in cui il team lavora.

<!--
Speaker note (1:15): Far emergere la parte di engineering. La qualità dello stack dipende da analisi del processo, non da un prompt brillante scritto una volta.
-->

---

# Potenzialità e Criticità
<br><br>
<div style="display:flex;gap:24px;align-items:flex-start;margin-top:0.4em;">
<div style="flex:1;">
<div style="background:#e8f5e9;border-left:4px solid #2e7d32;border-radius:6px;padding:12px 16px;font-size:0.88em;">
<strong style="color:#2e7d32;">✦ Potenzialità</strong><br><br>
Lo stack abilita:<br>
• <strong>onboarding</strong> più rapido su convenzioni QA<br>
• automazione di attività <strong>ripetitive</strong>, <strong>noiose</strong>, <strong>prone a errori</strong><br>
• riduzione di <strong>errori</strong> su commit, PR, run test e report<br>
• <strong>miglioramento incrementale</strong> successivo: nuove instruction, agenti, prompt<br>
• <strong>tracciabilità</strong>: gli asset AI sono versionati accanto al codice<br><br>
<em>Meno variabilità, meno conoscenza tribale, più ripetibilità.</em>
</div>
</div>
<div style="flex:1;">
<div style="background:#fce4ec;border-left:4px solid #c62828;border-radius:6px;padding:12px 16px;font-size:0.88em;">
<strong style="color:#c62828;">⚠ Criticità</strong><br><br>
Lo stack richiede <strong>manutenzione</strong>:<br>
• <strong>instruction duplicate</strong> o divergenti → conflitti<br>
• <strong>front matter errato</strong> → agente non performa come atteso<br>
• <strong>handoff troppo generici</strong> → output di bassa qualità<br>
• <strong>agenti troppo permissivi</strong> → modifiche fuori scope<br>
• <strong>comandi e path</strong> devono restare allineati al repo<br><br><br>
<em>Governare l'AI significa mantenere al meglio il suo contesto.</em>
</div>
</div>
</div>

<!--
Speaker note (1:05): Bilanciare potenziale e limiti. Il messaggio pratico: meno variabilità, meno conoscenza tribale, più ripetibilità. Ma il sistema richiede manutenzione: instruction obsolete, path errati o agenti troppo permissivi portano a decisioni sbagliate. Il contesto dell'AI va curato come il codice.
-->

---

# Prossimi passi consigliati
```text
 Obiettivo: far crescere lo stack come prodotto interno, non come esperimento isolato.
 ```
 <br>
 <div style="display:flex;gap:24px;align-items:flex-start;margin-top:0.4em;">
<div style="flex:1;">
<div style="background:#e1f5fe;border-left:4px solid #0277bd;border-radius:6px;padding:12px 16px;font-size:0.88em;">
<strong style="color:#0277bd;">⏰ Breve termine:</strong><br><br>
<ol>
<li>Ampliare lo stack con altri ruoli/istruzioni utili</li>
<li>Misurare metriche semplici: tempi di completamento, failure ricorrenti, fix loop, costo in crediti</li>
</ol>
</div>
</div>
<div style="flex:1;">
<div style="background: #0b0069;border-left:4px solid #0277bd;border-radius:6px;padding:12px 16px;font-size:0.88em;">
<strong style="color: #83d6f0;">⏰⏰ Medio termine:</strong><br><br>
<ol>
<li style="color:white;"><strong style="color:#83d6f0;">Introdurre AI</strong> nelle logiche di test e diagnostica (es. analizzare report NRT)</li>
<li style="color:white;">Migrare stack su server <strong style="color:#83d6f0;">MCP</strong> generale e configurabile
</li>
</ol>
</div>
</div>
</div>

<!--
Speaker note (1:00): Chiudere con una prospettiva realistica. Il sistema è già utile, ma diventa più forte se misurato, curato e integrato nel modo di lavorare quotidiano.
-->
---

<!-- _class: extra-slide -->
<!-- _footer: "" -->
<!-- _paginate: false -->

# EXTRA

<!--
Speaker note (0:10): Slide separatoria per passare all'appendice tecnica dei flussi.
-->
---

<!-- _class: video-slide -->

# Demo /promptize

<video controls preload="metadata" style="width:100%;max-height:70vh;border-radius:10px;">
  <source src="../docs/videos/promptize_test.mp4" type="video/mp4" />
  Il browser non supporta la riproduzione video integrata.
</video>

<!--
Speaker note (0:45): Mostrare una breve demo del flusso agentico. Se necessario, aggiornare il path del file video in base alla posizione reale dell'asset.
-->
---

<!-- _class: video-slide -->

# Demo /qa test case completo

<video controls preload="metadata" style="width:100%;max-height:70vh;border-radius:10px;">
  <source src="../docs/videos/qa_dry_api_test.mp4" type="video/mp4" />
  Il browser non supporta la riproduzione video integrata.
</video>

<!--
Speaker note (0:45): Mostrare una breve demo del flusso agentico. Se necessario, aggiornare il path del file video in base alla posizione reale dell'asset.
-->
---

<!-- _class: video-slide -->

# Demo QA-analyst -> handodff -> QA-engineer

<video controls preload="metadata" style="width:100%;max-height:70vh;border-radius:10px;">
  <source src="../docs/videos/test2_analyst_handoff_engineer.mp4" type="video/mp4" />
  Il browser non supporta la riproduzione video integrata.
</video>

<!--
Speaker note (0:45): Mostrare una breve demo del flusso agentico. Se necessario, aggiornare il path del file video in base alla posizione reale dell'asset.
-->

---

# Esempio di front matter

Il front matter è un blocco YAML all'inizio del file Markdown.

## `from Python-utility-engineer.agent.md`
```yaml
---
description: "Use when: Python step definitions need to be implemented"
model: "GPT-5.3-Codex"
tools: [read/readFile, edit/createFile, edit/editFiles]
agents: [Python-utility-engineer]
user-invocable: true
---
```

Serve a dichiarare dati che non sono contenuto narrativo:

- quando usare un asset
- quale modello preferire
- quali tool sono consentiti
- quali agenti possono essere coinvolti
- se sono previsti handoffs verso altri agenti

<!--
Speaker note (1:20): Rendere chiaro che il front matter è metadata, non slide/testo normale. I sistemi agentici lo leggono per configurare il comportamento: routing, modello, tool e invocabilità.
-->

---

# Fix Loop del QA-runner


Workflow del `QA-runner`:

Handoff da QA-orchestrator
  ├─► scopre le istruzioni di run 
  ├─► mostra il comando e chiede conferma
  ├─► esegue i test
  └─►   in caso di failure avvia un fix loop massimo di **5 iterazioni**

```text
  •  delegando le modifiche al QA-engineer
  •  verificando ad ogni iterazione se la fix ha risolto il problema
  •  cedendo il testimone all'utente se il fix loop non risolve il problema (entro 5 iterazioni)
``` 

<!--
Speaker note (1:05): Spiegare che gli agenti sono contratti operativi. Il modello riceve un perimetro: strumenti ammessi, responsabilità, stop condition e forma dell'output.
-->

---

<!-- _class: extra-slide -->
<!-- _footer: "" -->
<!-- _paginate: false -->

# FLOWCHARTS

<!--
Speaker note (0:10): Slide separatoria per passare all'appendice tecnica dei flussi.
-->

---

<!-- _class: flow-slide -->

# Appendice Flussi: QA Orchestrator

![](../docs/flows/images/agent-qa-orchestrator.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: QA Analyst

![](../docs/flows/images/agent-qa-analyst.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: QA Engineer

![](../docs/flows/images/agent-qa-engineer.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: QA Runner

![](../docs/flows/images/agent-qa-runner.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: QA Closer

![](../docs/flows/images/agent-qa-closer.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Python Utility Engineer

![](../docs/flows/images/agent-python-utility-engineer.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Prompt `/qa`

![](../docs/flows/images/prompt-qa.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Prompt `/commit`

![](../docs/flows/images/prompt-commit.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Prompt `/pr`

![](../docs/flows/images/prompt-pr.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Prompt `/promptize`

![](../docs/flows/images/prompt-promptize.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Prompt `/sync-folder`

![](../docs/flows/images/prompt-sync-folder.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Instruction Gherkin

![](../docs/flows/images/instruction-gherkin.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Instruction Behave Steps

![](../docs/flows/images/instruction-behave-steps.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Instruction Python Scripts

![](../docs/flows/images/instruction-python-scripts.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Instruction Run Tests

![](../docs/flows/images/instruction-run-tests.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Instruction Git Commit

![](../docs/flows/images/instruction-git-commit.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Instruction Git PR

![](../docs/flows/images/instruction-git-pr.svg)

---

<!-- _class: extra-slide -->
<!-- _footer: "" -->
<!-- _paginate: false -->

# STACK MERMAID-FLOW

<!--
Speaker note (0:10): Separatore introduttivo per il nuovo stack prompt/agent/skill dedicato ai flow Mermaid.
-->

---

# Nuovo stack: `mermaid-flow`

## Obiettivo
Generare in modo ripetibile i **flow diagram Mermaid** degli asset del repo, con Markdown sempre prodotto e SVG opzionale.

## Tre asset, tre responsabilita

- **Skill** `.github/skills/mermaid-flow/SKILL.md`: regole tecniche (naming, output, prerequisiti, rendering, definition of done).
- **Agente** `Mermaid-flow-engineer`: applica la skill con i propri tool, gestisce installazioni e domande all'utente.
- **Prompt** `/mermaid-flow`: punto di ingresso utente, delega all'agente con argomenti opzionali (sorgenti, orientation, svg).

## Output garantito

- `docs/flows/<basename>.md` sempre.
- `docs/flows/images/<basename>.svg` solo se richiesto.

<!--
Speaker note (1:00): Sottolineare la separazione di responsabilita: la skill descrive il "come", l'agente esegue, il prompt e' la porta d'ingresso utente.
-->

---

<!-- _class: flow-slide -->

# Appendice Flussi: Skill `mermaid-flow`

![](../docs/flows/images/skill-mermaid-flow.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Agente `Mermaid-flow-engineer`

![](../docs/flows/images/agent-mermaid-flow-engineer.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Prompt `/mermaid-flow`

![](../docs/flows/images/prompt-mermaid-flow.svg)

---

<!-- _class: extra-slide -->
<!-- _footer: "" -->
<!-- _paginate: false -->

# STACK MARP-PRESENTATION

<!--
Speaker note (0:10): Separatore introduttivo per lo stack prompt/agent/skill dedicato al meta-autoring di deck Marp.
-->

---

# Nuovo stack: `marp-presentation`

## Obiettivo

Generare deck Marp coerenti partendo da un brief utente: stile grafico, tono comunicativo, palette colore.

## Tre asset, tre responsabilita

- **Skill** `.github/skills/marp-presentation/SKILL.md`: tooling (Marp VS Code, Marp CLI), interview, regole di cromoarmonia, layout, definition of done.
- **Agente** `Marp-presentation-engineer`: verifica/installa l'estensione, conduce l'interview, normalizza la palette, scrive il deck.
- **Prompt** `/marp-presentation`: punto di ingresso utente con argomenti opzionali (topic, audience, durata, stile, tono, colori).

## Input flessibile su colori

- Hex (`#1565c0`), nomi umani ("blu pagoPA", "petrolio"), oppure misto.
- Fino a 5 ruoli (`primary`, `secondary`, `accent`, `light`, `bg`); i mancanti vengono dedotti per cromoarmonia (HSL + WCAG AA).

<!--
Speaker note (1:00): Sottolineare che lo stack non genera un deck "a caso": l'interview e' obbligatoria solo dove il brief manca, e la palette e' sempre completata in modo deterministico.
-->

---

<!-- _class: flow-slide -->

# Appendice Flussi: Skill `marp-presentation`

![](../docs/flows/images/skill-marp-presentation.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Agente `Marp-presentation-engineer`

![](../docs/flows/images/agent-marp-presentation-engineer.svg)

---

<!-- _class: flow-slide -->

# Appendice Flussi: Prompt `/marp-presentation`

![](../docs/flows/images/prompt-marp-presentation.svg)

