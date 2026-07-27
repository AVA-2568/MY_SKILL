---
name: {{ skill_name }}
description: "{{ one_sentence_what + ' Use when ' + trigger_phrases }}"
user-invocable: true
risk_level: {{ risk_level }}
agent_created: true
category: {{ capability }}
---

# {{ Title Case Name }}

{{ paragraph_summary }}

## When to Use

- {{ trigger_1 }}
- {{ trigger_2 }}
- {{ trigger_3 }}

## When Not to Use

- {{ boundary_1 }}

## Procedure

1. {{ step_1 }} — check: {{ completion_criterion_1 }}
2. {{ step_2 }} — check: {{ completion_criterion_2 }}
3. {{ step_3 }} — check: {{ completion_criterion_3 }}

## Pitfalls

- {{ pitfall_1 }}
- {{ pitfall_2 }}
- {{ pitfall_3 }}

## Verification

- {{ verify_1 }}
- {{ verify_2 }}
- {{ verify_3 }}

## Output Template

```markdown
# {{ output_title }}
...
```
