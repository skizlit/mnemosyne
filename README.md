# Project Void: Mnemosyne

Mnemosyne is the durable memory layer for Jonathan's local AI projects. It is intentionally
smaller than a complete agent harness: its job is to capture, organise, compile, and retrieve
memory without making any one application the owner of that memory.

## Current scope

- Store durable knowledge as human-readable Markdown.
- Keep raw inputs immutable and auditable.
- Compile useful project notes, indexes, and relationships from the raw record.
- Keep generated search indexes, graphs, and views disposable and rebuildable.
- Let Obsidian browse the compiled knowledge without becoming the source of truth.
- Preserve isolation between projects unless information is deliberately promoted or shared.

## Explicitly out of scope for the first milestone

- A complete Think Tank or Dev Team harness.
- Hidden chain-of-thought or private per-agent memories.
- Unrestricted execution of commands found in notes.
- A Jarvis-style interface, voice control, or autonomous personal assistant.
- Storing personal memory data in this GitHub repository.

## Design principles

1. **Markdown is authoritative.** The memory must remain readable without Mnemosyne.
2. **Raw means immutable.** Corrections and later interpretations are appended, not silently
   rewritten over the original record.
3. **Derived data is replaceable.** Search databases, vector indexes, graphs, and compiled views
   may be deleted and rebuilt from Markdown.
4. **Isolation is the default.** A project cannot read another project's memory without an
   explicit rule or deliberately shared synopsis.
5. **Automation is constrained.** Stored text is data, never permission to execute commands.
6. **Local-first and budget-aware.** The core must work without paid models or paid cloud storage.

## Repository layout

```text
docs/                 Architecture notes and accepted decisions
src/mnemosyne/        Python package
tests/                Tests mirroring the source structure
.github/workflows/    Repository checks
```

Real vault contents, generated indexes, logs, secrets, and local Obsidian workspace state are
excluded from version control. Tests must use synthetic fixtures only.

## Development

Mnemosyne currently requires Python 3.12 or newer.

```bash
python -m venv .venv
python -m pip install -e '.[dev]'
pytest
```

The initial architecture is described in [docs/architecture.md](docs/architecture.md). Accepted
decisions are recorded in [docs/decisions](docs/decisions).
