---
name: retrieve-sql
description: Retrieve information from a SQL database — write and execute SELECT queries, explore schema, and visualize query results. Use when the user asks to query a database, explore table structures, or generate reports from relational data. Triggers: "query the database for X", "what's in the Y table", "run a SELECT to find Z", "show me the schema".
user-invocable: true
risk_level: mid
category: retrieval
---

# Retrieve SQL (检索 SQL)

Retrieve information from a SQL database.

## When to Use

- User asks to query a database
- User wants to explore table structures or relationships
- User asks for a report or data extract from a relational DB

## Procedure (skeleton — Builder will expand)

1. Identify the database connection (connection string, ORM, or existing client)
2. Explore schema: list tables, describe columns, check relationships
3. Construct the SELECT query (use EXPLAIN for complex queries)
4. Execute read-only (never UPDATE/DELETE/DROP without explicit confirmation)
5. Format and present results

## Pitfalls

- NEVER run write operations (INSERT/UPDATE/DELETE/DROP/TRUNCATE) without explicit user confirmation
- Use parameterized queries to prevent SQL injection
- Limit result sets (add LIMIT) for large tables

## Verification

- Only SELECT queries executed (unless write permission explicitly granted)
- Query uses parameterized inputs (no string interpolation)
- Results are complete and correctly formatted
