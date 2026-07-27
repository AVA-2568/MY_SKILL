---
name: domain-entry
description: "Overview of the 5 LLM-capability categories in the domain layer (Understanding / Generation / Retrieval / Execution / Decision). Use when the user wants to browse the skill library, asks \"what skills do you have\", or is uncertain which category fits their need."
user-invocable: true
risk_level: low
category: meta
---

# Domain Entry (领域入口)

5 LLM-capability categories. Use to browse the library or to understand which category a task belongs to.

## Categories

| Category | Meaning | Use for |
|---|---|---|
| **Understanding** | Read input, parse context, recognize intent | \"Read this code and tell me what it does\" / \"Parse this JSON\" |
| **Generation** | Produce output: code, documents, interface contracts, architecture, schemas, visual specifications | \"Write an API endpoint\" / \"Design an API\" / \"Design a system\" / \"Create a UI spec\" |
| **Retrieval** | Find information, query data, call APIs (incl. analysis) | \"Search for X\" / \"Query the database\" / \"Analyze this data\" |
| **Execution** | Run commands, manipulate files, invoke tools | \"Run the test suite\" / \"Deploy this\" |
| **Decision** | Plan, choose, weigh tradeoffs (incl. analysis) | \"Should we invest in X?\" / \"Pick between A and B\" |

Generation contains implementation-oriented skills (`generate-api`, `generate-doc`), design-oriented skills (`api-design`, `system-design`, `database-design`, `ui-design`, `ux-design`), and productivity-oriented skills forked from mattpocock/skills (`writing-great-skills`, `handoff`, `teach`). Design skills produce contracts and specifications; implementation skills turn specifications into artifacts; productivity skills support the user across sessions.

## Trigger

- **Manual**: `/domain` to list all categories; `/domain <category>` to list skills in a category.
- **Auto**: Distributor may call this when a user request is broad and needs category clarification.

## Procedure

1. If user asks for a category overview: list skills in that category from INDEX.yaml.
2. If user asks \"which category fits X\": analyze the task and recommend a primary category.
3. If user picks a category, list skills; user picks a skill; route to it via Distributor.

## Pitfalls

- **Don't bypass Distributor**: Domain-entry is for browsing; actual routing should go through Distributor's risk-score + match logic.
- **Category overlap**: Some tasks span multiple categories (e.g., \"Write a function and test it\" = Generation + Execution). Recommend the primary category; the secondary is implicit.
- **Stale listings**: Always read INDEX.yaml fresh; do not cache category listings across sessions.

## Verification

- A category listing must match INDEX.yaml (no orphaned entries).
- A category recommendation should include 1-2 specific skills in that category.
- Routing to a specific skill must still go through Distributor (not directly from Domain-entry).
