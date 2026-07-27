---
name: execute-bash
description: "Execute shell commands, scripts, and automation tasks in the Bash environment. Use when the user needs to run commands, scripts, file operations, or system automation."
user-invocable: true
agent_created: true
category: execution
---

# Execute-Bash (Shell 执行)

Run shell commands, scripts, and automation in the Bash environment.

## When to Use

- "Run this command"
- "Create a script to..."
- "Automate this task"

## When Not to Use

- Git operations → use execute-git
- Complex multi-step pipelines → prefer chaining with &&

## Procedure

1. Understand the desired outcome.
2. Construct a safe, idempotent command.
3. Run the command; capture output.
4. Verify the expected result.

## Pitfalls

- Destructive commands require user confirmation
- Long-running processes should use background mode
- File paths with spaces must be quoted

## Verification

- Command must complete with exit code 0
- Output must match expected format
- Clean up temporary files if created
