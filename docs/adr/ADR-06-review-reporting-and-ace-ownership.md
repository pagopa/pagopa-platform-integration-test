# ADR-06: Review protects features while allowing requested reports

- Status: Accepted
- Date: 2026-10-22

## Context

The review skill prohibited feature edits but permitted unspecified other file
creation, while persona permissions did not support a requested Markdown review.

## Decision

Follow [review reporting and ACE ownership](../workflows/qa-analyst/activity-routing.md#review-reports-and-ace-adr-06).
Review cannot create or modify any feature, including corrected copies. Allow
explicitly requested Markdown reports at human-confirmed paths, preserving
existing content and reporting write failures.

## Consequences

This is not permission to write arbitrary documents, UCs, code, skills,
instructions, UC stage artifacts or ACE files. The analyst returns trace elements;
the orchestrator remains responsible for capture and privacy finalization.
Reporting permissions neither block ACE nor add another trace writer.
