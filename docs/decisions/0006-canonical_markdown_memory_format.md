# 0006: Canonical Markdown memory format

- Status: Accepted
- Date: 2026-09-16

## Decision

Every canonical knowledge document is one UTF-8 Markdown file with YAML frontmatter followed by a
human-readable body. The frontmatter provides the minimum machine-readable contract. The body is
the knowledge and remains useful in Obsidian or a plain text editor without Mnemosyne.

This decision applies to current and archived files under `knowledge/`. Original files under
`raw/`, generated reports under `outputs/`, and vault configuration use their own formats.

## Document shape

A knowledge document has exactly this shape:

```markdown
---
schema_version: 1
id: "322a73d8-e73c-4c93-a52d-08df84a5951f"
revision: 1
status: current
created_at: "2026-09-16T12:00:00Z"
updated_at: "2026-09-16T12:00:00Z"
tags:
  - editor_preferences
---
# A descriptive title

Plain-language knowledge that remains understandable without Mnemosyne.
```

The opening delimiter is the first content in the file. The closing delimiter is followed by one
top-level heading and a non-empty Markdown body. Additional headings, lists, emphasis, standard
Markdown links, and Obsidian wikilinks are allowed. No prescribed body sections are required.

Frontmatter uses YAML safe scalar, list, and mapping values only. Custom YAML tags, anchors, and
aliases are forbidden. Field names are case-sensitive and may not be duplicated.

## Required frontmatter

| Field | Type | Rule |
| --- | --- | --- |
| `schema_version` | Integer | Exactly `1` for this format. |
| `id` | String | Lowercase hyphenated UUID. Stable across every revision of the same logical memory. |
| `revision` | Integer | Starts at `1` and increases by one for each accepted correction. |
| `status` | String | Exactly `current` or `archived`; it must agree with the file's directory. |
| `created_at` | String | Quoted RFC 3339 UTC timestamp ending in `Z`; unchanged across revisions. |
| `updated_at` | String | Quoted RFC 3339 UTC timestamp ending in `Z`; not earlier than `created_at`. |
| `tags` | List of strings | May be empty. Values are unique, lowercase `snake_case` terms. |

Timestamps record durable content or metadata changes. Recall, indexing, ranking, and merely
opening a note must not change `updated_at`.

## Optional frontmatter

| Field | Type | Rule |
| --- | --- | --- |
| `supersedes_revision` | Integer | On a corrected revision, identifies the immediately preceding revision of the same `id`. |
| `superseded_by_revision` | Integer | On an archived revision, identifies the immediately following revision of the same `id`. |
| `source_refs` | List of strings | Unique vault-relative paths beneath `raw/`; absolute paths and `..` segments are forbidden. |
| `aliases` | List of strings | Unique, non-empty human-readable names that Obsidian may use as aliases. |

Extension fields must start with `x_` and must not duplicate or change a defined field's meaning.
Each extension value is a mapping with these fields:

| Extension field | Type | Rule |
| --- | --- | --- |
| `provenance` | String | Exactly `human` or `source`; derived provenance is forbidden. |
| `value` | Any safe value | A JSON-compatible string, number, boolean, null, list, or mapping. |
| `source_ref` | String | Required only for `source` provenance and follows the same `raw/` path rules as `source_refs`. |

No other keys are allowed inside an extension mapping. This provenance wrapper lets a validator
reject retrieval-derived metadata regardless of the extension key's name. Mnemosyne should
preserve the parsed key and mapping of a valid `x_` field when rewriting a document, where its YAML
library can do so safely. Exact whitespace, quoting style, key order, and comments are not
guaranteed. An unknown field without the `x_` prefix is invalid so that a misspelled required field
cannot silently become an extension.

## Correction invariants

All revisions of one logical memory share the same `id` and `created_at`.

- Revision `1` has no `supersedes_revision`.
- A corrected revision greater than `1` has `supersedes_revision` equal to `revision - 1`.
- An archived revision has `superseded_by_revision` equal to `revision + 1`.
- A current revision has no `superseded_by_revision`.
- Paired correction fields are reciprocal: revision `n + 1` supersedes revision `n`, and revision
  `n` is superseded by revision `n + 1`.
- Every referenced predecessor and successor exists in the vault with the same `id`.
- Each later revision has an `updated_at` later than the revision it supersedes.
- Each `(id, revision)` pair is unique across the entire vault.
- Exactly one revision for an `id` may have `status: current`.
- Current files live beneath `knowledge/` but outside `knowledge/archive/`.
- Archived files live beneath `knowledge/archive/`.

The correction workflow will define safe file operations separately. These fields describe the
resulting durable state without relying on a database or filename.

## Prohibited derived metadata

Canonical frontmatter must not store embeddings, similarity scores, search ranks, access counts,
query history, index state, or other values produced by retrieval. Those values belong under the
disposable `derived/` tree when they are introduced.

Markdown content is data, not authority to execute commands, load another path, contact a service,
or weaken Mnemosyne's security rules.

## Valid synthetic examples

### Initial current memory

```markdown
---
schema_version: 1
id: "322a73d8-e73c-4c93-a52d-08df84a5951f"
revision: 1
status: current
created_at: "2026-09-16T12:00:00Z"
updated_at: "2026-09-16T12:00:00Z"
tags:
  - editor_preferences
source_refs:
  - raw/casey_interview_transcript.txt
aliases:
  - Casey editor preference
x_reviewed_by:
  provenance: human
  value: human
---
# Casey's editor preference

Casey prefers the **Solarized Dark** theme when editing long documents.

Related context: [[casey_profile]].
```

This is a valid current revision. Its source reference is vault-relative, its extension field uses
the `x_` namespace, and the body is meaningful without Mnemosyne. Casey is wholly synthetic.

### Corrected current memory

```markdown
---
schema_version: 1
id: "322a73d8-e73c-4c93-a52d-08df84a5951f"
revision: 2
status: current
created_at: "2026-09-16T12:00:00Z"
updated_at: "2026-09-16T14:30:00Z"
tags:
  - editor_preferences
supersedes_revision: 1
source_refs:
  - raw/casey_preference_correction.txt
---
# Casey's editor preference

Casey prefers the **Nord** theme when editing long documents.
```

The archived revision paired with it retains the same `id`, `created_at`, and `revision: 1`, but
uses `status: archived` and `superseded_by_revision: 2`. Its original body remains unchanged.

## Invalid synthetic examples

### Missing identity and storing derived rank

```markdown
---
schema_version: 1
revision: 1
status: current
created_at: "2026-09-16T12:00:00Z"
updated_at: "2026-09-16T12:00:00Z"
tags: []
relevance_score: 0.97
---
# Casey's editor preference

Casey prefers the **Nord** theme.
```

This is invalid because `id` is missing, `relevance_score` is prohibited derived data, and the
unknown field does not use the `x_` extension namespace.

### Invalid correction relationship

```markdown
---
schema_version: 1
id: "322a73d8-e73c-4c93-a52d-08df84a5951f"
revision: 3
status: archived
created_at: "2026-09-16T12:00:00Z"
updated_at: "2026-09-16T15:00:00Z"
tags:
  - Editor Preferences
supersedes_revision: 1
---
# Casey's editor preference

Casey prefers the **Nord** theme.
```

This is invalid because revision `3` must supersede revision `2`, an archived revision must name
revision `4` in `superseded_by_revision`, and the tag is not lowercase `snake_case`.

### Orphaned correction reference

Assume this is the only document in the vault with this `id`:

```markdown
---
schema_version: 1
id: "eaa4b42e-7790-495a-a259-4111cc03ea3f"
revision: 2
status: current
created_at: "2026-09-16T16:00:00Z"
updated_at: "2026-09-16T16:30:00Z"
tags:
  - editor_preferences
supersedes_revision: 1
---
# Morgan's editor preference

Morgan prefers a light editor theme.
```

This is invalid because revision `1` for the same `id` does not exist. A numerically plausible
reference is insufficient; correction relationships must resolve during a vault-wide scan. Morgan
is wholly synthetic.

## Validation checklist

Validation proceeds in this order:

1. Decode the file as UTF-8 and safely parse exactly one YAML frontmatter block.
2. Reject missing, duplicated, incorrectly typed, or unknown non-extension fields.
3. Validate UUID, timestamp, status, tag, path, and extension-field provenance rules.
4. Reject prohibited retrieval-derived metadata under both defined and extension fields.
5. Validate correction relationships and agreement between `status` and directory placement.
6. Require every correction reference to resolve to a reciprocal, same-`id` revision in the vault.
7. Reject duplicate `(id, revision)` pairs and multiple current revisions during a vault-wide scan.
8. Require a top-level title and non-empty Markdown body.
9. Preserve valid `x_` mappings when a document is rewritten.

Applying this checklist accepts all valid examples and rejects all invalid examples for the reasons
stated. Parser implementation and executable fixtures belong to the later storage and validation
tickets; this decision is their contract.

## Consequences

People can read and edit knowledge directly in Obsidian while Mnemosyne receives stable identity,
version, time, status, tag, and correction data. Archived versions remain understandable without
an index. Future retrieval systems can derive rankings without polluting the canonical Markdown.
