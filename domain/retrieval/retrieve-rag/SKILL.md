---
name: retrieve-rag
description: Retrieval-Augmented Generation over a local knowledge base. Use when the user asks a question that requires grounding in their documents, notes, or local files. Triggers: "search my notes for X", "what do my docs say about Y", "find references to Z in my knowledge base".
user-invocable: true
risk_level: low
category: retrieval
---

# Retrieve RAG (检索增强)

RAG query over the user's local knowledge base.

## When to Use

- User asks a question that requires their documents
- User asks "what do my notes say about X"
- User asks to find references across a corpus

## Procedure (skeleton — Builder will expand)

1. Identify the knowledge base (path / index location)
2. Embed the user's query
3. Retrieve top-k relevant chunks
4. Optionally re-rank
5. Synthesize an answer with citations

## Pitfalls

- Don't retrieve without first checking the index is current
- Cite source paths/sections for every claim
- If retrieved context is empty, say so explicitly — don't hallucinate

## Verification

- Answer is grounded in retrieved chunks
- Citations are accurate (point to actual source paths)
- Confidence is calibrated (low confidence → say "I don't know")
