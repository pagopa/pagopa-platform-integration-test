---
# No applyTo: loaded explicitly by Qa-runner only (see .github/agents/Qa-runner.agent.md)
---

# Running Tests

## Run an API suite

Placeholders: `<suite>` = `cart` | `auth-service` | `checkout-npg` | `ecommerce-cdc` — `<env>` = `dev` | `uat`

```powershell
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "reports\allure-results\<suite>-<env>"
New-Item "reports\allure-results\<suite>-<env>" -ItemType Directory -Force | Out-Null
behave src\api\<suite> -D env=<env> `
    -f allure_behave.formatter:AllureFormatter -o reports\allure-results\<suite>-<env> `
    -f progress --summary --show-timings
```

## Run integration tests in UAT

```powershell
$env:TARGET_ENV="uat"
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
