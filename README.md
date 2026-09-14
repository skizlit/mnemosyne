# Project Void: Mnemosyne

Mnemosyne is a clean-sheet, local-first memory system. Its job is to turn information into durable
knowledge that can be inspected by a human, recalled in a later session, and corrected without
leaving conflicting active memories behind.

It is not a rewrite, migration, or extension of Second Brain.

## v0.1 goal

Prove one useful memory loop:

1. Capture a piece of knowledge.
2. Close and reopen the application.
3. Retrieve and apply that knowledge in a later session.
4. Correct the knowledge.
5. Retrieve the corrected version without returning the old version as current truth.
6. Inspect and edit the same knowledge as ordinary Markdown in Obsidian.

See [the v0.1 proof](docs/v0.1_proof.md) for the acceptance scenario.

## Architecture direction

- **Markdown vault:** permanent, human-readable source of truth.
- **Obsidian:** human interface for viewing, editing, navigating, and linking the Markdown.
- **Python:** capture, consolidation, correction, and retrieval.
- **Optional indexes:** SQLite, embeddings, vectors, or graphs may be evaluated later only as
  disposable accelerators that can be rebuilt from Markdown.

The exact vault structure and document schema have not been chosen yet. They will be settled
through small, testable tasks rather than inherited from the old system.

## Not part of v0.1

- Inventorying or migrating Second Brain.
- A complete agent harness.
- ChatGPT, Agent Team, or other external integrations.
- A Jarvis-style interface or voice control.
- A database as the authoritative memory.
- Paid models or paid cloud storage.

## Repository layout

```text
docs/                 Goal, architecture, and accepted decisions
src/mnemosyne/        Python package
tests/                Tests mirroring the source structure
.github/workflows/    Repository checks
```

Real memory vaults, generated indexes, logs, and secrets must never be committed to this
repository. Tests and examples use synthetic data only.

## Development

Mnemosyne currently requires Python 3.12 or newer.

```bash
python -m venv .venv
python -m pip install -e '.[dev]'
ruff check .
pytest
```
