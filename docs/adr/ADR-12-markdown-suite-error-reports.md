# ADR-12: Produce only Markdown suite-error closure reports

- Status: Accepted
- Date: 2026-10-22

## Context

The closer wrapper promised HTML reports without a matching procedure, and
report creation was not limited to actual errors in test-suite work.

## Decision

Apply the [error-only report policy](../workflows/qa-closer/closure.md#error-only-markdown-reporting-adr-12).
Create or reuse a local Markdown report only for unresolved suite errors.
Reuse the runner's report; allow report-only closure without publication.
Do not read Confluence reporting templates or generate/serve HTML.

## Consequences

Successful work, non-suite changes and Git/tool failures alone produce no suite
report. Return errors and actual state in chat regardless. GitHub PR templates
remain required for PR bodies; existing Allure/CI workflows are unchanged.
