---
name: api-design
description: Design a REST or GraphQL API contract before any code is written. Use when the user wants to define resources, endpoints, request/response schemas, auth, pagination, errors, idempotency, rate limits, versioning, or emit an OpenAPI/GraphQL SDL artifact. Triggers: "design an API for X", "draft an OpenAPI spec for Y", "define the resource model and endpoints", "spec the REST contract for Z", "model the API surface for W", "write the GraphQL schema".
user-invocable: true
risk_level: low
category: generation
agent_created: true
---

# API Design (API 契约设计)

Design — do not implement — an API contract from a business requirement. Stop at the contract boundary; framework code (routes, handlers, ORM) belongs to `generate-api`.

## When to Use

- User asks for an API contract, OpenAPI document, or GraphQL schema
- User wants resource modeling, endpoint surface, or request/response shapes pinned down
- User wants explicit auth/authz, pagination, errors, idempotency, rate-limit, or versioning policy
- A team needs a shared contract before frontend, backend, or integration work splits

Do NOT use when the user asks for runnable framework code (route handlers, controllers, ORM mappings) — route to `generate-api` instead.

## Procedure

1. Extract actors, resources, and operations from the requirement; classify each action as read, write, or admin.
2. Model resources: noun, identifier strategy (UUID vs. autoincrement), fields with types, required/optional flags, relationships.
3. Choose style — REST + OpenAPI 3.1, GraphQL SDL, or hybrid — and record the rationale in the output.
4. Define endpoints: method + path + auth scope; plural nouns for REST, domain-grouped types/queries for GraphQL.
5. Specify request schema (body, query, path, headers) and response schema (success + error envelope) with field-level constraints and examples.
6. Define auth/authz: scheme (Bearer/JWT/API key/OAuth2), scopes per endpoint, token lifecycle.
7. Define pagination (cursor/offset), rate limits, idempotency keys, and versioning strategy.
8. Define error envelope: code + message + details; standard HTTP status codes mapped to application errors.
9. Output: structured API contract with all of the above.

## Verification

- Every endpoint maps to a concrete business operation
- Every resource has an identifier strategy, fields with types, and required/optional flags
- Error states are specified, not just the happy path
- Auth/authz is explicit per endpoint, not a single "Authentication: Bearer" placeholder