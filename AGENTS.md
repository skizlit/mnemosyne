# Mnemosyne contributor instructions

## Read before changing the repository

1. Read Jonathan's shared `master_rules.md`.
2. Read `local_rules.md`, `CONTRIBUTING.md`, and `SECURITY.md`.
3. Confirm the GitHub issue and create a branch from the intended base before editing.

If the shared rulebook is unavailable, ask Jonathan for it before substantial work.

## Project boundary

Mnemosyne is the memory component of Project Void. Markdown is the durable source of truth.
Obsidian is an optional view and editor. Databases, embeddings, indexes, caches, logs, and other
runtime state are derived or local data and must remain replaceable and outside source control.

Never commit real memories, personal notes, vault contents, credentials, private configuration,
NAS details, or copied-and-anonymised personal data. Tests and examples must be wholly synthetic.

## Workflow

- Use one issue for each substantial unit of work.
- Name branches `<type>/<issue-number>-<short_snake_case_name>`.
- Start issue-related commit subjects with `[<issue-number>]`.
- Keep changes within the approved issue and stop at Jonathan's approval checkpoints.
- Open a pull request, run CI, address CodeRabbit findings, and wait for Jonathan's approval
  before merging.

## Verification

Install development dependencies with:

```bash
python -m pip install -e '.[dev]'
```

Run the smallest relevant test first, followed by:

```bash
ruff check .
pytest
```

Report skipped tests, missing dependencies, and unverified behaviour as limitations, not passes.
