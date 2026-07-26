---
name: generate-api
description: Generate runnable API code (routes, handlers, middleware, controllers) in a target framework (Express, FastAPI, etc.) from a design contract (OpenAPI, GraphQL schema, or natural language). Use when the user has a design ready and wants implementation code — typically after `api-design` or `database-design`. Triggers: "build the API from this spec", "implement the endpoints from the OpenAPI doc", "generate the route handlers", "convert the design to code".
user-invocable: true
risk_level: low
category: generation
---

# Generate API (生成 API)

Generate runnable API code from a design contract.

## When to Use

- User has a design (OpenAPI, GraphQL schema, resource model) and wants implementation
- User asks to scaffold a new API endpoint or route
- User wants automatic handler generation from a spec

Do NOT use for designing the API contract itself — route to `api-design` instead.

## Procedure (skeleton — Builder will expand)

1. Identify the target framework and language from context
2. Parse the design contract (OpenAPI / GraphQL SDL / natural language)
3. Generate route registration and handler skeletons
4. Generate request validation (from schema constraints)
5. Generate error handling (standard envelope)
6. Output: ready-to-run code files

## Pitfalls

- Don't generate business logic; only scaffold structure
- Respect framework conventions (middleware ordering, error handling patterns)
- Don't reinvent auth — use framework-standard auth middleware

## Verification

- Every endpoint from the design is implemented
- Request validation matches schema constraints (types, required fields)
- Error responses follow the design contract's envelope format
