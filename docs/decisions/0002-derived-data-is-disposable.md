# 0002: Derived data is disposable

- Status: Accepted
- Date: 2026-09-14

## Decision

SQLite indexes, embeddings, vector stores, and relationship graphs are optional derived products.
They may be introduced only when they solve a measured retrieval problem, and they must be fully
rebuildable from the Markdown vault.

## Reason

A convenient search tool must not quietly become an irreplaceable second source of truth.

## Consequence

Mnemosyne first proves file-based persistence and retrieval. Any future index needs a deterministic
rebuild path and may be deleted without losing durable knowledge.
