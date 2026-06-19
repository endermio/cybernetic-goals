---
name: framing-cybernetic-intent
description: 'Use when cybernetic routing is requested but user input is pre-task intent or role-ambiguous context: confusion, dissatisfaction, risk sense, observed symptoms, failed attempts, method preference, process distrust, source material, declared current state, or unclear requested transformation.'
---

# Framing Cybernetic Intent

## Overview

Use this before workflow routing when the input is not yet a formed task.

```text
human situation -> input role binding -> collaborative intent framing -> Shared Intent Understanding -> optional task candidate
```

This skill is not a router, requirements analyzer, planner, reviewer, or
executor. Detailed examples live in
`references/intent-framing-detailed-rules.md`.

## Core Rule

Bind input roles before treating anything as the task.

Protect these distinctions:

- method preference is not purpose;
- source material is not automatically the primary object;
- declared current state is not automatically a new investigation;
- current implementation is not the primary object of a future feasibility
  inquiry unless the user asks for current-state audit;
- confusion, dissatisfaction, risk sense, failed experience, and process
  distrust are pre-task inputs until shared intent is clear.

Do not turn source material into the task unless the user explicitly asks to
act on it as the primary object.

Do not turn a declared completed finding into a new investigation unless the
user asks to verify it.

Do not treat current implementation as the primary object of a feasibility inquiry unless the user asks for current-state audit.

## Input Role Binding

At minimum identify:

- human purpose;
- method preference;
- source material;
- declared current state;
- requested transformation;
- primary object;
- reference object;
- non-goals;
- uncertainty to reduce.

Ask one concise role-binding question only when roles conflict or the primary
object is ambiguous.

## Process

1. Reflect the human situation in neutral language.
2. Bind input roles.
3. State what should not be assumed yet.
4. Ask at most one high-value question if intent is unstable.
5. Summarize Shared Intent Understanding once clear enough.
6. Offer a response-only next move.

The loop ends at shared understanding, not artifact production.

## Default Output

Use the chat-only shape from `references/intent-framing-detailed-rules.md`.
It starts with:

```text
Shared Intent Understanding
- Human situation:
- Input role binding:
  - Source material:
  - Declared current state:
  - Requested transformation:
  - Primary object:
  - Reference object:
  - Method preference:
  - Non-goals:
```

Possible next moves:

- continue intent framing;
- make a judgment or decision;
- design a small experiment;
- perform a bounded inspection;
- hand off to `$routing-cybernetic-workflows`;
- hand off to `$analyzing-cybernetic-requirements`;
- stop because purpose is not stable.

## Optional Task Formation

Only include a task candidate after shared intent is clear. If the next step is
routing, keep the handoff response-only:

```text
$routing-cybernetic-workflows <clear task statement>
```

Do not write this command into requirements, design, goal, plan, review,
progress, or orchestration artifacts.

## Persistence

Default to no file write. Persist an intent brief only when the user asks or the
same shared intent must guide future approved files.

Use `assets/intent-frame-template.md`. The intent brief must not contain
complete requirements, solution design, execution policy, control review, or
runtime goal content.

## Common Mistakes

- Treating "use this workflow" as the user's goal.
- Treating source material as the task object.
- Treating declared completed findings as a new investigation request.
- Treating artifact creation as evidence that intent is clear.
