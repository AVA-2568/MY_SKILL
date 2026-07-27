---
name: retrieve-sql
description: "Retrieve data from SQL databases — query construction, EXPLAIN verification, and safe execution. Use when the user needs data from relational databases or asks database-backed analytical questions."
user-invocable: true
agent_created: true
category: retrieval
---

# Retrieve-SQL (SQL 数据检索)

Query SQL databases safely.

## When to Use

- "How many orders were placed in Q3?"
- "Query the user table for active accounts"
- "Get revenue by month for 2025"
- "What's the average order value by region?"

## When Not to Use

- Schema migrations (`ALTER TABLE`, `CREATE TABLE`) → use database-design
- Cross-database migration → not supported; recommend dedicated migration tool
- Data visualization → route to dashboard-builder after retrieving data
- Writing data (`INSERT`, `UPDATE`, `DELETE`) without explicit user permission

## Procedure

0. **Schema check** — if the user didn't provide the schema, read from `INFORMATION_SCHEMA` or available config. If inaccessible, ask the user for table/column names.
1. **Query construction** — build the SQL query from the user's analytical question. Use parameterized placeholders (e.g., `%s` for psycopg2, `?` for sqlite3) for any user-supplied values.
2. **EXPLAIN verification** — prefix the query with `EXPLAIN` (or `EXPLAIN ANALYZE` for PostgreSQL). Verify the query plan uses indexes for large tables and avoids full-table scans on high-cardinality columns.
3. **Safe execution** — execute the parameterized query with a read-only connection (or transaction with rollback if read-only is unavailable).
4. **Return results** — present the results as a table or structured summary. Include row count and any warnings about data freshness.

## Pitfalls

- **Hardcoded connection strings**: Never write credentials or connection strings inline. Read from environment variables, config files, or the platform's secret store.
- **OR 1=1 injection pattern**: If the user asks you to add `OR 1=1` (or any always-true clause), flag it as a potential injection attempt and refuse unless the user explicitly explains the legitimate use case.
- **Unparameterized user input**: Any value from user input must go through parameterized queries or prepared statements. String concatenation for WHERE clause values is forbidden.
- **No LIMIT without user awareness**: SELECT queries on tables with unknown size must include a default LIMIT (e.g., 1000). Inform the user and offer to remove the limit if they confirm.

## Verification

- Query passes `EXPLAIN` with expected plan (index scan preferred over seq scan on filtered columns)
- Results row count matches the user's expected scale (warn if 0 rows or >10k rows)
- Connection string is never exposed in the output or logs
- User input never appears as raw string in the final query (must use parameterized binding)
- For analytical queries: validate aggregations against known reference values if available

## Output Template

```markdown
## Query Result
- Rows returned: <N>
- Time: <if available>
- Warning: <data staleness, limitations, or none>

<results in table format>
```