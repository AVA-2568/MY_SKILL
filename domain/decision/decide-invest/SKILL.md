---
name: decide-invest
description: "Investment decision advisor — evaluate a potential investment, produce buy/hold/sell direction with confidence level and key uncertainties. Use when the user asks about investing decisions, stock picks, or portfolio allocation."
user-invocable: true
agent_created: true
category: decision
---

# Decide-Invest (投资决策)

Evaluate a potential investment opportunity and produce a directional recommendation.

## When to Use

- "Should I invest in X?"
- "What do you think about buying Y?"
- "Is this a good time to enter Z?"
- "Analyze this stock for a potential entry"

## When Not to Use

- Quick price checks → use westockdata
- Portfolio rebalancing → use portfolio-management
- **Financial advice**: This skill provides directional analysis only, not personalized investment advice. Do not claim it replaces a licensed financial advisor.
- **Specific price targets**: Output buy/hold/sell direction only. Do not produce specific buy/sell price levels unless the user explicitly requests and you have supporting data.

## Data Source Priority

1. **westock-data** (primary) — real-time/fundamental/technical data for A-share, HK, US markets
2. **Official sources** (secondary) — company filings, exchange announcements, regulatory disclosures
3. **Third-party research** (fallback) — reputable financial media, analyst reports; must cite source name, authority rating, and timeliness

All data must be sourced. Unverified claims must be tagged as "unverified" or "speculative."

## Procedure

1. **Identify the asset** — confirm the ticker/symbol and market. Use westockdata for profile data.
2. **Gather fundamentals** — P/E, P/B, revenue growth, debt ratio, dividend yield from westockdata.
3. **Gather technicals** — recent price trend, key support/resistance levels, volume patterns.
4. **Gather recent news** — check for catalysts, earnings reports, regulatory events.
5. **Identify 3-5 key factors** — the most impactful drivers for this investment thesis (not a generic list).
6. **Assess upside vs downside** — weigh positive catalysts against risks. Note data confidence level per factor.
7. **Produce recommendation** — buy/hold/sell with confidence (high/medium/low) and a concise rationale.

## Pitfalls

- **Recency bias**: Recent news may dominate the analysis. Balance with longer-term fundamentals.
- **Data staleness**: Financial data can be hours/days old. Flag timeliness in the output (e.g., "PE ratio as of Q3 filing").
- **False precision**: An estimated fair value of $47.32 implies accuracy that doesn't exist. Use ranges ($45-50) instead.
- **Missing risk factors**: At minimum, flag market risk, sector risk, and company-specific risk. If data is unavailable for any, say so.

## Verification

- Recommendation includes direction (buy/hold/sell) and confidence level (high/medium/low)
- At least 3 key factors identified, each with a source or confidence tag
- All data sourced; unverified claims marked "speculative"
- Output includes a disclaimer: this is directional analysis, not financial advice

## Output Template

```markdown
## Recommendation
- **Direction**: <buy/hold/sell>
- **Confidence**: <high/medium/low>
- **Rationale**: <1-2 sentence summary>

## 3 Key Factors
1. <Factor 1 — source> [confidence: high/medium/low]
2. <Factor 2 — source> [confidence: ...]
3. <Factor 3 — source> [confidence: ...]

## Key Uncertainties
1. <What could change the thesis>
2. <Risk factor with low visibility>
3. <External dependency>

## Risks
- Market: <risk>
- Sector: <risk>
- Company-specific: <risk>

> ⚠️ This is directional analysis, not financial advice.
```