---
name: distributor
description: Route user tasks to the most appropriate skill via description matching plus risk scoring; detect skill gaps and trigger Builder. Always-active; the entry point of every task. Use when the user submits any task — even if they don't explicitly ask for routing.
user-invocable: false
risk_level: low
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

All four (thinking-first / caveman / grill-with-docs; Review runs separately) are `user-invocable: false`; they cannot be /slash-called directly by the user. Distributor injects them into context at the forced trigger points.