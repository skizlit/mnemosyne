# 0001: Markdown is the authoritative memory

- Status: Accepted
- Date: 2026-09-14

## Decision

Durable memory will be stored in human-readable Markdown files with explicit metadata and a clear
folder structure. A database may support search or retrieval, but it will not be the sole source
of truth.

## Reason

The memory should be inspectable, editable with ordinary tools, portable, easy to back up, and
recoverable without a particular application or database engine.

## Consequence

Schemas and write rules must be strict enough to keep a file-based store reliable. Any database,
vector index, or knowledge graph must be reproducible from the Markdown record.
