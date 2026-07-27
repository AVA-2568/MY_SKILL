---
name: decide-product
description: "Product decision advisor — weigh tradeoffs between features, priorities, or product strategies. Use when the user faces product decisions, feature prioritization, or strategic product choices."
user-invocable: true
agent_created: true
category: decision
---

# Decide-Product (产品决策)

Weigh tradeoffs between product options and provide a structured recommendation.

## When to Use

- "Which feature should we build first?"
- "Should we invest in performance or new features?"
- "Which market segment should we target?"

## When Not to Use

- Technical architecture decisions → use system-design
- Investment decisions → use decide-invest

## Procedure

1. Clarify the decision context: timeframe, constraints, success criteria.
2. List 2-4 viable options.
3. Score each option against success criteria.
4. Recommend with rationale.

## Output Template

```markdown
## Decision: [Option Name]
- Rationale: ...
- Tradeoffs accepted: ...
- Risk: ...
```
