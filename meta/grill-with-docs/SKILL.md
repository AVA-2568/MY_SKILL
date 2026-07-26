---
name: grill-with-docs
description: On-gap design interrogation — when Distributor detects no matching skill for a task, grill the user about design intent (what should the missing skill do) and land the result as an ADR + glossary entry. Force-triggered by Distributor at the gap-detection point. Not user-invocable; part of the horizontal layer.
user-invocable: false
risk_level: low
category: meta
agent_created: true
---

# Grill with Docs (文档化审问)

On-gap design interrogation + ADR/glossary landing.

## When This Triggers

Distributor triggers Grill-with-Docs when:
- A user task has no matching skill (gap detected)
- Before Builder is invoked

## Procedure

1. **Interrogate**: ask the user what the missing skill should do. Clarify boundaries.
2. **Document**: write the answer as a new ADR (in `docs/adr/`) and update the glossary (`CONTEXT.md`).
3. **Hand off to Builder**: pass the clarified intent to Builder for skill creation.

## Pitfalls

- Don't skip the interrogation step; assumptions about what the user wants lead to wrong skills.
- Don't create ADRs for trivial clarifications; only for design decisions that affect architecture.

## Verification

- ADR is written and follows the ADR format.
- Glossary has a new or updated term.
- Builder receives a clear, interrogated design intent.
