# Playbook globale — ACE

Sorgente di verità per i bullet condivisi da **tutti** gli agenti del
team, come definito in [ace/config/project.json](../ace/config/project.json)
(l'agente orchestratore in `orchestrator_agent` più i subagenti elencati in
`participating_agents`).

Il file di istruzioni globali di ciascuna piattaforma abilitata
(`global_instructions_file` in `ace/config/project.json`, es. `CLAUDE.md`
per Claude Code o `.github/copilot-instructions.md` per Copilot) viene
generato/sincronizzato a partire da questo file tramite
`ace/scripts/retrieval.js` — non va editato a mano in prod: qualunque
bullet reale nasce sempre da un batch reflector→curator→warden, mai da
un'edit diretta qui.

Il playbook parte vuoto: non c'è ancora nessun bullet reale, perché nessuna
trace è stata ancora processata da un batch reale.

<!--
Formato bullet (scritto da ace/scripts/apply_delta.js, non a mano):

## P-XXX — active|quarantined|deprecated — used:N helped:N hurt:N
Contenuto operativo della lezione, in forma imperativa, specifico
a questo progetto. Non ovvio per un professionista generico del dominio.

tags: [tag1, tag2]
counters: helped_confirmed=N; helped_provisional=N; hurt_confirmed=N; hurt_provisional=N
provenance: source_trace_ids=[...]; created_at=...; created_by=reflector+curator; batch_id=...

Tag, counters e provenance sono sempre presenti sui bullet reali (anche
tags: [] se non servono tag fini) — servono al retrieval e all'audit, non
vanno iniettati nel contesto dell'agente che lavora (solo id + content).
counters distingue evidenza confermata da provvisoria (vedi
ace/schema/bullet.schema.json, counters.helped_confirmed/helped_provisional/
hurt_confirmed/hurt_provisional) e guida le decisioni strutturali del
curator (DEPRECATE/PROMOTE/baking) — used/helped/hurt nell'intestazione
restano un aggregato storico retrocompatibile, non usato da solo per
quelle decisioni.
-->
