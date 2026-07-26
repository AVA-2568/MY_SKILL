# Domain: Five LLM Capabilities

The domain layer is classified by **LLM capability graph** into 5 categories:

| Category | Meaning | Example skills |
|---|---|---|
| **Understanding** | Read input, parse context, recognize intent | `comprehend-code`, `comprehend-doc` |
| **Generation** | Produce output: code, documents, interface contracts, architecture, schemas, visual specifications | `generate-api`, `generate-doc`, `api-design`, `system-design`, `database-design`, `ui-design`, `ux-design` |
| **Retrieval** | Find information, query data, call APIs (incl. analysis) | `retrieve-rag`, `retrieve-sql` |
| **Execution** | Run commands, manipulate files, invoke tools | `execute-bash`, `execute-git` |
| **Decision** | Plan, choose, weigh tradeoffs (incl. analysis) | `decide-invest`, `decide-product` |

**Status**: accepted
**Considered Options**:
- A. 4 categories (Understanding / Generation / Analysis / Decision) — oversimplified
- B. 5 categories (Understanding / Generation / Retrieval / Execution / Decision) (adopted)
- C. 6 categories (+ Analysis as a separate category)
- D. 9 categories (preserve workbuddy's existing classification)
**Why B**: An LLM-native (capability-oriented) classification aligns better with what LLMs actually need during tasks than a task-oriented (what-humans-do) view. The 5 categories balance granularity and cognitive load; "Analysis" is intentionally merged into Retrieval and Decision to avoid redundancy. Governance (lifecycle management) belongs to Review (horizontal), not to Domain — this is a clean separation of concerns under the 4V+1H topology.