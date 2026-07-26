---
name: review
description: Horizontal review layer intercepting every task. Two scopes — per-task (Code Review / Task Recheck / Security Review with Reflection Gate) and per-skill (Lifecycle Governance: review / merge / split / retire). Always-active; runs on every task and on every library lifecycle event. Cross-cutting concern, not a peer of on-demand skills.
user-invocable: false
risk_level: low
always_active: true
horizontal: true
---

# Review (审查)

Horizontal layer. **Not on the B-Chain path**; intercepts every task at input / process / output and every library lifecycle event.

## Two Scopes

### Per-task (3 sub-types)

| Sub-type | View | Gate | Trigger |
|---|---|---|---|
| **Code Review** | Product (code/document/data) | Soft | Task produces artifacts |
| **Task Recheck** | Goal (was user intent met) | Soft | Task has verifiable outcome |
| **Security Review** | Risk (vulnerability/PII/overreach/prompt injection) | Reflection (+extreme hard) | Every task |

The **Security Review's Reflection Gate** is the standard pattern: detected risks are injected back into system context; the model must explicitly process them (fix / explain / refuse) before continuing. Cannot be silently ignored. See ADR-0004 for full detail.

### Per-skill (Lifecycle Governance)

Govern the skill library itself: review, merge, split, retire skills. This is the **meta-governance** role that no major public skill ecosystem (anthropics/skills, obra/superpowers, mattpocock/skills) abstracts as a first-class module — MY_SKILL treats it as part of Review.

## Trigger

- **Per-task**: every task (input / process / output points). Always-active.
- **Per-skill**: triggered by lifecycle events (new skill added, skill stale > 6 months, two skills overlap, etc.). See `lifecycle` section in INDEX.yaml.