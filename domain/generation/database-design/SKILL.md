---
name: database-design
description: Design a database schema (relational or NoSQL) from a domain model or business requirement. Use when the user wants to model entities, define relationships, choose between SQL/NoSQL, plan indexes, or emit DDL. Triggers: "design the database for X", "create a schema for Y", "model the tables for Z", "normalize the data model".
user-invocable: true
risk_level: low
category: generation
agent_created: true
---

# Database Design (数据库设计)

Design a database schema from a domain model or requirement. Stop at the schema definition (DDL, entity diagrams); query optimization and ORM mappings belong to execution-layer skills.

## When to Use

- User asks for a database schema, entity model, or DDL
- User wants to choose between SQL and NoSQL for a use case
- User wants to normalize a data model
- User wants index recommendations

Do NOT use when the user asks for runnable SQL queries — route to `retrieve-sql` instead.

## Procedure

1. Identify entities, attributes, and relationships from the domain model or requirement.
2. Choose the database paradigm (relational, document, key-value, graph, etc.) with rationale.
3. For relational: normalize to 3NF minimum; define tables, columns, types, constraints, foreign keys.
4. For NoSQL: describe the access patterns that drove the document/collection design.
5. Recommend indexes: which queries are the hot path? What indexes support them?
6. Define migration strategy if there's an existing schema.
7. Output: DDL (SQL) or equivalent schema definition, plus an entity-relationship summary.

## Pitfalls

- Don't create tables for "maybe one day" — design for known access patterns.
- Don't skip index planning; without indexes, the schema is half-done and a performance trap.
- Don't choose NoSQL "because scale" — SQL scales fine for most use cases; choose the paradigm that matches the data shape and query pattern.

## Verification

- Every entity in the domain model maps to a table or collection.
- Referential integrity is enforced (foreign keys for SQL, application-level for NoSQL where appropriate).
- Index recommendations align with stated access patterns.
- Schema supports the queries described in the requirement.
