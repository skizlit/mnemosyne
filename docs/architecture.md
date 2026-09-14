# Architecture

## Boundary

Mnemosyne is the memory subsystem, not the agent system around it. It accepts durable records,
protects their history, and produces useful knowledge views for humans and authorised tools.

The NAS is the durable memory and control plane. A desktop, local model, or future Agent Manager
is a replaceable compute client. Losing a compute client must not lose the memory.

## Data flow

1. An authorised client submits a record or immutable run bundle.
2. Mnemosyne validates its identity, project boundary, metadata, and attachments.
3. The original input is written once to the raw record.
4. Compilation produces readable project knowledge, indexes, and explicit relationships.
5. Obsidian and retrieval tools consume compiled knowledge.
6. Disposable indexes or graphs may be rebuilt entirely from the authoritative Markdown.

## Storage layers

| Layer | Purpose | Authority | Mutation rule |
| --- | --- | --- | --- |
| `raw/` | Original notes, imports, and run bundles | Authoritative evidence | Append only |
| `wiki/` | Compiled project knowledge and indexes | Derived knowledge | Regenerated deliberately |
| `views/` | Graphs, search indexes, and tool-specific projections | Disposable | Rebuild at any time |
| `audit/` | Record of accepted writes and administrative actions | Authoritative history | Append only |

The exact vault schema will be specified and tested before implementation. These names describe
roles, not permission for this source repository to contain real memory data.

## Project isolation

Every stored item belongs to a project or an explicitly global area. Cross-project access is
denied by default. Sharing happens through a deliberate promotion or synopsis with its source
recorded; it is not inferred from filesystem proximity.

## Agent run bundles

A future Agent Manager may export an immutable run bundle containing inputs, declared outputs,
decisions, tool results suitable for retention, and provenance. Mnemosyne does not retain hidden
reasoning or create separate private memories for individual agents.

## Obsidian

Obsidian is a human interface over compiled Markdown. It may add links and navigation metadata to
the compiled knowledge area, but plugins, caches, layouts, and graph state are not authoritative.
The memory must continue to work when Obsidian is closed or removed.

## Safety boundary

Notes, imported content, and model output are untrusted data. No text stored in memory grants
permission to run a command, load a plugin, cross a project boundary, or disclose a secret.
Automation must use explicit allow-listed operations and validated paths.
