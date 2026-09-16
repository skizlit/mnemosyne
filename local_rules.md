# Mnemosyne local programming rules

These project rules record language and tool conventions that differ from, or refine, the shared
`master_rules.md`.

## Python naming

Follow Python's established conventions:

- modules, Python files, functions, methods, and variables use `snake_case`
- classes use `PascalCase`
- constants use `UPPER_SNAKE_CASE`
- tool-recognised files retain their conventional names

## Tests

Pytest is configured to use Jonathan's class/file test convention:

- a test file is named `<subject>_tests.py`
- a test class is named `<Subject>Tests`
- test methods retain pytest's required `test_<behaviour>` form
- the source layout is mirrored beneath `tests/` where practical

Every behavioural change requires meaningful automated coverage. Use entirely synthetic test data.
