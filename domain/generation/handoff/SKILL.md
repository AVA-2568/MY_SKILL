---
name: handoff
description: Create a structured handoff document to transfer context between sessions, agents, or people. Use when you've completed a complex task and need to save state for the next session, or you're wrapping up work someone else will continue. Triggers: "create a handoff", "save my progress", "write a summary for the next session", "prepare a checkpoint", "I'm done for now but someone else will pick this up".
disable-model-invocation: true
risk_level: low
category: generation
source: mattpocock/skills@productivity
---

# Handoff (会话交接)

> Forked from `mattpocock/skills@productivity` — see [ADR-0007](../../../docs/adr/0007-mvp-minimum-viable.md) for inclusion rationale.

Create a structured handoff document to transfer context between sessions.

## When to use

Use this skill when:
- You've completed a complex task and the next session needs to continue
- You're wrapping up work that another person or agent will continue
- You want to checkpoint progress before a long break

## Procedure

### 1. Summarize what was done

Briefly describe what was accomplished in this session.

### 2. Surface key files and data

List the files that were created or modified, with brief descriptions of what changed.

### 3. Document remaining work

List what still needs to be done, in priority order.

### 4. Record decisions and open questions

Note any decisions made and questions that remain unresolved.
