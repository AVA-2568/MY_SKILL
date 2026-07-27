---
name: distributor
description: "Route user tasks to the most appropriate skill via description matching plus risk scoring; detect skill gaps and trigger Builder. Always-active; the entry point of every task. Use when the user submits any task — even if they don't explicitly ask for routing."
user-invocable: false
risk_level: low
category: meta
always_active: true
---

# Distributor (分发器)

Routes user tasks to the most appropriate skill. **Always-active** (`user-invocable: false`); loaded into every session as the B-Chain entry point.

## Responsibilities (3 mandatory)

1. **Route** — match the user task against every skill's `description` field; produce a match score (0-100).
2. **Risk score** — apply the skill's `risk_level` (low=0, mid=-10, high=-30) to the match score; produce a composite score.
3. **Gap detection** — if no skill matches above the threshold, trigger Builder (or grill-with-docs for design tasks) to create a new skill; otherwise forward the user task to the matched skill in Domain.

## Forced Triggers (4 horizontal skills — must run, not user-invocable)

The Distributor **forces** four horizontal skills at specific points in the flow:

| Skill | Trigger point | Why forced |
|---|---|---|
| **thinking-first** | pre-route (after receiving task, before caveman) | Every task needs cognitive discipline before acting |
| **caveman (pre-think)** | after thinking-first, before routing | Constrains the *thinking* itself to 3-5 short points — not post-compress of output |
| **caveman (post-output)** | after Domain skill, before final output | Belt-and-suspenders: compress residual verbosity in Domain's output |
| **grill-with-docs** | on-gap (when match_score < threshold, OR task is design/planning) | Ambiguous tasks need design interrogation + ADR landing |

All four (thinking-first / caveman / grill-with-docs; Review runs separately) are `user-invocable: false`; they cannot be /slash-called directly by the user. Distributor invokes them internally.

Note: caveman has **two** trigger points (pre-think + post-output). This is intentional — pre-think is the primary lever (constrains thinking), post-output is the safety net (compresses residual verbosity). Both are required.

## Trigger

- **Auto**: every user task (not user-invocable; the agent must call this first before doing anything).

## Procedure

1. Receive user task.
2. **Force thinking-first** (pre-route): inject cognitive discipline into context; model self-checks understanding, source, uncertainty.
3. **Force caveman (pre-think)**: compress thinking-first's 5-rule output into 3-5 short points (each ≤10 words). Routing uses the compressed version, not the full user task.
4. Read `INDEX.yaml` (in this same directory) for the fast-lookup list of skills.
5. For each skill, compute `match_score` from description-vs-task semantic similarity (0-100).
6. Subtract risk penalty: `composite = match_score - (0 / 10 / 30 based on risk_level)`.
7. Pick the highest composite score. If above threshold (default 50), forward to that skill via Domain.
8. If below threshold, OR if task contains design/planning/architecture keywords, **force grill-with-docs** (on-gap): run relentless interrogation + land ADR/glossary.
9. After grill-with-docs lands new decisions, **trigger Builder** to create a new skill; re-run route step.
10. Domain skill executes.
11. **Force caveman (post-output)**: compress final output; preserve uncertainty tags and source citations.
12. Output compressed result.

## Pitfalls

- **Skipping forced triggers**: The 3 forced triggers are not optional. Skipping thinking-first → ungrounded output. Skipping caveman → token bloat. Skipping grill-with-docs on gap → ungrounded new skills.
- **Over-routing**: A high match score on a high-risk skill may dominate a low-risk skill with a slightly lower match. The risk penalty handles this; do not skip it.
- **Threshold miscalibration**: 50 is the default; tune based on user feedback. A too-high threshold triggers too many gap-fills (slow); a too-low threshold routes poorly (low quality).
- **INDEX.yaml drift**: If INDEX.yaml is out of sync with `domain/`, routing will miss skills. Builder and Review are responsible for keeping INDEX.yaml current.

## Verification

- Every task must end with either: (a) a Domain skill successfully executed, or (b) grill-with-docs landed + Builder triggered + a new skill generated.
- Every task must have gone through thinking-first (pre) and caveman (post). Skipping either is a bug.
- On gap, grill-with-docs must produce at least one ADR; the new skill must be routable after Builder finishes.
- No task should be silently dropped.
