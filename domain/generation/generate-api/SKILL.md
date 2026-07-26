---
name: generate-api
description: Generate a REST/GraphQL API endpoint from a specification. Use when the user wants to add a new API endpoint, scaffold a CRUD resource, or generate a service stub. Triggers: "create an API endpoint for X", "add a CRUD for X", "scaffold the resource", "generate a service for X".
user-invocable: true
risk_level: low
category: generation
---

# Generate API (生成 API)

Generate a backend API endpoint from a specification.

## When to Use

- User wants to add a new API endpoint
- User asks to scaffold a CRUD resource
- User wants a service stub

## Procedure (skeleton — Builder will expand)

1. Identify framework (Express, FastAPI, Spring, etc.)
2. Identify data model (entity, fields, relationships)
3. Identify operations (CRUD / custom actions)
4. Generate: route definitions + handler functions + request/response schemas
5. Generate: validation + error handling
6. Generate: tests

## Pitfalls

- Don't skip auth/authz if the resource is sensitive
- Match the existing project's naming and style conventions
- For multi-step generation, generate one piece at a time so the user can review

## Verification

- Generated endpoint handles all requested operations
- Validation rejects invalid input with clear error messages
- Tests cover happy path + common error cases
