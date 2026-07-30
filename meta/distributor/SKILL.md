---
name: distributor
description: "Discoverability guarantor + skill router. Injects all registered skill descriptions into context at session start (prevents model from forgetting installed skills), then routes each user task to the best-matching skill via keyword + fuzzy scoring with risk penalty. Always-active; the entry point of every task."
user-invocable: false
risk_level: low
category: meta
always_active: true
---

# Distributor (分发器)

Two responsibilities, in priority order:

1. **Discoverability guarantee** (primary) — at session start, read `INDEX.yaml` and inject every registered skill's `name` + `description` into context. This is the anti-hallucination mechanism: the model cannot "forget" a skill it has been explicitly told exists.
2. **Routing** (secondary) — match each user task against skill descriptions; produce a match score (0-100) with risk penalty; forward to the top match or report a gap.

**Always-active** (`user-invocable: false`); loaded into every session as the entry point.

## Why this exists

Model hallucination ("installed but ignored") has three root causes:

| Cause | Mechanism here |
|---|---|
| Model never loaded the skill's description | Session-start injection forces all descriptions into context |
| Model loaded it but mis-routes | Keyword routes (exact) + fuzzy score (semantic) pick the best match; model does not choose freely |
| Model chose a skill but skipped execution | Review's Reflection Gate catches "mentioned but not called" and re-injects |

Distributor owns causes 1 and 2. Review owns cause 3 (see [meta/review/SKILL.md](../review/SKILL.md)).

## Responsibilities

### 1. Session-start discoverability injection

On session start (before any user task):

1. Read `INDEX.yaml` in this directory.
2. For every skill entry, resolve its `SKILL.md` and read the frontmatter `description`.
3. Inject a compact manifest into context:
   ```
   [Available skills]
   - <name>: <description>
   - <name>: <description>
   ...
   ```
4. The model now has the full menu. It cannot claim it did not know a skill existed.

### 2. Per-task routing

For each user task:

1. Tokenize the task.
2. Check `KEYWORD_ROUTES` in `score.py` for exact phrase matches (high precision).
3. If no keyword hit, run fuzzy scoring: description-vs-task F1 + name bonus + bigram bonus.
4. Apply risk penalty (`low=0, mid=-10, high=-30`).
5. Pick the highest composite score.
6. If above threshold (default 50), forward to that skill.
7. If below threshold, **report a gap** — tell the user "no installed skill matches; consider importing one with `installer import <repo>` or writing a new SKILL.md". Do **not** silently proceed without a skill.

## What was removed (vs. earlier design)

The previous Distributor force-triggered a horizontal discipline layer (thinking-first / caveman / grill-with-docs) and a Builder module. These have been removed:

- **thinking-first / caveman** — cognitive discipline is the model's own responsibility (extended thinking, system prompt). Wrapping it as forced skills added overhead without improving output quality.
- **grill-with-docs** — design interrogation is covered by the ecosystem (e.g. superpowers `brainstorming`). MY_SKILL no longer ships its own.
- **Builder** — auto-generating new skills on gap was over-engineered for the actual usage frequency. On gap, Distributor now reports and lets the user decide (import or hand-write).

See `docs/adr/0008-slim-infra-not-content-library.md` for the rationale.

## Trigger

- **Auto**: every session start (discoverability injection) + every user task (routing). Not user-invocable.

## Procedure

1. **Session start**: run discoverability injection (above).
2. **User task arrives**: tokenize → keyword route → fuzzy score → risk penalty → pick top.
3. If top composite ≥ threshold: forward to matched skill.
4. If top composite < threshold: report gap; suggest `installer import` or manual SKILL.md creation.
5. After skill executes: hand off to Review for the Reflection Gate (did the model actually call the skill it said it would?).

## Pitfalls

- **Skipping session-start injection**: the single most common failure mode. If the model "forgets" a skill, it is almost always because the injection did not run. Bootstrap verifies this; do not skip.
- **Over-routing on broad keywords**: a high match score on a broadly-named skill may dominate a more specific one. Keyword routes exist to fix this; keep them curated.
- **Threshold miscalibration**: 50 is the default. Too high → too many false gaps; too low → poor routing.
- **INDEX.yaml drift**: if INDEX.yaml is out of sync with the filesystem, injection will list phantom skills or miss real ones. Bootstrap detects this on session start.

## Verification

- Every session start must produce the `[Available skills]` manifest in context.
- Every user task must end with either: (a) a skill forwarded and executed, or (b) a gap reported with an actionable suggestion.
- No task should be silently dropped.
- `last_reviewed` in INDEX.yaml must be current (Review's lifecycle responsibility).
