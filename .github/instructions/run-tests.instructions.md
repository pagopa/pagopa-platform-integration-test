---
# Catalog metadata anchors (do not edit manually)
source: pagopa-platform-mcp
source_version: 1.1.0
source_digest: sha256:d958428eca45dfbd6437d900c665769a71f525dcfc7a332ef2a9f08705e44f87
source_id: run-tests-guidelines
---

# Running Tests

## Run an API suite

Placeholders: `<suite>` = `cart` | `auth-service` | `checkout-npg` | `ecommerce-cdc` — `<env>` = `dev` | `uat`

```powershell
$env:TARGET_ENV = "<env>"
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "reports\allure-results\<suite>-<env>"
New-Item "reports\allure-results\<suite>-<env>" -ItemType Directory -Force | Out-Null
behave src\api\<suite> `
    -f allure_behave.formatter:AllureFormatter -o reports\allure-results\<suite>-<env> `
    -f progress --summary --show-timings
```

## Run integration tests in UAT

```powershell
$env:TARGET_ENV="uat"
$env:suite="wisp"
behave src/bdd/wisp --tags=@runnable `
    --format allure_behave.formatter:AllureFormatter -o allure-results `
    --junit-directory=junit --junit --summary --show-timings -v
```

## View the Allure report

Use **absolute paths** — the integrated terminal may start from a parent folder and relative paths can resolve incorrectly.

```powershell
# <port> = any free port, e.g. 5300
allure serve "\reports\allure-results\<suite>-<env>" --port <port>
```

## Validation rules

- All scenarios must pass (0 failures) before the task is considered done, unless otherwise specified.
- On certificate errors: keep `http_client.py` in place, diagnose the OS trust store — do **not** set `verify=False`.
- <Test rule>
