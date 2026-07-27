---
name: comprehend-code
description: "Understand and explain code — language detection, entry points, data flow, dependencies, and intent. Use when the user wants to understand code, review code logic, or get an architectural overview."
user-invocable: true
agent_created: true
category: understanding
---

# Comprehend-Code (代码理解)

Read, understand, and explain code with structured output.

## When to Use

- "Read this Python file and explain the class hierarchy"
- "What does this function do?"
- "Give me an overview of this codebase"
- "Explain the architecture of this project"
- "What design patterns are used in this code?"

## When Not to Use

- Document understanding (specs, contracts, manuals) → use comprehend-doc
- Debugging specific errors → use debugging skill
- Quick code formatting questions → not needed

## Procedure

1. **Identify context** — detect programming language, framework, runtime, file type.
2. **Find entry points** — locate `main()`, handlers, route registrations, or script entry points.
3. **Map data structures** — identify key types, interfaces, classes, and their relationships.
4. **Trace data flow** — follow input → processing → output through the code paths.
5. **Map dependencies** — list external packages, imports, API calls, databases.
6. **Synthesize intent** — explain what the code is designed to do, not just what it does line by line.

## Pitfalls

- **Cross-language misjudgment**: Do not assume the same patterns apply across languages (e.g., Python duck typing vs Java interfaces). Always state the language first.
- **Excessive nesting expansion**: Stop at 3 levels deep unless the user specifically asks for deeper detail. Full call tree expansion drowns signal in noise.
- **Framework-specific assumptions**: Do not infer framework conventions without seeing imports/configuration. A `@app.route()` might be Flask, FastAPI, or a custom decorator.
- **Missing external context**: Code that reads files, queries DBs, or calls APIs depends on external state. Always flag what is unknown about the environment.

## Verification

- **Test case 1 — single file**: Read a Python class with inheritance (`class B(A)`) → output must mention `B` extends `A`, list methods, and identify the MRO implication.
- **Test case 2 — multi-file entry**: Read a project with `src/main.ts` + `src/routes/` + `src/models/` → output must identify main.ts as entry point, describe route-model separation, and infer framework from `package.json` or imports.
- **Test case 3 — dependency detection**: Read a Go file that imports `"database/sql"` and `"github.com/lib/pq"` → output must list both stdlib and third-party deps separately, flag that lib/pq is a PostgreSQL driver.
- Every output must state the language and framework at the top, before any detail.

## Output Template

```markdown
## Overview
- Language: <language>
- Framework: <framework or "none detected">
- File type: <single file / multi-file project>

## Entry Points
- <path>: <role (main/handler/script)>

## Key Structures
- <type/class>: <role>

## Data Flow
1. <input source> → <processing step> → <output destination>

## Dependencies
- <package>: <purpose>

## Intent
<1-3 sentence statement of what the code is designed to achieve>
```

This template is the minimum output structure. For deeper analysis, expand each section as needed.