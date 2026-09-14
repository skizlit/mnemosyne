# 0003: Obsidian is the human interface

- Status: Accepted
- Date: 2026-09-14

## Decision

Obsidian opens the authoritative Markdown vault directly. It may be used to read, edit, link, and
navigate current knowledge.

Python remains responsible for programmatic capture, consolidation, correction, and retrieval.

## Reason

Obsidian supplies a mature human editing and navigation experience without making its application
database the owner of the memory.

## Consequence

Mnemosyne must tolerate valid Obsidian edits and ignore disposable workspace state. The memory
engine must also work when Obsidian is closed or uninstalled.
