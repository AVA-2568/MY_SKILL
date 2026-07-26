---
name: execute-bash
description: Execute a bash command on the local or remote shell. Use when the user asks to run a shell command, script, or batch operation. Triggers: "run X", "execute Y", "shell into Z and do W".
user-invocable: true
risk_level: mid
category: execution
---

# Execute Bash (执行 Bash)

Execute a bash command.

## When to Use

- User asks to run a command
- User asks to execute a script
- User asks for a batch file operation

## Procedure (skeleton — Builder will expand)

1. Identify the working directory and environment
2. Construct the command (avoid destructive operations without confirmation)
3. Execute
4. Capture stdout / stderr / exit code
5. Report

## Pitfalls

- Destructive operations (`rm -rf`, `dd`, `> critical-file`): require explicit user confirmation
- Long-running commands: respect timeout, suggest background
- Commands with secrets: never echo credentials; use env vars or stdin

## Verification

- Exit code is 0 (or expected non-zero)
- Output matches user's intent
- No silent failures
