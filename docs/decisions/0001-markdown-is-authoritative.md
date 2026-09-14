# 0001: Markdown is the authoritative memory

- Status: Accepted
- Date: 2026-09-14

## Decision

Durable memory is stored as human-readable Markdown in a local vault. Obsidian and Python both
work with those canonical files.

A database may later accelerate retrieval, but it cannot become the sole source of truth.

## Reason

The memory must remain inspectable, editable, portable, and recoverable without a particular
application, model, or database engine.

## Consequence

Mnemosyne must safely recognise valid human edits. Every derived index must be reproducible from
the Markdown vault.
