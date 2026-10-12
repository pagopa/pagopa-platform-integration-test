#!/usr/bin/env node
'use strict';

const { captureTrace } = require('./lib/runtime');

function valueOf(name) {
  const index = process.argv.indexOf(name);
  return index === -1 ? undefined : process.argv[index + 1];
}

function run() {
  const manifestPath = valueOf('--manifest') || process.argv[2];
  const tracePath = valueOf('--trace') || process.argv[3];
  if (!manifestPath || !tracePath) {
    throw new Error('Usage: capture_trace.js --manifest <file> --trace <file>');
  }
  const result = captureTrace({ manifestPath, tracePath });
  console.log(`Captured trace: ${result.path}`);
  return result;
}

if (require.main === module) {
  try {
    run();
  } catch (error) {
    console.error(`ACE trace capture failed: ${error.message}`);
    process.exitCode = 1;
  }
}

module.exports = { run };
