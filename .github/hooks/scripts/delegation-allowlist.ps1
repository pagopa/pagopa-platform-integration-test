# Windows launcher for delegation-allowlist.js. Without Node.js 18+ it denies only
# delegation calls with an explicit reason, instead of failing every tool call.
$ErrorActionPreference = 'Stop'
$OutputEncoding = [Text.UTF8Encoding]::new($false)
$raw = [Console]::In.ReadToEnd()

$node = Get-Command node -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
$major = 0
if ($node) {
    $version = & $node.Source --version 2>$null
    if ($version -match '^v(\d+)\.') { $major = [int]$Matches[1] }
}

if ($major -lt 18) {
    $payload = if ($raw.Trim()) { $raw | ConvertFrom-Json } else { $null }
    $tool = if ($payload.toolName) { $payload.toolName } else { $payload.tool_name }
    if ($tool -and @('task', 'agent', 'runsubagent', 'agent/runsubagent') -contains $tool) {
        @{
            permissionDecision       = 'deny'
            permissionDecisionReason = 'Delegation blocked: the allowlist hook requires Node.js 18+ in PATH.'
        } | ConvertTo-Json -Compress
    } else {
        '{}'
    }
    exit 0
}

$raw | & $node.Source (Join-Path $PSScriptRoot 'delegation-allowlist.js') @args
exit $LASTEXITCODE
