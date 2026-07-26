---
name: comprehend-doc
description: Read and summarize a document (PDF, markdown, text, web article) — extract key points, claims, action items, and intent. Use when the user shares a document and asks for a summary, key takeaways, or analysis. Triggers: "summarize this", "what are the key points", "extract action items", "what does this document say".
user-invocable: true
risk_level: low
category: understanding
---

# Comprehend Document (理解文档)

Read a document and produce a structured summary.

## When to Use

- User shares a document and asks for summary
- User asks for key points, claims, or action items
- User asks "what does this document say"

## Procedure (skeleton — Builder will expand)

1. Identify document type and length
2. Read fully (chunked if needed for long docs)
3. Extract: thesis / key points / supporting evidence / action items
4. Output: structured summary (length adapts to user request)

## Pitfalls

- For very long documents, ask the user what aspect to focus on
- Don't paraphrase claims that look like quotes; quote them directly
- Distinguish author's claims from cited claims

## Verification

- Summary covers the document's main thesis
- Key action items (if any) listed explicitly
- Length proportional to user request (default: concise)
