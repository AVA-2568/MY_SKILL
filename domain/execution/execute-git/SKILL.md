---
name: execute-git
description: Execute git operations — status, diff, commit, branch, merge, rebase, push, pull. Use when the user asks to interact with a git repository. Triggers: "commit my changes", "create a branch for X", "merge Y into Z", "show me the diff", "push to origin".
user-invocable: true
risk_level: mid
category: execution
---

# Execute Git (执行 Git)

Execute git operations.

## When to Use

- User asks to commit, branch, merge, rebase, push, pull
- User asks to inspect git state (status, diff, log)
- User asks to set up a worktree or stash

## Procedure (skeleton — Builder will expand)

1. Verify git repo and current branch
2. Check working tree state (clean vs dirty)
3. Construct the git command
4. For destructive ops (force-push, reset --hard, branch -D): require explicit user confirmation
5. Execute
6. Report

## Pitfalls

- `git push --force` to a shared branch: NEVER do this silently
- `git reset --hard` / `git checkout --` / `git clean -fd`: all destructive; require confirmation
- For merge conflicts, surface them; don't auto-resolve

## Verification

- Git state after operation matches user's intent
- No silent data loss
- For commits: verify the message and the diff before pushing
