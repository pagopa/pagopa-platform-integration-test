#!/usr/bin/env node
'use strict';

// Agent-scoped preToolUse hook: allows delegation only to the agents passed as
// arguments. Copilot equivalent of the Local-only `agents:` frontmatter field.
// Usage: node .github/hooks/scripts/delegation-allowlist.js <agent> [<agent> ...]

const DELEGATION_TOOLS = new Set(['task', 'agent', 'runsubagent', 'agent/runsubagent']);
const AGENT_FIELDS = ['agent_type', 'agentType', 'subagent_type', 'agentName', 'agent_name', 'agent'];

function normalize(name) {
  return String(name).trim().toLowerCase();
}

function decide(payload, allowed) {
  const toolName = payload.toolName ?? payload.tool_name;
  if (!toolName || !DELEGATION_TOOLS.has(normalize(toolName))) return {};

  let args = payload.toolArgs ?? payload.tool_input ?? {};
  if (typeof args === 'string') {
    try {
      args = JSON.parse(args);
    } catch {
      args = {};
    }
  }
  const field = AGENT_FIELDS.find((key) => typeof args?.[key] === 'string' && args[key].trim());
  const target = field ? args[field] : null;
  const list = allowed.join(', ');

  if (!target) {
    return {
      permissionDecision: 'deny',
      permissionDecisionReason: `Delegation target not identifiable. Allowed agents: ${list}.`,
    };
  }
  if (allowed.some((name) => normalize(name) === normalize(target))) {
    return {};
  }
  return {
    permissionDecision: 'deny',
    permissionDecisionReason: `Delegation to "${target}" is not allowed for this agent. Use one of: ${list} (by name, not by generated id).`,
  };
}

function main() {
  const allowed = process.argv.slice(2).filter((name) => name.trim());
  let raw = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (chunk) => { raw += chunk; });
  process.stdin.on('end', () => {
    // Exceptions exit nonzero, which denies the call: command preToolUse hooks fail closed.
    const payload = raw.trim() ? JSON.parse(raw) : {};
    process.stdout.write(JSON.stringify(decide(payload, allowed)));
  });
}

if (require.main === module) main();

module.exports = { decide };
