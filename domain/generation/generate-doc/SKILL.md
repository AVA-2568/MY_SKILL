---
name: generate-doc
description: Generate technical documentation — API docs, READMEs, architecture overviews, onboarding guides — from code or intent. Use when the user asks to document a codebase, explain an architecture, or generate a reference from source. Triggers: "write docs for X", "generate API documentation", "document the architecture", "create a README".
user-invocable: true
risk_level: low
category: generation
---

# Generate Doc (生成文档)

Generate technical documentation.

## When to Use

- User asks to document a codebase or module
- User wants auto-generated API reference docs
- User asks to write an architecture overview or onboarding guide

## Procedure (skeleton — Builder will expand)

1. Identify the scope (single file, module, whole codebase)
2. Determine the target audience and doc type (reference, guide, overview)
3. Extract structure from code (exports, types, public API surface)
4. Generate organized documentation with examples
5. Cross-link related documents

## Pitfalls

- Don't regenerate docs that are already up to date (check git diff)
- Avoid excessive detail — prioritize the "why" and "how to use" over "how it works"
- Don't document implementation details that are clear from reading the code

## Verification

- All public APIs are documented
- Examples are runnable and correct
- Links between documents are valid
