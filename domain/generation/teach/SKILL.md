---
name: teach
description: Create comprehensive learning materials — tutorials, guides, courses, cheatsheets — to teach a concept, skill, or process. Use when the user wants to explain something to others (or themselves) in a structured, pedagogical way with spaced-repetition notes. Triggers: "teach me X", "create a tutorial on Y", "explain Z to a beginner", "make a course about W", "write a cheatsheet for V".
disable-model-invocation: true
risk_level: low
category: generation
source: mattpocock/skills@productivity
---

# Teach (教学)

> Forked from `mattpocock/skills@productivity` — see [ADR-0007](../../../docs/adr/0007-mvp-minimum-viable.md) for inclusion rationale.

Create comprehensive learning materials to teach a concept, skill, or process.

## When to use

Use this skill when:
- A user wants to learn a new technical concept
- A team member needs onboarding material
- You want to document knowledge in a reusable format
- A user says "teach me X"

## Procedure

Follow these steps in order. You may skip parts of the process (like not creating a glossary) if the user explicitly tells you to, but the default is to follow every step.

### 1. Create a mission for the learning session

Help the user create a mission for the session, so that they know what the scope of the material is. Take a look at the `MISSION-FORMAT.md` file and fill it in for the session. If they already have a mission, ask them to copy it from the `MISSION-FORMAT.md` file.

### 2. Create an initial glossary of terms

Search through the records for any existing glossaries and build on them. If there are none, start a new one. This is the glossary for this learning session. Use `GLOSSARY-FORMAT.md` for the format.

### 3. Find appropriate resources

Ascertain what the user already knows about this topic. Then, decide on the best resources to teach them, considering:

- Your own knowledge of the topic.
- The web (use `WebSearch` or similar tools to find tutorials, articles, videos).
- The user's existing knowledge base (check their files, notes, projects for relevant context).

Document these resources, what they contain, and how to use them using `RESOURCES-FORMAT.md`.

### 4. Create a lesson plan

Create a lesson plan that is structured to teach the user the concept over time. Covering:

- Spaced repetition and retrieval practice prompts
- Active learning exercises
- Bite-sized, incremental steps

Write this plan into `LEARNING-RECORD-FORMAT.md`.

### 5. Execute the lesson

Walk the user through the lesson plan, asking them to complete the exercises.

### 6. Update the learning records

After the session, update the learning records with:

- What was covered
- What was learned
- What exercises were completed
- What needs review in future sessions

### 7. Keep the glossary updated

After each session, update the glossary with any new terms introduced.
