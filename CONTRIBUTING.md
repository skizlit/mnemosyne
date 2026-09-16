# Contributing

Read `AGENTS.md`, `local_rules.md`, and `SECURITY.md` before making changes. Jonathan's shared
`master_rules.md` remains the governing rulebook.

## Working rules

- Keep each change small enough to map to one GitHub issue.
- Start only from an approved issue with a clear goal, scope, and acceptance criteria.
- Create the correctly named issue branch from the intended base before editing. Use
  `<type>/<issue-number>-<short_snake_case_name>`.
- Follow the Python and pytest naming rules in `local_rules.md`.
- Add or update tests with every behavioural change.
- Mirror the source layout under `tests/` where practical.
- Add useful structured logging at system boundaries; never log secrets or private memory text.
- Use wholly synthetic data in tests and examples.
- Record architectural changes as numbered decisions under `docs/decisions/`.
- Prefer the smallest implementation that satisfies the acceptance criteria.

## Change workflow

1. Confirm the approved issue and dependency state.
2. Create the named branch before editing; do not implement directly on `main`.
3. Make small, stable commits whose subjects begin with `[<issue-number>]`.
4. Run the smallest relevant test, then the full documented checks.
5. Inspect the complete diff for scope, naming, accidental files, and private data.
6. Open a pull request and complete every applicable section of the template.
7. Resolve CI and substantive CodeRabbit findings, or document why a finding is dismissed.
8. Wait for Jonathan's final approval before merging.
9. Verify the merged result, then delete the merged local and remote branches.

Never place real vault material in source files, fixtures, logs, screenshots, issues, or pull
request descriptions. Use wholly invented synthetic data rather than anonymised personal data.

## Before committing

Run the smallest relevant test, followed by:

```bash
gitleaks git --config .gitleaks.toml --redact
python tools/check_repository_safety.py
ruff check .
pytest
```

See [`docs/repository_safety_checks.md`](docs/repository_safety_checks.md) for installation,
allow-list, and remediation guidance.

Inspect the final diff for unrelated files, secrets, syntax errors, and formatting problems.
Issue-related commit subjects must start with `[<issue-number>]`.
