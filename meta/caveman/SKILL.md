---
name: caveman
description: Constrain verbosity — pre-think (limit thinking to 3-5 short points before acting) + post-output (compress residual verbosity from final outputs). Force-triggered by Distributor at two points: pre-route (constrains thinking) and post-route (compresses output). Not user-invocable; part of the horizontal layer.
user-invocable: false
risk_level: low
category: meta
agent_created: true
---

# Caveman (穴居人)

Constrain AI verbosity at two trigger points: pre-think and post-output.

## When This Triggers

Distributor triggers Caveman at two points:
1. **Pre-think** (before the AI begins reasoning): constrains the thinking block to ≤5 short, concrete points.
2. **Post-output** (after the AI has produced its final response): compresses residual verbosity.

This is NOT post-hoc compression only — it affects the AI's thought process itself.

## Pre-think Procedure

Before the AI reasons about the task, enforce:

1. Think in 3-5 short points maximum. No paragraphs.
2. Each point must be one concrete action or decision.
3. Skip "context setting" and "background" in thinking.
4. If you need more than 5 points, you're overthinking — pick the top 5.

## Post-output Procedure

After the AI produces its output, compress residual verbosity:

1. Cut any sentences that restate what's already obvious.
2. Remove conversational filler ("let me explain", "as you can see", "it's worth noting").
3. Replace multi-sentence explanations with one crisp sentence where possible.
4. Keep all factual content and actionable information intact.
5. Delete entire paragraphs that add no new information.

## Pitfalls

- Don't compress so aggressively that the output loses meaning or correctness.
- Pre-think must not prevent the AI from doing necessary analysis — 5 points is a guardrail, not a straitjacket.
- Post-output must not remove qualifiers ("might", "likely", "estimated") that affect accuracy.

## Verification

- Pre-think: thinking block has ≤5 points (count them).
- Post-output: output contains no conversational filler phrases.
- All factual claims from the original output are preserved.
