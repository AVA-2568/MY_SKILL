---
name: comprehend-code
description: Read and explain a code file's structure, behavior, dependencies, and intent. Use when the user pastes code and asks "what does this do", or asks for an explanation of a function, class, or module. Triggers: "explain this code", "what does this function do", "trace the logic", "summarize the file".
user-invocable: true
risk_level: low
category: understanding
---

# Comprehend Code (理解代码)

Read a code file and produce a structured explanation.

## When to Use

- User pastes code and asks for an explanation
- User asks what a function/class/module does
- User asks to trace logic, summarize, or compare

## Procedure (skeleton — Builder will expand)

1. Identify the language and framework
2. Identify entry points (top-level functions, exports, main)
3. Trace data flow
4. Identify dependencies (imports, library calls)
5. Output: structure / behavior / dependencies / intent

## Pitfalls

- Don't guess intent from names alone — read the actual logic
- For large files, focus on the entry point and the user's specific question
- If code is incomplete, ask before explaining

## Verification

- Explanation covers all user-asked questions
- Major dependencies identified
- Any uncertainty explicitly flagged
