---
name: retrieve-sql
description: Generate and execute a SQL query against a relational database. Use when the user asks a data question best answered by SQL. Triggers: "how many users signed up last week", "show me the top 10 customers by revenue", "what's the average X by Y".
user-invocable: true
risk_level: mid
category: retrieval
---

# Retrieve SQL (SQL 检索)

Generate and execute a SQL query against a relational database.

## When to Use

- User asks a data question best answered by SQL
- User asks for an aggregate, a join, or a specific slice of data

## Procedure (skeleton — Builder will expand)

1. Identify the database and connection
2. Inspect the schema (table list, column types, indexes)
3. Draft the query
4. Dry-run (EXPLAIN) for performance sanity
5. Execute
6. Return rows + interpretation

## Pitfalls

- For destructive queries (DROP / DELETE / UPDATE), require explicit user confirmation
- For large result sets, paginate or aggregate before returning
- For ambiguous schema (similar column names across tables), ask the user

## Verification

- Query returns the expected columns
- Row count is sane (not zero when it shouldn't be, not millions when it shouldn't be)
- Execution time is reasonable (under 5s for typical queries)
