---
name: generate-doc
description: Generate a structured document — report, README, proposal, design doc, or template. Use when the user asks for a new document with a specific structure. Triggers: "write a README for X", "draft a proposal for Y", "create a design doc for Z", "generate a report on W".
user-invocable: true
risk_level: low
category: generation
---

# Generate Document (生成文档)

Generate a structured document from a specification.

## When to Use

- User wants a README / proposal / design doc / report
- User wants a template for recurring document types

## Procedure (skeleton — Builder will expand)

1. Identify document type (README / proposal / report / design doc)
2. Identify audience (engineers / execs / customers)
3. Identify length and tone
4. Generate: outline → fill sections → review for consistency
5. Apply the document-type conventions (e.g., RFC 2119 keywords for design docs)

## Pitfalls

- Don't generate an empty skeleton — at least the first 2 sections must be substantive
- For proposals, list alternatives considered before recommending one
- For design docs, the schema/interface must be concrete, not hand-wavy

## Verification

- Document is coherent end-to-end
- All sections requested by the user are present
- No placeholder text ("TODO", "TBD") left behind unless explicitly allowed
