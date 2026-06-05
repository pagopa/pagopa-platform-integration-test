# pagopa-platform-integration-test

## To install Playwright:
```bash
    pip install playwright
    pip install pytest-playwright
    playwright install-deps
    playwright install
```

## WISP integration suite

Suite di integrazione per `wisp`, con feature e step definiti in `src/integration/wisp/`.

### Run

```powershell
python -m behave src/integration/wisp --tags=@runnable -D env=uat -f allure_behave.formatter:AllureFormatter -o reports/allure-results/wisp-uat -f progress --summary --show-timings
```

### Files

- Feature: `src/integration/wisp/features/`
- Step definitions: `src/integration/wisp/steps/`