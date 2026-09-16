# 0005: Canonical vault layout

- Status: Accepted
- Date: 2026-09-16

## Decision

Mnemosyne uses one configured Obsidian vault as its complete durable source of truth. Current
memories, correction history, non-secret configuration, and safe operational metadata have
separate locations inside that vault. Derived retrieval data lives outside the vault.

The layout is:

```text
<private_data_root>/
├── vault/
│   ├── memories/
│   │   ├── current/
│   │   └── history/
│   ├── configuration/
│   ├── operational_metadata/
│   └── .obsidian/
└── derived/
```

`<private_data_root>` and the folder named `vault` in this diagram are deployment placeholders,
not prescribed private paths. The configured vault root is the directory that Obsidian opens and
that Mnemosyne receives through external configuration.

## Directory responsibilities

| Location | Responsibility | Durable |
| --- | --- | --- |
| `memories/current/` | The one current version of each logical memory. | Yes |
| `memories/history/` | Superseded versions retained for correction history and provenance. | Yes |
| `configuration/` | Human-readable, vault-local settings needed to interpret or operate the vault. | Yes |
| `operational_metadata/` | Small recovery-safe metadata, such as a vault identifier or format version. | Yes |
| `.obsidian/` | Optional Obsidian workspace and plugin-free application settings. | No |
| `derived/` | Future indexes, caches, embeddings, or other reproducible retrieval data. | No |

Project-owned directory and file names use `snake_case`. `.obsidian` is the sole named
exception because Obsidian requires that tool-recognised directory name. The memory filename rules
are intentionally deferred to S1-03.

## Canonical boundary

The following data is part of a complete Mnemosyne backup:

- every Markdown file under `memories/current/`;
- every Markdown file under `memories/history/`;
- supported files under `configuration/`; and
- supported files under `operational_metadata/`.

`.obsidian/` may be backed up for convenience, but Mnemosyne cannot require it for remember,
recall, correction, validation, or restore. A fresh Obsidian installation must be able to open the
vault without a third-party plugin.

`configuration/` and `operational_metadata/` must never contain credentials, absolute private
paths, device names, memory bodies, logs, search rankings, or index state. Secrets and
machine-specific configuration remain outside the vault.

`derived/` is a sibling of the vault rather than a child of it. It is configured independently,
may be absent, and must be safe to delete in full. Mnemosyne must be able to rebuild any future
derived state exclusively from the canonical vault.

## Current and historical versions

A current memory file belongs under `memories/current/`. A superseded version belongs under
`memories/history/`. The future Markdown schema will also record version status so that files
remain understandable when copied independently.

The directory and Markdown status must agree. Mnemosyne treats a disagreement as an integrity
error rather than guessing which state is correct. S1-04 will define the ordering and recovery
rules for moving a corrected version into history while establishing its replacement as current.

## Synthetic example

This example illustrates placement only. S1-02 and S1-03 will define the final Markdown schema,
stable IDs, and filenames.

```text
private_data/
├── vault/
│   ├── memories/
│   │   ├── current/
│   │   │   └── casey_editor_theme.md
│   │   └── history/
│   │       └── casey_editor_theme_version_1.md
│   ├── configuration/
│   │   └── vault_config.yaml
│   ├── operational_metadata/
│   │   └── vault_metadata.yaml
│   └── .obsidian/
└── derived/
    └── retrieval_cache/
```

Casey and the editor preference used in related examples are wholly synthetic. No example path is
a real deployment path.

## Use-case verification

| Use case | Layout behaviour |
| --- | --- |
| Remember | Write one canonical Markdown document beneath `memories/current/`. |
| Recall | Search current Markdown by default; inspect `memories/history/` only when history is explicitly requested. |
| Correct | Preserve the superseded document under `memories/history/` and leave exactly one replacement under `memories/current/`. |
| Obsidian edit | Open `vault/` directly and edit canonical Markdown without a Mnemosyne or third-party plugin. |
| Backup | Back up the durable vault locations; optionally include `.obsidian/`; exclude the sibling `derived/` tree. |
| Restore | Restore the durable vault locations and operate without any derived state. |
| Rebuild | Delete `derived/`, then recreate it solely from canonical files if an index is later introduced. |

## Alternatives rejected

- A single flat directory would make current truth and correction history harder to distinguish
  safely.
- Keeping superseded versions only in a database would make Markdown incomplete and violate the
  source-of-truth decision.
- Placing derived indexes inside the vault would encourage Obsidian and Synology Drive to process
  disposable data and make backup boundaries less clear.
- Requiring an Obsidian plugin would make the memory dependent on an optional editor.

## Consequences

Backup and restore must preserve the four durable locations. Recall defaults to
`memories/current/`, while history remains directly inspectable. Future indexes receive a
separate path and cannot become authoritative. The schema, filename, correction, and recall
contracts will refine this layout without changing its canonical boundary.
