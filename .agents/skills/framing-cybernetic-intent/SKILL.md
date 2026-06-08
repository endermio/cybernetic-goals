---
name: framing-cybernetic-intent
description: 'Use when cybernetic routing is requested but user input is pre-task intent or role-ambiguous context: confusion, dissatisfaction, risk sense, observed symptoms, failed attempts, method preference, process distrust, source material, declared current state, or unclear requested transformation.'
---

# Framing Cybernetic Intent

## Overview

Help the user and agent form shared intent understanding before the cybernetic
workflow treats anything as a task.

This skill handles the pre-task layer:

```text
human situation
-> input role binding
-> collaborative intent framing
-> shared intent understanding
-> optional task formation
-> routing-cybernetic-workflows
```

It is not a router, requirements analyzer, planner, reviewer, or executor.

## What This Skill Owns

This skill owns input role binding and collaborative intent framing before
workflow routing.

Owned framing:

- reflect the user's situation without prematurely taskifying it;
- bind input roles before suggesting a next move;
- separate purpose, method, source material, declared current state, requested
  transformation, primary object, reference object, non-goal, risk,
  uncertainty, and failure experience;
- identify what uncertainty the user appears to want reduced;
- state what should not be assumed yet;
- ask one high-value question when intent is unstable;
- summarize shared intent understanding;
- optionally form a task candidate only after the shared intent is clear;
- optionally write an intent brief when persistence is justified or requested.

Routed elsewhere:

- requirements meaning go to `$analyzing-cybernetic-requirements`;
- workflow fit goes to `$routing-cybernetic-workflows`;
- solution design, goal contracts, execution policies, control reviews,
  progress logs, and runtime `/goal` commands belong to their downstream skills;
- routine clarification stays in chat unless persistence is justified.

Protect these bindings during framing:

- user-selected methods, skills, workflows, and tools are method preferences;
- source material, reference context, and declared current state need an explicit
  requested transformation before becoming the primary task object;
- confusion, dissatisfaction, risk sense, failed experience, and process distrust
  are pre-task inputs until shared intent is clear.

## Trigger Signals

Use this skill when the input is not yet a formed task. Common signals:

- confusion: "I do not know what is wrong";
- dissatisfaction: "This workflow feels wrong";
- intuition: "This seems overcontrolled";
- risk sense: "This may explode context";
- observed symptoms: "The agent keeps writing plans";
- failure experience: "Last time this did not converge";
- method preference: "Use the full cybernetic workflow";
- process distrust: "I do not trust the current pipeline";
- completed findings: "I already finished the investigation; turn these
  findings into a repair plan";
- feasibility framing: "Use the current system as baseline, but investigate
  future implementation boundaries".

Do not use this skill for clearly formed low-risk tasks unless the user also
expresses unclear intent, process distrust, or method-goal confusion.

## Input Role Binding

Before suggesting any next move, classify the user's input into roles:

- Human purpose: what the user ultimately wants changed.
- Method preference: what method, skill, workflow, or tool the user suggests.
- Source material: material, lists, code, conclusions, logs, observations, or
  prior findings provided as input.
- Declared current state: what the user says is already complete or currently
  true.
- Requested transformation: what the user wants the source material changed
  into, such as findings to repair framing or baseline plus target capability
  to feasibility boundaries.
- Primary object: the real object to analyze, design, repair, judge, or decide.
- Reference object: evidence, baseline, constraint, context, or comparison
  material that should not become the task object by default.
- Non-goals: what should not be done.
- Uncertainty to reduce: the current uncertainty that matters most.

Do not turn source material into the task unless the user explicitly asks to
act on it as the primary object.

Do not turn a declared completed finding into a new investigation unless the
user asks to verify it.

Do not treat current implementation as the primary object of a feasibility inquiry unless the user asks for current-state audit.

Do not treat method preference as purpose.

Ask one concise role-binding question only when roles conflict or the primary
object is ambiguous, for example:

```text
Do you want these findings verified, or turned into a repair/convergence task?
```

```text
Does "capability limit" mean current system state, or future technical
implementation limit?
```

## Process

1. Reflect the human situation in neutral language.
2. Bind input roles before treating any part of the input as the task object.
3. Separate purpose, method, source material, declared state, requested
   transformation, primary object, reference object, non-goals, risk, and
   uncertainty.
4. Identify the uncertainty the user seems to want reduced.
5. State what should not be assumed yet.
6. Ask at most one high-value role-binding or intent question when the intent
   is still unstable.
7. Summarize shared intent understanding once it is clear enough.
8. Offer possible next moves without treating any one move as mandatory.

Ask concise questions. Do not interview the user for routine execution details.
The loop ends at shared understanding, not at artifact production.

## Default Output

Use this chat-only shape by default:

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
- Apparent purpose:
- Method vs purpose distinction:
- Symptoms or failure experience:
- Risk or uncertainty to reduce:
- What not to assume yet:
- Current best next move:
```

Allowed next moves include:

- continue intent framing;
- make a judgment or decision;
- design a small experiment;
- perform a bounded inspection;
- hand off to `$routing-cybernetic-workflows`;
- hand off to `$analyzing-cybernetic-requirements`;
- stop because the user purpose is not yet stable.

## Optional Task Formation

Only include a task candidate after shared intent is clear.

```text
Optional Task Candidate
- Task statement:
- Why this task follows from the shared intent:
- Known non-goals:
- Recommended handoff:
```

If the next step is routing, keep the handoff response-only:

```text
$routing-cybernetic-workflows <clear task statement>
```

Do not write this command into requirements, design, goal, plan, review,
progress, or orchestration artifacts.

## Persistence Rule

Default to no file write.

Write an intent brief only when one of these is true:

- the intent frame will affect long-lived approved files;
- the same unresolved intent is likely to recur;
- the user asks to record the framing;
- future routing or requirements analysis needs a stable record of the shared
  intent.

When persistence is justified, use:

```text
docs/cybernetics/intents/YYYY-MM-DD-<slug>.md
```

Use `assets/intent-frame-template.md`.

The intent brief preserves shared understanding and optional handoff only. It
must not contain full requirements, solution design, execution policy, control
review, or runtime goal content.

## Common Mistakes

- Treating "use this workflow" as the user's goal.
- Treating source material as the task object.
- Treating declared completed findings as a new investigation request.
- Treating current implementation as the primary object of a future feasibility
  inquiry.
- Responding to dissatisfaction by creating a repair goal.
- Responding to failed experience by rerunning the same workflow.
- Producing requirements before clarifying what the user wants changed.
- Treating artifact creation as evidence that intent is clear.
