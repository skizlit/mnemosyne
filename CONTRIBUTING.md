# Contributing

Read `AGENTS.md`, `local_rules.md`, and `SECURITY.md` before making changes. Jonathan's shared
`master_rules.md` remains the governing rulebook.

## Working rules

- Keep each change small enough to map to one GitHub issue.
- Create the correctly named issue branch before editing.
- Follow the Python and pytest naming rules in `local_rules.md`.
- Add or update tests with every behavioural change.
- Mirror the source layout under `tests/` where practical.
- Add useful structured logging at system boundaries; never log secrets or private memory text.
- Use wholly synthetic data in tests and examples.
- Record architectural changes as numbered decisions under `docs/decisions/`.
- Prefer the smallest implementation that satisfies the acceptance criteria.

## Before committing

Run the smallest relevant test, followed by:

```bash
ruff check .
pytest
```

Inspect the final diff for unrelated files, secrets, syntax errors, and formatting problems.
Issue-related commit subjects must start with `[<issue-number>]`.
