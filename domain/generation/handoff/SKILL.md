---
name: handoff
description: "Compact the current conversation into a handoff document for another agent to pick up and continue the work. Suggested skills, task summary, artifacts reference, and redacted sensitive info."
argument-hint: "What will the next session be used for?"
user-invocable: true
risk_level: mid
category: generation
source: mattpocock/skills@productivity
agent_created: true
---

# Handoff (任务交接)

Create a handoff document that lets another agent (or a future session of the same agent) pick up the work seamlessly.

## When to Use

- "Write a handoff doc for the next session"
- "Document what's been done so the team can continue"
- End of a session with incomplete work
- "Save context so I don't have to repeat myself next time"

## When Not to Use

- Simple one-off tasks finished in this session → no handoff needed
- Documentation of completed features → use generate-doc instead
- Git commit messages → use execute-git

## Procedure

1. **Scan artifacts** — list all files created or modified in this session: specs, plans, ADRs, issues, commits, diffs. Extract their paths and key conclusions.
2. **Summarize context** — concisely state: what was the task, what decisions were made, what is still in progress, what remains to be done.
3. **Identify suggested skills** — based on the remaining work, list 1-3 skills the next agent should invoke (use MY_SKILL skill names from INDEX.yaml).
4. **Redact sensitive info** — scan for API keys, passwords, tokens, PII, internal URLs, and replace with `<REDACTED>` markers. Note what was redacted and where.
5. **Write the document** — save to the OS temp directory (not the workspace). Use a timestamped filename: `handoff-YYYY-MM-DD-HHmm.md`.
6. **Report** — tell the user the file path and a brief summary of what's in the handoff.

## Output Template

```markdown
# Handoff: <task-name>
- Generated: <timestamp>
- Next focus: <from argument-hint or inferred>

## Task Summary
<2-4 sentence summary of what was done and what's left>

## Decisions Made
- <decision 1>
- <decision 2>

## Artifacts
- <file path>: <one-line description>

## Suggested Skills for Next Session
- `<skill-name>`: <why needed>

## Redactions
- <field>: <reason>

## Open Questions
- <if any>
```

## Pitfalls

- **Sensitive info leakage**: Keys, tokens, passwords in code examples or config files must be redacted. Double-check all file contents before writing.
- **Broken links**: Artifact paths must be absolute or relative-from-repo-root. Relative paths can break when the handoff is read from a different machine.
- **Duplicate content**: Do not re-summarize what's already in artifacts. Reference them by path. The handoff is an index, not a second copy.
- **Vague task summary**: "Finished some work on X" is not helpful. State concrete progress: "Implemented POST /users endpoint (routes + handler + schema), tests pending."

## Verification

- Handoff file exists at the reported path
- No API keys, passwords, or PII in the file (scan the written file)
- Every artifact path references an actually-existing file
- Suggested skills are real MY_SKILL names from INDEX.yaml
- The handoff is self-contained — an agent with no prior context can start working from it