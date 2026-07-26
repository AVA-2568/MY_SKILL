---
name: system-design
description: Design a system or service architecture — decompose a requirement into components, data flows, interfaces, and deployment topology. Use for greenfield system design, architecture review, or technology selection. Triggers: "design the architecture for X", "how should I structure Y", "what's the right tech stack for Z", "review my system design".
user-invocable: true
risk_level: low
category: generation
agent_created: true
---

# System Design (系统设计)

Design a system architecture from a business or technical requirement. Stop at the architecture description; implementation (infrastructure-as-code, CI/CD, service stubs) belongs to execution-layer skills.

## When to Use

- User asks for a system design, architecture, or deployment topology
- User wants to decompose a requirement into services, databases, and message flows
- User wants technology selection with rationale (language, framework, DB, message broker, orchestration)
- User asks "how should I structure X" or "what's the right stack for Y"

Do NOT use when the user asks for runnable infrastructure code — route to `execute-bash`, `docker-devops`, or framework-specific generation skills instead.

## Procedure

1. Frame the problem: what business problem does this system solve? Who are the actors?
2. Identify functional and non-functional requirements (scale, latency, availability, consistency).
3. Propose a logical architecture: components, their responsibilities, and how they communicate (sync vs async).
4. Choose the physical topology: deployment model, scaling strategy, data storage per component.
5. Select technologies: language, framework, database, message broker, with rationale.
6. Describe critical data flows with sequence or flow diagrams (text-based).
7. Call out trade-offs explicitly: what did you reject and why.

## Pitfalls

- Don't over-engineer for hypothetical scale. Design for known needs first; document how to scale later.
- Don't chase "best practice" without context. Every architectural choice is a trade-off — name the trade-off.
- Don't prescribe implementation details (exact class names, file structure) — leave that to generation skills.

## Verification

- Every component has a clear single responsibility.
- Data flows are traceable end-to-end (no magic hops).
- At least one explicit trade-off is documented.
- Technology choices have rationale.
