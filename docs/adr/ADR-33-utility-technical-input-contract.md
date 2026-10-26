# ADR-33: Verify utility contracts on delegated and direct requests

- Status: Accepted

## Decision

Before editing establish the [technical contract](../workflows/python-utility-engineer/implementation.md#technical-input-contract-adr-33):
purpose/consumers, input/output/error behaviour, edge cases, API, owned paths and
compatibility. Reuse known facts and ask only about material ambiguity, including
on direct invocation without a delegation packet.

## Consequences

Ordinary compatible implementation details need no needless approval. Missing
domain rules/oracles return to the caller/user; existing mechanics do not invent
requirements. No silent invalid-input defaults or success-shaped error suppression.
