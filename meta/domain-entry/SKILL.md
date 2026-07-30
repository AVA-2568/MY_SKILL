---
name: domain-entry
description: "Browse the skill registry. Use when the user asks \"what skills do you have\", wants to browse available skills, or is uncertain which skill fits their need. Lists skills from INDEX.yaml grouped by category."
user-invocable: true
risk_level: low
category: meta
---

# Domain Entry (领域入口)

Browsing entrypoint for the skill registry. Lists skills from INDEX.yaml grouped by category.

## Categories

The registry supports 5 LLM-capability categories (skills can be added via `importer.py` from external repos):

| Category | Meaning | Current skills |
|---|---|---|
| **Understanding** | Read input, parse context, recognize intent | *(none — import as needed)* |
| **Generation** | Produce output: code, documents, schemas, visual specs | `ui-design`, `ux-design` |
| **Retrieval** | Find information, query data, call APIs | *(none — use MCP)* |
| **Execution** | Run commands, manipulate files, invoke tools | *(none — platform-native)* |
| **Decision** | Plan, choose, weigh tradeoffs | `decide-invest` |

Most common skills (code understanding, RAG, bash/git execution) have better ecosystem equivalents in `obra/superpowers` or platform-native tooling. Import them with `installer import owner/repo` when needed. The 3 current seeds exist because no public equivalent covers their domain.

## Trigger

- **Manual**: `/domain` to list all skills; "what skills do you have" triggers this naturally.
- **Auto**: Distributor may call this when a user request is broad and needs clarification.

## Procedure

1. Read INDEX.yaml fresh (do not cache).
2. List all registered skills grouped by category.
3. If user asks "which skill fits X": analyze the task and recommend 1-2 specific skills.
4. Routing to a specific skill still goes through Distributor (not directly from Domain-entry).

## Pitfalls

- **Don't bypass Distributor**: Domain-entry is for browsing; actual routing goes through Distributor's score + risk logic.
- **Stale listings**: always read INDEX.yaml fresh; skills may have been imported or retired since last session.

## Verification

- A category listing must match INDEX.yaml (no orphaned entries, no missing skills).
- Routing to a specific skill must still go through Distributor.
