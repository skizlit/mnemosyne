# 0005: Canonical vault layout

- Status: Accepted
- Date: 2026-09-16

## Decision

Mnemosyne uses one configured Obsidian vault for its durable, human-readable data. Original source
material, canonical knowledge, generated outputs, and non-secret configuration have distinct
locations. Derived retrieval data lives outside the vault.

The layout is:

```text
<private_data_root>/
├── vault/
│   ├── raw/
│   ├── knowledge/
│   │   └── archive/
│   ├── outputs/
│   │   └── archive/
│   ├── configuration/
│   │   └── operational_metadata/
│   └── .obsidian/
└── derived/
```

`<private_data_root>` and the folder named `vault` in this diagram are deployment placeholders,
not prescribed private paths. The configured vault root is the directory that Obsidian opens and
that Mnemosyne receives through external configuration.

## Directory responsibilities

| Location | Responsibility | Durable |
| --- | --- | --- |
| `raw/` | Original source files preserved as the immutable evidence baseline. | Yes |
| `knowledge/` | Current, canonical, cross-linked Markdown knowledge. | Yes |
| `knowledge/archive/` | Superseded knowledge retained for correction history and provenance. | Yes |
| `outputs/` | Current human-facing reports generated from the vault. | Yes |
| `outputs/archive/` | Retired or superseded generated reports. | Yes |
| `configuration/` | Human-readable rules and non-secret settings used to interpret or operate the vault. | Yes |
| `configuration/operational_metadata/` | Small recovery-safe metadata, such as a vault identifier or format version. | Yes |
| `.obsidian/` | Optional Obsidian preferences, hotkeys, themes, plugin settings, and workspace state. | No |
| `derived/` | Future indexes, caches, embeddings, or other reproducible retrieval data. | No |

Project-owned directory and file names use `snake_case`. `.obsidian` is the sole named directory
exception because Obsidian requires that tool-recognised name. The filename rules for source,
knowledge, and output files are intentionally deferred to S1-03.

## Data-layer boundaries

Files accepted into `raw/` are never edited in place by a person or by Mnemosyne. A correction to
source material is stored as a new source file so that the original evidence remains available.
The supported source formats and ingestion contract will be defined by later tickets.

`knowledge/` is not a disposable compilation of `raw/`. It is Mnemosyne's canonical understanding
and is edited directly by Mnemosyne or through Obsidian. Links and backlinks are expressed by the
Markdown files, so there is no separate `links/` directory.

Current knowledge lives directly beneath `knowledge/`, using subject folders when useful. When a
correction supersedes a knowledge document, the previous version moves to `knowledge/archive/`.
Recall excludes the archive unless historical information is explicitly requested.

Generated reports belong in `outputs/`. An output does not become canonical knowledge merely
because Mnemosyne generated it. Durable facts discovered while producing a report must be written
to `knowledge/` deliberately. Retired reports move to `outputs/archive/`; active reports do not use
`archive/` as their destination.

Operational metadata is subordinate to the vault configuration rather than a separate content
layer. `configuration/` and `configuration/operational_metadata/` must never contain credentials,
absolute private paths, device names, memory bodies, logs, search rankings, or index state. Secrets
and machine-specific configuration remain outside the vault.

## Canonical and backup boundary

A complete Mnemosyne backup contains:

- every accepted source file under `raw/`;
- every Markdown file under `knowledge/`, including `knowledge/archive/`;
- every retained report under `outputs/`, including `outputs/archive/`; and
- supported files under `configuration/`, including safe operational metadata.

`.obsidian/` may be backed up for convenience, but it is editor state rather than Mnemosyne memory.
Mnemosyne cannot require it for remember, recall, correction, validation, report generation, or
restore. A fresh Obsidian installation must be able to open the vault without a third-party plugin.

`derived/` is a sibling of the vault rather than a child of it. It is configured independently,
may be absent, and must be safe to delete in full. Mnemosyne must be able to rebuild any future
derived state exclusively from the canonical vault.

## Synthetic example

This example illustrates placement only. S1-02 and S1-03 will define the final Markdown schema,
stable IDs, and filenames.

```text
private_data/
├── vault/
│   ├── raw/
│   │   └── casey_interview_transcript.txt
│   ├── knowledge/
│   │   ├── casey_editor_preferences.md
│   │   └── archive/
│   │       └── casey_editor_preferences_version_1.md
│   ├── outputs/
│   │   ├── casey_preference_report.md
│   │   └── archive/
│   │       └── casey_preference_report_version_1.md
│   ├── configuration/
│   │   ├── vault_rules.md
│   │   └── operational_metadata/
│   │       └── vault_metadata.yaml
│   └── .obsidian/
└── derived/
    └── retrieval_cache/
```

Casey and the material used in this example are wholly synthetic. No example path represents a
real deployment.

## Use-case verification

| Use case | Layout behaviour |
| --- | --- |
| Remember | Preserve an original source under `raw/` when one exists, then create or update canonical Markdown under `knowledge/`. |
| Recall | Search current Markdown under `knowledge/`; consult `raw/` for evidence and `knowledge/archive/` only when requested. |
| Correct | Preserve the superseded knowledge document under `knowledge/archive/` and leave its replacement in `knowledge/`. |
| Generate | Write a current human-facing report under `outputs/` without treating the report as canonical knowledge. |
| Obsidian edit | Open `vault/` directly and edit canonical Markdown without a Mnemosyne or third-party plugin. |
| Backup | Back up all durable vault layers; optionally include `.obsidian/`; exclude the sibling `derived/` tree. |
| Restore | Restore the durable vault layers and operate without `.obsidian/` or any derived state. |
| Rebuild | Delete `derived/`, then recreate it solely from canonical files if an index is later introduced. |

## Alternatives rejected

- `raw/`, `wiki/`, and disposable compiled views would make the editable knowledge secondary to
  its source material. Mnemosyne treats both immutable sources and curated knowledge as durable.
- A top-level `memories/current/` and `memories/history/` split would not distinguish original
  evidence, canonical knowledge, and generated reports.
- A separate `links/` directory would duplicate relationships already represented by Markdown
  links and discovered by Obsidian backlinks.
- Sending active generated reports directly to an `archive/` directory would blur current output
  with retired material.
- Keeping superseded knowledge only in a database would make the vault incomplete and violate the
  Markdown source-of-truth decision.
- Placing derived indexes inside the vault would encourage Obsidian and Synology Drive to process
  disposable data and make backup boundaries less clear.
- Requiring an Obsidian plugin would make the memory dependent on an optional editor.

## Consequences

Backup and restore preserve the four durable layers: source evidence, knowledge, outputs, and
configuration. Recall defaults to current knowledge, while source evidence and correction history
remain directly inspectable. Obsidian state and future retrieval indexes cannot become
authoritative. The schema, filename, correction, and recall contracts will refine this layout
without changing its canonical boundaries.
