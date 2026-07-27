---
name: generate-api
description: "Generate API implementations from contracts — route definitions, handler skeletons, request/response schemas, and error types. Use when the user asks to implement an API endpoint or service with a framework, after an API contract already exists from api-design."
user-invocable: true
agent_created: true
category: generation
---

# Generate-API (API 实现生成)

Generate API implementations (route handlers, schemas, errors) from a pre-existing contract.

## When to Use

- "Generate an Express.js endpoint for creating a user"
- "Implement the API from the OpenAPI spec"
- "Create route handlers for the user service"
- "Build a RESTful API from the api-design contract"

## When Not to Use

- Designing the API contract (endpoints, methods, data model) → route to api-design first
- Designing the database schema behind the API → route to database-design
- Full-stack scaffolding without a contract → route to api-design first, then return here

## Procedure

0. **Prerequisite check** — verify an API contract exists (from api-design skill output). If not, route to api-design first and stop. Do not generate implementation without a contract.
1. **Parse the contract** — extract endpoints, HTTP methods, path parameters, request/response schemas from the api-design output or OpenAPI spec.
2. **Generate route definitions** — map each endpoint to a route registration file (e.g., `routes/users.ts`).
3. **Generate handler skeletons** — create handler functions for each route, with typed parameters.
4. **Generate schema types** — create request/response TypeScript interfaces or type definitions, derived from the contract.
5. **Generate error types** — create custom error classes or error response types for documented error codes.

## Pitfalls

- **Skipping prerequisite check**: Generating implementation without a contract produces disconnected code. Always run step 0 first.
- **Framework mismatch**: Use the framework the user specified (Express, Fastify, Nest, etc.). Do not assume. If unspecified, ask.
- **Over-generating**: Generate only what the contract specifies. Do not add endpoints, fields, or error codes not in the contract.
- **Hardcoded routes**: Route paths must match the contract exactly, including URL parameter names.

## Verification

- Every endpoint in the contract has a corresponding route definition and handler
- Every request/response schema in the contract has a corresponding type definition
- Route paths are identical to the contract (no renamed params)
- Error types exist for every documented error status code in the contract

## Output Template

```typescript
// routes/<resource>.ts — Route registration
router.<method>('/<path>/:<param>', handler.<handlerName>);

// handlers/<resource>.ts — Handler implementation
export async function <handlerName>(
  req: Request<<Params>, <Response>>,
  res: Response<<Response>>
): Promise<void> { ... }

// schemas/<resource>.ts — Request/response types
export interface <RequestType> { ... }
export interface <ResponseType> { ... }

// errors/<resource>.ts — Error types
export class <ErrorName> extends HttpError {
  statusCode = <code>;
}
```

For non-TypeScript targets, adapt the template to the language's type system (e.g., Go structs, Python dataclasses, Java records).