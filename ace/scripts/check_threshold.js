#!/usr/bin/env node
'use strict';

// Conteggio deterministico per decidere se una fase del ciclo ACE deve
// scatenare automaticamente la fase successiva (soglie in
// ace/config/thresholds.json, editabili senza toccare questo script).
// Non decide MAI da solo se invocare l'agente successivo: si limita a
// dire "raggiunta: true/false" — la decisione di invocare resta un passo
// esplicito nel prompt dell'agente chiamante (orchestratore/reflector/curator).
// Se il valore di soglia è < 1, la fase viene interpretata come "skip"
// nel routing automatico: il passaggio deve essere fatto solo a mano.
//
// Uso:
//   node ace/scripts/check_threshold.js reflector
//   node ace/scripts/check_threshold.js curator --file ace/proposals/<batch>.json
//   node ace/scripts/check_threshold.js warden   --file ace/proposals/<batch>-decisions.json
//
// Stampa un JSON su stdout: { stage, count, threshold, reached, skipped }.
// Exit code: 0 se reached oppure skipped, 1 se non reached, 2 su errore (argomenti/file).

const fs = require('fs');
const path = require('path');
const { REPO_ROOT, ACE_ROOT } = require('./lib/playbook');

const CONFIG_PATH = path.join(ACE_ROOT, 'config', 'thresholds.json');

function loadConfig() {
  return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
}

function countUnprocessedTraces() {
  const dir = path.join(REPO_ROOT, 'ace', 'traces');
  return fs.readdirSync(dir, { withFileTypes: true })
    .filter((e) => e.isFile() && e.name.endsWith('.json'))
    .length;
}

function countArrayInFile(filePath, arrayKey) {
  const abs = path.isAbsolute(filePath) ? filePath : path.join(REPO_ROOT, filePath);
  if (!fs.existsSync(abs)) {
    throw new Error(`File non trovato: ${filePath}`);
  }
  const doc = JSON.parse(fs.readFileSync(abs, 'utf8'));
  const arr = doc[arrayKey];
  if (!Array.isArray(arr)) {
    throw new Error(`Campo "${arrayKey}" assente o non è un array in ${filePath}`);
  }
  return arr.length;
}

function main() {
  const args = process.argv.slice(2);
  const stage = args[0];
  const fileFlagIdx = args.indexOf('--file');
  const filePath = fileFlagIdx !== -1 ? args[fileFlagIdx + 1] : null;

  if (!['reflector', 'curator', 'warden'].includes(stage)) {
    console.error('Uso: node ace/scripts/check_threshold.js <reflector|curator|warden> [--file <path>]');
    process.exit(2);
  }

  const config = loadConfig();
  const threshold = config[stage].threshold;
  const skipped = threshold < 1;

  let count;
  try {
    if (stage === 'reflector') {
      count = countUnprocessedTraces();
    } else if (stage === 'curator') {
      if (!filePath) throw new Error('--file obbligatorio per stage=curator (file di proposte del reflector)');
      count = countArrayInFile(filePath, 'proposals');
    } else {
      if (!filePath) throw new Error('--file obbligatorio per stage=warden (file di decisioni del curator)');
      count = countArrayInFile(filePath, 'decisions');
    }
  } catch (err) {
    console.error(`Errore: ${err.message}`);
    process.exit(2);
  }

  const reached = !skipped && count >= threshold;
  console.log(JSON.stringify({ stage, count, threshold, reached, skipped }));
  process.exit(skipped || reached ? 0 : 1);
}

main();
