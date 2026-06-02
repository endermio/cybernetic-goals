---
name: framing-cybernetic-intent
description: 'Use before cybernetic workflow routing when user input is pre-task intent rather than a formed task: confusion, dissatisfaction, intuition, risk sense, observed symptoms, failed attempts, method preference, or distrust of the current process. Collaboratively frames human intent into shared understanding before optional task formation. Does not analyze requirements, choose workflow fit, write control artifacts, or execute target work.'
---

# Framing Cybernetic Intent

## Overview

Help the user and agent form shared intent understanding before the cybernetic
workflow treats anything as a task.

This skill handles the pre-task layer:

```text
human situation
-> collaborative intent framing
-> shared intent understanding
-> optional task formation
-> routing-cybernetic-workflows
```

It is not a router, requirements analyzer, planner, reviewer, or executor.

## Core Boundary

This skill must not:

- analyze full requirements semantics;
- decide workflow fit;
- treat a user-selected method, skill, workflow, or tool as the human purpose;
- turn confusion, dissatisfaction, risk sense, failed experience, or process
  distrust directly into an execution task;
- force every vague input into a task candidate;
- write requirements, solution designs, goal contracts, execution policies,
  control reviews, progress logs, or runtime `/goal` commands;
- create persistent artifacts for routine clarification.

This skill may:

- reflect the user's situation without prematurely taskifying it;
- separate purpose, method, symptom, constraint, risk, uncertainty, and failure
  experience;
- identify what uncertainty the user appears to want reduced;
- state what should not be assumed yet;
- ask one high-value question when intent is unstable;
- summarize shared intent understanding;
- optionally form a task candidate only after the shared intent is clear;
- optionally write an intent brief when persistence is justified or requested.

## Trigger Signals

Use this skill when the input is not yet a formed task. Common signals:

- confusion: "I do not know what is wrong";
- dissatisfaction: "This workflow feels wrong";
- intuition: "This seems overcontrolled";
- risk sense: "This may explode context";
- observed symptoms: "The agent keeps writing plans";
- failure experience: "Last time this did not converge";
- method preference: "Use the full cybernetic workflow";
- process distrust: "I do not trust the current pipeline".

Do not use this skill for clearly formed low-risk tasks unless the user also
expresses unclear intent, process distrust, or method-goal confusion.

## Process

1. Reflect the human situation in neutral language.
2. Separate purpose, method, symptom, constraint, risk, and uncertainty.
3. Identify the uncertainty the user seems to want reduced.
4. State what should not be assumed yet.
5. Ask at most one high-value question when the intent is still unstable.
6. Summarize shared intent understanding once it is clear enough.
7. Offer possible next moves without treating any one move as mandatory.

Ask concise questions. Do not interview the user for routine execution details.
The loop ends at shared understanding, not at artifact production.

## Default Output

Use this chat-only shape by default:

```text
Shared Intent Understanding
- Human situation:
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

- the intent frame will affect long-lived control artifacts;
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
- Responding to dissatisfaction by creating a repair goal.
- Responding to failed experience by rerunning the same workflow.
- Producing requirements before clarifying what the user wants changed.
- Treating artifact creation as evidence that intent is clear.
