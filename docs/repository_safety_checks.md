# Repository safety checks

Mnemosyne's source repository is public code, not a storage location for the private vault or
machine-specific configuration. Two independent checks enforce that boundary:

- [Gitleaks](https://github.com/gitleaks/gitleaks) detects common credentials and the private
  Mnemosyne configuration fields defined in `.gitleaks.toml`.
- `tools/check_repository_safety.py` rejects prohibited vault paths, private infrastructure
  details, environment files, database files, logs, keys, tokens, and application metadata.

## Run locally

Install Gitleaks, then run both checks from the repository root:

```bash
gitleaks git --config .gitleaks.toml --redact
python tools/check_repository_safety.py
```

The repository guard uses only the Python standard library. It scans Git-tracked files when run
without path arguments. Pass one or more files or directories to scan a proposed subset.

## Allow-list policy

Allow-list entries must be exact, visibly synthetic placeholders. The public placeholders live in
`security/repository_safety.toml` and are mirrored in `.gitleaks.toml`. Never allow-list a broad
path, file type, rule, entropy threshold, or real-looking credential. Any addition must be reviewed
as a source-code change and documented in the pull request.

Findings redact the matched value. If a real secret is ever committed, remove it from use and
rotate it immediately; deleting it in a later commit is not sufficient.

## Test strategy

The automated tests create positive and negative fixtures in a temporary directory. The positive
fixture is deliberately synthetic and never enters Git history. CI runs the repository guard and
Gitleaks on every push and pull request.
