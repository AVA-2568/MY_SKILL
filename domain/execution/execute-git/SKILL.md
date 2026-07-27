---
name: execute-git
description: "Git operations — commit, push, branch, merge, and git workflow management. Use when the user needs git actions or version control operations. Related user-level skill: git-workflow (workflow conventions)."
user-invocable: true
agent_created: true
category: execution
related: [git-workflow]
---

# Execute-Git (Git 操作)

Perform git operations with safety checks.

## When to Use

- "Commit my changes"
- "Push to remote"
- "Create a branch"
- "Merge feature into main"
- "Undo the last commit"

## When Not to Use

- Interactive rebase (`git rebase -i`) → ask user for explicit step-by-step instructions; do not automate
- Git bisect → requires manual guidance; stub and ask user to run commands
- Submodule operations (`git submodule`) → stub: ask user for explicit intent
- Reflog recovery → surface reflog entries but let the user pick the target

## Procedure

1. **Status check** — run `git status` and `git diff --stat` to understand the current state.
2. **Plan** — describe the intended operation to the user (especially if destructive: reset, force-push, rebase). Wait for confirmation.
3. **Pre-operation safety**:
   - For merge: do a `git merge --no-commit --no-ff <branch>` dry-run first; if conflicts, report them.
   - For push: show `git diff --stat` and let the user review before pushing.
   - For destructive operations: show the full command, explain the impact, wait for explicit "yes".
4. **Execute** — run the git operation.
5. **Verify** — run `git log --oneline -3`, `git status`, and optionally `git diff --stat` to confirm the result.

## Pitfalls

- **Destructive commands list** (all require explicit approval before execution):
  - `git reset --hard` / `git reset --mixed`
  - `git push --force` / `git push --force-with-lease`
  - `git rebase` (interactive or not)
  - `git checkout -- <file>` (discard changes)
  - `git branch -D` (force-delete branch)
- **Skipping pre-commit hooks**: Never use `--no-verify`. If a hook fails, diagnose and fix the issue.
- **No diff review before commit**: Always show the diff to the user before committing, unless they explicitly waived review.
- **Merge without dry-run**: Merging without `--no-commit --no-ff` dry-run can leave a dirty working tree.

## Verification

- After the operation: `git status` shows a clean working tree matching the expected outcome
- `git log --oneline -3` shows the expected commit on the expected branch
- For push operations: local HEAD === remote HEAD (verify via `git rev-parse HEAD && git ls-remote origin HEAD`)
- For merge operations: the merge commit appears in `git log` and the feature branch's commits are reachable

## Output Template

When reporting the result of a git operation, use a compact summary:

```
Status: <clean/dirty>
Branch: <current>
Last commit: <hash> <message>
Remote: <in-sync/behind N/ahead N>
```