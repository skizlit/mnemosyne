# Contributing

## Working rules

- Keep each change small enough to map to one GitHub issue.
- Use `snake_case` for Python modules, functions, variables, and filesystem identifiers.
- Add or update tests with every behavioural change.
- Mirror the source layout under `tests/` as the package grows.
- Add useful structured logging at system boundaries; never log secrets or private memory text.
- Use synthetic data in tests and examples.
- Record architectural changes as numbered decisions under `docs/decisions/`.
- Prefer the smallest implementation that satisfies the acceptance criteria.

## Before committing

```bash
gitleaks git --config .gitleaks.toml --redact
python tools/check_repository_safety.py
ruff check .
pytest
```

See [`docs/repository_safety_checks.md`](docs/repository_safety_checks.md) for installation,
allow-list, and remediation guidance.

Commit messages should be imperative and describe one completed change.
