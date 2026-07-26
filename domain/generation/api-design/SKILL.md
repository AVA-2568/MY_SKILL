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
6. Define auth/authz: scheme (Bearer/JWT/API key/OAuth2), scopes/roles per endpoint, ownership rules, multi-tenant boundaries.
7. Specify cross-cutting behavior: pagination (cursor or offset + max page size), filtering/sorting, idempotency keys (POST/PATCH/DELETE), rate-limit headers + 429 + Retry-After, versioning strategy (URI / header / sunset).
8. Specify the error model: stable code, human message, field path, trace id; map to HTTP status or GraphQL `extensions.code`.
9. Emit the contract artifact — OpenAPI 3.1 YAML or GraphQL SDL — with inline examples; resolve all `$ref`s.
10. Run the verification checklist; surface unresolved assumptions in an "Open Questions" block.

## Output Template

```
# <Service Name> API Contract
Style: REST (OpenAPI 3.1) | GraphQL SDL
Auth: <scheme + scopes>

## Resources
- <Resource>: id, <field:type>, ...; relations: [<other>]
## Endpoints
- <METHOD> <path> — <purpose> — auth: <scope>
## Schemas
- <Request|Response name>: fields + types + required + constraints
## Cross-cutting
- pagination: cursor | offset, default_limit, max_limit
- idempotency: <header + ttl + replay behavior>
- rate limit: <budget per actor + 429 shape + Retry-After>
- versioning: <URI | header | sunset policy>
## Errors
- <code>: <http/status> — <when> — <client fix hint>
## OpenAPI / SDL
<artifact body, fully expanded>
## Open Questions
- <assumption the user must confirm>
```

## Pitfalls

- Don't fabricate field types — mark anything unspecified as `unknown` and surface it in Open Questions.
- Don't pick REST vs. GraphQL silently — the choice reshapes data fetching; ask if ambiguous.
- Don't skip the error model — every endpoint must declare at least 401/403/404/422 (or GraphQL equivalents).
- Don't bleed into code generation — stop at the contract; implementation routes to `generate-api`.
- Don't leave `$ref`s unexpanded or pagination/auth unspecified for collection endpoints.

## Verification

- [ ] Every resource has explicit id strategy and typed fields
- [ ] Every endpoint declares auth scope plus success and error responses
- [ ] Pagination, idempotency, rate-limit, and versioning policies present and concrete
- [ ] Error model covers 4xx + 5xx with stable codes and trace id
- [ ] OpenAPI/SDL lints clean (no `$ref` cycles, no unresolved paths)
- [ ] Open Questions lists every assumption the user must confirm

## Example

Requirement: "Let customers place and cancel orders, and view their order history."
→ Style REST/OpenAPI 3.1; auth Bearer+JWT; resource `Order{id:uuid, customer_id, items[], status:enum, total:cents}`; define create, cancel, and cursor-paginated history operations; require `Idempotency-Key` for order creation; cap pages at 100; rate limit 60 req/min/user with `429` + `Retry-After`; errors `401/403/404/409/422/429` with envelope `{code,message,trace_id}`; version with URI `/v1` and sunset header; surface assumptions: "tax handling", "refund flow", "archive versus permanent deletion".
