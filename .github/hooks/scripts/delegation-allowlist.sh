#!/bin/sh
# POSIX launcher for delegation-allowlist.js. Without Node.js 18+ it denies only
# delegation calls with an explicit reason, instead of failing every tool call.
dir=$(dirname "$0")
raw=$(cat)

major=0
if command -v node >/dev/null 2>&1; then
  major=$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null)
fi
case $major in ''|*[!0-9]*) major=0 ;; esac

if [ "$major" -lt 18 ]; then
  compact=$(printf '%s' "$raw" | tr -d ' \t\r\n' | tr '[:upper:]' '[:lower:]')
  case $compact in
    *'"toolname":"task"'*|*'"toolname":"agent"'*|*'"toolname":"runsubagent"'*|*'"toolname":"agent/runsubagent"'*|\
    *'"tool_name":"task"'*|*'"tool_name":"agent"'*|*'"tool_name":"runsubagent"'*|*'"tool_name":"agent/runsubagent"'*)
      printf '%s' '{"permissionDecision":"deny","permissionDecisionReason":"Delegation blocked: the allowlist hook requires Node.js 18+ in PATH."}'
      ;;
    *)
      printf '{}'
      ;;
  esac
  exit 0
fi

printf '%s' "$raw" | node "$dir/delegation-allowlist.js" "$@"
