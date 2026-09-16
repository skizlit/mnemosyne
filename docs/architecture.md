# Architecture

## Purpose

Mnemosyne is a memory system only. It captures information, consolidates it into durable
knowledge, retrieves relevant knowledge later, and applies corrections to the existing current
truth.

It starts from scratch. No storage layout, workflow, or component is inherited from Second Brain
unless it independently proves useful for Mnemosyne.

## Components

### Markdown vault

The vault contains the authoritative memory as ordinary Markdown. A person must be able to read,
copy, back up, and repair it without Mnemosyne.

The canonical directory structure is defined in
[decision 0005](decisions/0005-canonical_vault_layout.md). The canonical knowledge-document
format is defined in [decision 0006](decisions/0006-canonical_markdown_memory_format.md).

### Obsidian

Obsidian opens the Markdown vault directly. It is the human interface for reading, editing,
linking, and navigating memory. Mnemosyne must recognise valid edits made through Obsidian.

Obsidian is not required for the Python engine to operate.

### Python memory engine

Python provides four responsibilities:

1. Capture new information.
2. Consolidate related information rather than blindly creating duplicates.
3. Update current knowledge when a correction is accepted.
4. Retrieve relevant knowledge for a later session.

Interfaces and external integrations sit outside the initial memory proof.

### Optional retrieval index

File and metadata retrieval will be proved first. SQLite, embeddings, vectors, or a knowledge
graph may be evaluated later if measurements show that they improve recall.

Any such index is disposable. Deleting it must not delete knowledge, and rebuilding it from
Markdown must restore its complete state.

## First vertical slice

The first slice is intentionally small:

1. Store one synthetic memory.
2. construct a fresh engine instance from the same vault;
3. retrieve that memory;
4. correct it using its stable identity;
5. construct another fresh engine instance; and
6. retrieve only the corrected statement as current knowledge.

Passing this test proves persistence across sessions and correct update behaviour. It does not
claim that semantic retrieval, automatic capture, or integrations are solved.

## Boundaries

- Real personal memory never enters this source repository.
- The vault location is configurable and may later live locally or on the NAS.
- The core does not depend on a paid model, paid database, or paid cloud storage.
- Stored content never grants permission to execute code or access another path.
- A full agent harness, chat integration, and Jarvis-style interface are separate future projects.
