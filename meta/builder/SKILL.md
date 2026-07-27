---
name: builder
description: "Create a new skill on demand when Distributor detects a skill gap, or when the user wants to add a new capability to the library. Three internal sub-modules — confirm (clarify user intent) → plan (design skill structure) → generate (write SKILL.md + bundled resources). Loaded on demand by Distributor; manually invocable via `/builder`."
user-invocable: true
risk_level: low
category: meta
---

# Builder (构建器)

Creates new skills on demand. Triggered by Distributor when no existing skill matches the user task; also manually invocable.

## Internal Sub-modules (3)

1. **confirm** — clarify user intent; ask one question at a time if the request is ambiguous.
2. **plan** — design the skill's structure: category (one of 5 LLM capabilities), bundled resources (scripts/references/assets), trigger phrases, completion criteria.
3. **generate** — write the SKILL.md and any bundled resources to the appropriate `domain/<category>/<skill-name>/` directory; update INDEX.yaml.

## Trigger

- **Auto**: called by Distributor when skill gap is detected.
- **Manual**: user invokes `/builder` directly with a skill idea.

## Procedure

1. Receive the user task and the gap context from Distributor (or read the user's direct request).
2. Run `confirm`: ask one clarifying question if needed (e.g., "Should this skill handle X or Y?"); if no question is needed, proceed.
3. Run `plan`: design the skill structure; output a SKILL.md draft.
4. Run `generate`: write the file(s) to disk under `domain/<category>/<skill-name>/`; update INDEX.yaml via Distributor; commit the change.
5. Return the new skill's name to Distributor; Distributor re-routes the original task.

## Pitfalls

- **Premature generation**: Do not write the SKILL.md before `plan` is approved (or at least before the design feels coherent).
- **Bundled resource bloat**: Skills with too many scripts/references are hard to maintain; keep bundled resources minimal.
- **Frontmatter incompleteness**: `risk_level`, `category`, and `user_invocable` must all be set; otherwise Distributor cannot route correctly.
- **Category misclassification**: Skills that span multiple LLM capabilities should pick the *primary* capability in `category:`; document the secondary in the SKILL.md body.

## Verification

- After generation, the new skill must be routable: re-run Distributor's matching against INDEX.yaml; the new skill must appear and match the original task.
- The new skill must have at least one bundled resource (or be explicitly documented as \"no resources needed\").
- INDEX.yaml must reflect the new skill before generation is considered complete.
