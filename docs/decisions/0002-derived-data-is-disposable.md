# 0002: Derived data is disposable

- Status: Accepted
- Date: 2026-09-14

## Decision

Compiled views, search databases, embeddings, and relationship graphs are derived products. They
may be deleted and rebuilt from authoritative Markdown and the append-only audit history.

## Reason

This prevents a convenient retrieval tool from quietly becoming an irreplaceable second source
of truth.

## Consequence

Every derived format needs a deterministic rebuild path. A feature is incomplete if deleting its
derived state causes durable information to be lost.
