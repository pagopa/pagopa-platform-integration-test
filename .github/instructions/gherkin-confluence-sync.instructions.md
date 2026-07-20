---
applyTo: "src/**/*.feature"
---

# Gherkin Confluence Synchronization Requirements

These instructions define the metadata required to keep `.feature` files aligned with the Confluence documentation. They apply to every feature file in the repository.

## File header

- First line **must** be a single line comment having a 10-digit number, e.g. `#3119448843`, when processing the file, if missing **ask the user to provide it**.
- Second line **must** be a single line comment having the language specification `#language:it`, if missing **add it**.
- Third line **must** be a tag to the `Feature` line, carrying the suite name in snake_case, followed by a progressive 3-digit number starting from 001, having scope in the suite (e.g. `@CUP_001`), each suite has its own numbering sequence.

## Given step (`Contesto`)

- In the Given step (`Contesto`), each line **must** start with `Dato`, `Data`, `Dati`, `Date` or `E`.

## Scenario tagging and linking

- Each `Scenario`:
  - **must** have a tag which is the same as the `Feature` tag, but with an ulterior progressive 2-digit number starting from 01, having scope in the feature file (e.g. `@CUP_001_05`).
  - **may** have a single line comment in the format `#link:{anchor}|{confluence_area_id}|{confluence_page_name}` to link the scenario to a specific use-case Confluence page, e.g. `#link:📜-Dettaglio-flusso-principale|IQCGJ|[CUP - 2027] UC-01: Creazione Posizione Debitoria` if missing **ask the user to provide it**, but it's optional, emoticons are allowed.

## Language enforcement

- Only italian Gherkin keywords are allowed, if any other language is used **fix it**.
