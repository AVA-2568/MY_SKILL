---
name: retrieve-rag
description: "Retrieve information from personal knowledge sources (notes, docs, wikis, knowledge bases) using RAG-style retrieval. Use when the user asks questions about their personal notes, saved documents, or knowledge base."
user-invocable: true
agent_created: true
category: retrieval
---

# Retrieve-RAG (知识检索)

Retrieve relevant information from personal knowledge sources.

## When to Use

- "What do my notes say about X?"
- "Find the document about Y"
- "Search my knowledge base for Z"

## When Not to Use

- Structured database queries → use retrieve-sql
- Web searches → use web-research

## Procedure

1. Parse the user query to identify key search terms.
2. Search the knowledge base for relevant documents.
3. Rank results by relevance.
4. Present the most relevant information with source references.

## Pitfalls

- Results may be outdated; check document timestamps
- Multiple documents may have conflicting information

## Verification

- Results must include source references
- If no results found, report clearly rather than fabricating
