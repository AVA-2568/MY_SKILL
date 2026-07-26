---
name: domain-entry
description: Domain layer entry point — list, search, and dispatch to skills in the five LLM capability categories. Use when the Distributor has matched a category but the agent needs to locate the specific skill. Not user-invocable; loaded on-demand by Distributor.
user-invocable: false
risk_level: low
category: meta
agent_created: true
---

# Domain Entry (领域入口)

Domain layer entry point. Navigates the five LLM capability categories to locate specific skills.

## When This Triggers

Distributor loads Domain-entry when:
- A task has been classified into a capability category
- The Distributor needs to locate the specific skill within that category

## Procedure

1. Receive the capability category and task description from Distributor.
2. Scan the `domain/<category>/` directory for matching skills.
3. Score each skill by description relevance to the task.
4. Return the top match (or "no match" if none above threshold).

## Category Map

| Category | Directory | Seed Skills |
|---|---|---|
| understanding | `domain/understanding/` | comprehend-code, comprehend-doc |
| generation | `domain/generation/` | generate-api, generate-doc, api-design, system-design, database-design, ui-design, ux-design, writing-great-skills, handoff, teach |
| retrieval | `domain/retrieval/` | retrieve-rag, retrieve-sql |
| execution | `domain/execution/` | execute-bash, execute-git |
| decision | `domain/decision/` | decide-invest, decide-product |

## Pitfalls

- Don't return a low-relevance match just to avoid "no match"; gap detection triggers the Builder.
- Don't hardcode the category list; derive it from the filesystem (future-proof for new categories).

## Verification

- The returned skill genuinely matches the task (not a forced fit).
- "No match" is returned when no skill scores above threshold.
- The search covers all skills in the category directory.
