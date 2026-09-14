# 0004: Prove file-based recall before adding indexes

- Status: Accepted
- Date: 2026-09-14

## Decision

The first working slice uses Markdown files without SQLite, embeddings, a vector store, or a
knowledge graph.

## Reason

The project should prove that it can remember, recall, and correct knowledge before adding
retrieval infrastructure. This gives later indexing decisions a real baseline instead of an
assumption.

## Consequence

The v0.1 proof may use simple file and metadata search. Optional retrieval technologies will be
benchmarked later and added only if the benefit justifies the complexity.
