# 0003: Obsidian is a view over compiled knowledge

- Status: Accepted
- Date: 2026-09-14

## Decision

Obsidian will open the compiled knowledge area rather than owning or directly rewriting the
immutable raw record.

## Reason

Obsidian adds useful navigation, backlinks, and visualisation while Markdown remains portable.
Keeping it at the view layer protects raw evidence from plugins and accidental manual edits.

## Consequence

Obsidian-specific workspace state is local and ignored by Git. Mnemosyne must remain fully usable
without Obsidian.
