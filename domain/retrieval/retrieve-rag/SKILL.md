---
name: retrieve-rag
description: Retrieve information from a RAG (Retrieval-Augmented Generation) knowledge base — vector stores, document collections, or indexed wikis. Use when the user asks to query a knowledge base, find relevant documents, or search through indexed content. Triggers: "search the knowledge base for X", "what does the documentation say about Y", "find documents related to Z".
user-invocable: true
risk_level: low
category: retrieval
---

# Retrieve RAG (检索 RAG)

Retrieve information from a RAG knowledge base.

## When to Use

- User asks to query a knowledge base or document store
- User wants to find relevant documents in an indexed collection
- User asks "what does the docs/wiki/knowledge base say about X"

## Procedure (skeleton — Builder will expand)

1. Identify the knowledge base and its access method (API, local index, etc.)
2. Construct the query (natural language or structured)
3. Retrieve top-k results
4. Filter and rank by relevance
5. Synthesize answer from retrieved chunks, citing sources

## Pitfalls

- Don't fabricate results; if nothing relevant is found, say so
- Cite the source chunk, not just the document name
- Respect the retrieval limit — don't claim exhaustive search if only top-k were retrieved

## Verification

- Retrieved chunks are directly relevant to the query
- Sources are cited (document + chunk location)
- Confidence is stated (how much of the answer comes from retrieval vs. model knowledge)
