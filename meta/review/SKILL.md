---
name: review
description: "Two focused scopes: (1) Reflection Gate — after Distributor routes to a skill, verify the model actually executed it (catches 'mentioned but skipped'); re-inject on miss. (2) Lifecycle Governance — review/merge/split/retire skills in INDEX.yaml. Horizontal; force-triggered by Distributor after every task and on lifecycle events."
user-invocable: false
risk_level: low
category: meta
horizontal: true
---

# Review (审查)

Two scopes only. Everything else (code review, task recheck) is the platform's or the ecosystem's job — not ours.

## Scope 1: Reflection Gate (anti-skip)

This is the third layer of the anti-hallucination triad:

| Cause | Owner |
|---|---|
| Model never loaded skill description | Distributor (session-start injection) |
| Model loaded but mis-routes | Distributor (keyword + fuzzy routing) |
| **Model routed but skipped execution** | **Review (Reflection Gate)** ← this |

### Mechanism

After Distributor routes a task to skill X and the model produces output:

1. Check whether the model actually **invoked** skill X (look for skill-specific behavior / artifacts in the output).
2. If yes → pass. No action.
3. If no (the model said "I'll use X" but then did something else, or silently dropped X) → **inject the reflection**:
   ```
   [Reflection Gate] You were routed to skill <X> but there is no evidence
   you executed it. Either (a) execute <X> now, or (b) explain why <X> does
   not apply and what you did instead. Do not silently skip.
   ```
4. The model must respond to the reflection before the task is considered complete.

### Why this is the only per-task gate

Code Review and Task Recheck were removed because:
- **Code Review** — superpowers and platform-native review tools cover this better.
- **Task Recheck** — the model's own verification-before-completion handles this.

The Reflection Gate survives because **no other layer catches "routed but skipped"**. It is MY_SKILL's unique contribution to the anti-hallucination problem.

## Scope 2: Lifecycle Governance

Govern the skill registry itself. This is meta-governance that no major public skill ecosystem (anthropics/skills, obra/superpowers, mattpocock/skills) abstracts as a first-class module.

### Triggers

- New skill added (by `installer import` or manual creation) → review SKILL.md + frontmatter before registering in INDEX.yaml.
- Skill stale: `last_reviewed` older than `lifecycle.stale_after_days` (180) → re-review.
- Skill overlap: two skills' descriptions match > `lifecycle.overlap_threshold` (0.8) → recommend merge.
- Skill dead: zero usage for `lifecycle.retire_after_zero_usage_days` (90) → retire candidate.

### Procedure

1. **New-skill review**: verify frontmatter has `name`, `description`, `category`, `risk_level`, `user-invocable`; verify path exists; add to INDEX.yaml with `last_reviewed` = today.
2. **Stale-skill review**: re-read SKILL.md; if still valid, bump `last_reviewed`; if outdated, flag for update or retirement.
3. **Overlap review**: compute description similarity; if above threshold, recommend merge to the user.
4. **Retire review**: confirm zero usage; move skill to `archived/` (or delete); remove from INDEX.yaml.

## What was removed (vs. earlier design)

- **Code Review** (soft gate on artifacts) — removed; ecosystem covers this.
- **Task Recheck** (soft gate on goal completion) — removed; model's own verification handles this.
- **`always_active: true`** on Review itself — removed. Review is per-task force-triggered by Distributor (on output) and per-event (on lifecycle), not session-injected. Only Distributor is `always_active`.

See `docs/adr/0008-slim-infra-not-content-library.md` for rationale.

## Trigger

- **Per-task**: after Distributor routes + skill executes. Force-triggered by Distributor.
- **Per-skill**: on lifecycle events (new skill, stale, overlap, dead).

## Pitfalls

- **Reflection escape**: if the model replies to the reflection without actually addressing it ("I'll keep that in mind"), re-inject. The model must either execute or explicitly explain.
- **Lifecycle invisibility**: per-skill reviews must update `last_reviewed` in INDEX.yaml; otherwise governance is invisible.
- **Gate scope creep**: do not re-add Code Review / Task Recheck as soft gates. That is the ecosystem's job.

## Verification

- Per-task: every routed task must have a Reflection Gate check logged (passed or re-injected).
- Per-skill: every skill in INDEX.yaml must have a current `last_reviewed`; stale skills must be flagged.
- INDEX.yaml must match the filesystem (no phantom entries, no orphans).
