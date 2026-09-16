# Public-code/private-memory boundary

## Purpose

The Mnemosyne source repository is intended to become public. The memory vault is private runtime
data. They are separate security zones even when the same computer runs the code and accesses the
vault.

This boundary applies to source files, commits, branches, pull requests, issues, test output,
screenshots, logs, documentation, and release artifacts.

## Public source repository

The repository may contain:

- Mnemosyne source code and packaging files;
- automated tests that use invented people, facts, paths, and identifiers;
- synthetic fixtures that are clearly labelled as synthetic;
- generic documentation, schemas, and vault templates;
- configuration examples containing placeholders only; and
- CI configuration and disposable-index implementations that contain no runtime data.

Public examples must be created for the project. Real memory must not be copied and then
anonymised for use as a fixture because identifying details can be missed.

## Private runtime data

The following must never enter the repository or any GitHub discussion or artifact:

- a real vault or any memory, note, attachment, import, export, or backup from it;
- personal, family, work, account, health, financial, location, or communication data;
- secrets such as passwords, tokens, cookies, private keys, recovery codes, and populated
  environment files;
- private infrastructure details such as hostnames, IP addresses, usernames, share names,
  absolute vault paths, mount paths, tunnel details, and device configuration;
- runtime logs, crash dumps, temporary files, generated databases, indexes, or embeddings that
  may reproduce memory content; and
- local Obsidian workspace state or plugin data that may reveal private filenames or content.

Public account names that are deliberately used to identify repository authors are repository
metadata, not memory content. They must not be reused inside memory examples.

## Location rule

A real vault must be configured at a location outside the Git worktree. This remains true for a
local development vault, a synchronized Obsidian folder, and a vault mounted into a future NAS
container.

Mnemosyne must not provide a command that copies a real vault into the repository. The future
vault-initialization command must refuse any destination inside a Mnemosyne Git worktree. Generic
templates may live in the repository, but they may contain only synthetic content and placeholder
configuration.

## Examples

| Item | Allowed? | Reason |
| --- | --- | --- |
| Invented memory in `tests/fixtures/` | Yes | Purpose-built synthetic test data |
| `.env.example` with `<private-vault-path>` | Yes | Placeholder without a private value |
| Generic schema or empty vault template | Yes | Structure without runtime data |
| `vault/`, `local_data/`, or an Obsidian export | No | Potentially real memory data |
| Populated `.env`, token, key, cookie, or credential | No | Secret material |
| Real NAS address, share, user, mount, or sync path | No | Private infrastructure data |
| Runtime log, database, index, embedding, or crash dump | No | May reproduce private memory |
| Copied real note with names replaced | No | Anonymisation can miss private details |

## Before committing or publishing

1. Confirm every example and fixture was invented for the repository.
2. Inspect staged file names and content for vault data, private paths, and credentials.
3. Run the repository's leak checks once they are introduced by S0-03.
4. Keep the repository private if the result is uncertain.

`.gitignore` reduces accidents but is not a security control by itself. S0-02 expands repository
exclusions, and S0-03 adds automated leak checks. Until those safeguards exist, every change needs
a manual boundary review.

## If private data is found

Stop publication and do not copy the value into an issue or pull request. Treat exposed
credentials as compromised and rotate them. Remove the data from both the working tree and Git
history before making the repository public, then repeat the full audit required by S0-04.
