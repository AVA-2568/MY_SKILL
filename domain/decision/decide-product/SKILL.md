---
name: decide-product
description: "Product decision support — analyze a product decision (feature priority, A/B test result, roadmap trade-off) and produce a structured recommendation. Use when the user asks \"should we build X\", \"which feature has higher priority\", \"is the A/B result conclusive\". Triggers: \"prioritize the roadmap\", \"evaluate feature X\", \"interpret the A/B result\", \"decide between X and Y\"."
user-invocable: true
risk_level: mid
category: decision
---

# Decide Product (产品决策)

Product decision support: structured analysis of a product decision.

## When to Use

- User asks whether to build a feature
- User asks to prioritize the roadmap
- User asks to interpret an A/B test result
- User asks to evaluate a feature proposal

## Procedure (skeleton — Builder will expand)

1. Frame the decision (what's being chosen, what are the alternatives)
2. Identify the criteria (impact, effort, risk, alignment with strategy)
3. Score each alternative on the criteria
4. List the assumptions and how sensitive the recommendation is to them
5. Output: recommendation + sensitivity analysis + open questions

## Pitfalls

- Don't optimize for a single metric; multi-criteria decisions need trade-off reasoning
- Acknowledge unknowns; don't pretend to know things the user hasn't told you
- For A/B test results, distinguish statistical significance from practical significance

## Verification

- All criteria are explicit (not hidden in the recommendation)
- Sensitivity analysis is provided (what would change the recommendation)
- Open questions are listed (what additional data would help)
