---
name: decide-invest
description: Investment decision support — analyze a potential investment (stock, fund, project) and produce a structured recommendation. Use when the user asks "should I invest in X" or "is Y a good buy". Triggers: "analyze this stock", "should I buy X", "is Y overvalued", "compare Z with W".
user-invocable: true
risk_level: mid
category: decision
---

# Decide Invest (投资决策)

Investment decision support: structured analysis of a potential investment.

## When to Use

- User asks whether to invest in X
- User asks to compare two or more investments
- User asks "is X a good buy"

## Procedure (skeleton — Builder will expand)

1. Identify the investment type (stock, fund, project, etc.)
2. Gather data: fundamentals, technicals, sentiment, macro context
3. Apply valuation framework (PE/PB/DCF/etc.)
4. List risks and counter-arguments
5. Output: recommendation + confidence + key uncertainties

## Pitfalls

- This skill is **decision support, not advice** — clearly state the user is responsible for the final call
- Don't fabricate data; if a data point is unavailable, say so
- Acknowledge the limits of the model (LLMs are not financial advisors)

## Verification

- All claims are sourced (data point + source)
- Recommendation is explicit (buy / hold / sell / pass) with confidence level
- Counter-arguments are listed, not just the bull case
