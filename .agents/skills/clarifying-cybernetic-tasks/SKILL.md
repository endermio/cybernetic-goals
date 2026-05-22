---
name: clarifying-cybernetic-tasks
description: 'Use before writing a Codex /goal, implementation plan, or code for complex or ambiguous work. Clarifies human intent, domain concepts, product behavior, permissions, data model choices, verification criteria, non-goals, and stop conditions. Do not downscope requirements merely because implementation seems hard. Ask only high-value human questions, record obvious defaults as assumptions, defer execution details to planning, and create a clarification brief under docs/superpowers/clarifications/ when file writing is available.'
---

# Clarifying Cybernetic Tasks

## Overview

Turn a fuzzy human intention into an approved task understanding before it becomes a Codex `/goal`, implementation plan, or code change.

This skill is a pre-goal control loop:

```text
human purpose -> AI context scan -> ambiguity map -> human decisions -> approved assumptions -> goal-ready task brief
```

This skill clarifies requirements and product semantics. It does not write final `/goal` commands, does not create final goal files, and does not start implementation.

Output:

- a concise clarification response in chat, or
- a clarification brief at `docs/superpowers/clarifications/YYYY-MM-DD-<slug>.md`.

Use `assets/clarification-brief-template.md` for the file structure.

## Core Rules

### Clarify Requirements, Do Not Downscope Them

Do not reduce, simplify, postpone, or replace the requested behavior merely because implementation seems complex, risky, unstable, or hard.

Implementation complexity may be recorded as execution risk, planning concern, verification concern, or future implementation challenge. It must not become the recommended product default unless the human explicitly asks for a lower-risk scope.

### Ask Only High-Value Human Questions

Ask the human a question only if all are true:

1. The answer materially changes product semantics, data model, permission model, public API, acceptance criteria, or user-visible behavior.
2. There are at least two plausible business choices.
3. The correct answer cannot be safely inferred from the user request, existing docs, or common product conventions.
4. A wrong default would be costly to reverse or would cause serious misalignment.

Do not ask the human about routine execution tactics, obvious resilience behavior, or implementation mechanics.

### Use Decision Levels

Classify uncertainty as:

- Level 1: Blocking Human Decision
- Level 2: Default Assumption
- Level 3: Deferred Execution / Planning Detail

Only Level 1 items should become questions.

## Process

1. Inspect just enough context to ask non-generic questions.
2. Restate the human purpose in product language.
3. Build a control map: objective, controlled object, sensors, actuators, constraints, disturbances, stop conditions.
4. Identify and classify decisions by level.
5. Ask 3-7 high-value questions, preferably no more than 5.
6. Create or update the clarification brief.
7. If the human answers, update `Confirmed Decisions From Human` and the `Clarification Status`.
8. Do not create a goal, plan, control review, or runtime `/goal` command.

## Clarification Status

The brief must include:

```text
Status: `Incomplete` or `Complete`
```

Mark `Complete` only when:

- all blocking human decisions are resolved;
- confirmed decisions are recorded;
- remaining assumptions are low-risk and explicit;
- the next step can safely create a goal contract.

## Output Format

If a brief was created or updated:

```markdown
Created or updated clarification brief:

`docs/superpowers/clarifications/YYYY-MM-DD-slug.md`

Clarification summary:
- ...

Blocking human decisions:
| Decision | Recommended default | Risk if wrong |
|---|---|---|
| ... | ... | ... |

Default assumptions:
- ...

Deferred to planning:
- ...

Questions:
1. ...
2. ...
3. ...

Next action:
Reply with one of:
- `按默认继续`
- answers to the questions
- revised scope
- cancel/postpone
```

If all blocking decisions are resolved:

```markdown
Clarification is complete.

Updated clarification brief:
`docs/superpowers/clarifications/YYYY-MM-DD-slug.md`

Ready for:
`$writing-cybernetic-goals`
```

## Validation Checklist

- [ ] Requirement semantics are separated from implementation planning.
- [ ] The response did not downscope because implementation is hard.
- [ ] Uncertainty is classified into blocking decisions, default assumptions, and deferred details.
- [ ] Obvious defaults are not asked as blocking questions.
- [ ] There are no more than 7 questions.
- [ ] The brief includes `Clarification Status`.
- [ ] No goal, plan, or runtime `/goal` was created.
