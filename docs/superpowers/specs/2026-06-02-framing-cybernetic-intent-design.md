# Design: framing-cybernetic-intent

## Status

Status: `Draft for user review`

## Purpose

The cybernetic skill chain currently assumes its input is already a task that can
be routed, analyzed, designed, compiled, and executed. Real user input often
arrives earlier than that: confusion, dissatisfaction, intuition, risk sense,
observed symptoms, failed attempts, method preference, or distrust of the
current process.

This design adds a pre-task skill, `framing-cybernetic-intent`, whose job is to
help the user and agent form a shared understanding of intent before any
workflow is selected.

## Core Claim

The missing layer is not stronger routing or larger requirements analysis. The
missing layer is collaborative intent framing:

```text
human situation
-> framing-cybernetic-intent
-> shared intent understanding
-> optional task formation
-> routing-cybernetic-workflows
-> requirements analysis
-> solution design
-> goal
-> execution policy
-> review
-> runtime
```

The skill must prevent premature taskification. It should not optimize for
creating artifacts, selecting workflows, or producing task candidates before the
human purpose is clear.

## Scope

Create a new independent skill:

```text
.agents/skills/framing-cybernetic-intent/
```

The skill is used before `routing-cybernetic-workflows` when the user input is
not clearly an already formed task, or when the user appears to name a method,
workflow, or skill as if it were the goal.

## Non-Goals

The skill must not:

- analyze full requirements semantics;
- write requirements, design, goal, execution policy, review, progress, or
  runtime goal artifacts by default;
- decide workflow fit;
- treat a user-selected method as the human purpose;
- force every vague input into a task candidate;
- turn emotional or experiential input into an execution objective without
  shared understanding;
- create persistent artifacts for routine clarification.

## Trigger Model

Trigger the skill when input looks like pre-task intent rather than a formed
task. Examples:

- confusion: "I do not know what is wrong here";
- dissatisfaction: "This workflow feels wrong";
- intuition: "I think this is overcontrolled";
- risk sense: "This might explode context";
- observed symptoms: "The agent keeps producing plans";
- failure experience: "Last time this did not converge";
- method preference: "Use the full cybernetic workflow";
- process distrust: "I do not trust the current pipeline".

Do not trigger it for a clearly formed low-risk task such as "run the unit
tests" or "fix this failing local assertion" unless the user also expresses
unclear intent, process distrust, or method-goal confusion.

## Process

The skill uses a short collaborative loop:

1. Reflect the apparent human situation without converting it into a task.
2. Separate purpose, method, symptom, constraint, risk, and uncertainty.
3. Identify the uncertainty the user seems to want reduced.
4. State what should not be assumed yet.
5. Ask at most one high-value question when the intent is still ambiguous.
6. When enough shared understanding exists, summarize it.
7. Offer possible next moves without treating any one move as mandatory.

The loop ends when the conversation has a `Shared Intent Understanding`, not
when an artifact has been produced.

## Default Output

The default output is chat-only:

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

The next move can be one of:

- continue intent framing;
- make a judgment or decision;
- design a small experiment;
- perform a bounded inspection;
- hand off to `routing-cybernetic-workflows`;
- hand off to `analyzing-cybernetic-requirements`;
- stop because the user purpose is not yet stable.

## Optional Task Formation

Only after shared intent is clear may the skill include an optional task
candidate. The task candidate is a downstream handoff, not the default output.

```text
Optional Task Candidate
- Task statement:
- Why this task follows from the shared intent:
- Known non-goals:
- Recommended handoff:
```

If the next step is routing, the handoff should be response-only:

```text
$routing-cybernetic-workflows <clear task statement>
```

## Persistence Rule

Use hybrid persistence.

Do not write files by default. Write an intent brief only when one of these is
true:

- the intent frame will affect long-lived control artifacts;
- the same unresolved intent is likely to recur;
- the user asks to record the framing;
- future routing or requirements analysis needs a stable record of the shared
  intent.

When persistence is needed, write:

```text
docs/cybernetics/intents/YYYY-MM-DD-<slug>.md
```

The intent brief should preserve only the shared understanding and optional
handoff. It should not contain full requirements, design, plans, reviews, or
runtime goals.

## Skill Contents

The implementation should add:

- `SKILL.md`;
- `agents/openai.yaml`;
- `assets/intent-frame-template.md`;
- `evals/evals.json`.

No scripts are required for the first version. The behavior is primarily
conversational and semantic.

## Integration Changes

Update the top-level workflow documentation so the chain starts with human
situation and intent framing:

```text
human situation
-> intent framing
-> task candidate, when appropriate
-> routing
```

Update `routing-cybernetic-workflows` to clarify that it routes tasks. It should
not take responsibility for collaborative intent framing. When it receives
pre-task input, it should hand off to `framing-cybernetic-intent` instead of
forcing a workflow decision.

Update `analyzing-cybernetic-requirements` to clarify that it analyzes a formed
task's requirement semantics. It should not become responsible for deciding
whether the user was only expressing dissatisfaction, risk sense, or method
preference.

Update the invariant matrix with an intent invariant.

Suggested invariant:

```text
INV-INT-001: Pre-task intent must be collaboratively framed before workflow
routing when user input is not yet a formed task or when method is being treated
as goal.
```

## Evaluation Coverage

Add eval cases that require the skill to:

- distinguish "use the full workflow" as method preference, not purpose;
- avoid turning dissatisfaction into an execution task;
- avoid turning failure experience into an immediate repair goal;
- ask a small clarifying question when intent is unstable;
- produce shared intent understanding before optional task formation;
- hand off to routing only after the task is clear;
- avoid writing files in ordinary chat-only framing;
- write an intent brief only when persistence is justified or requested.

## Testing Strategy

Use lightweight regression tests for repository invariants:

- README mentions the pre-task layer before routing;
- the new skill exists with required metadata;
- eval ids cover method-goal confusion, dissatisfaction, failure experience,
  and chat-only default behavior;
- invariant matrix includes `INV-INT-001`;
- router text names `framing-cybernetic-intent` as the handoff for pre-task
  input.

These tests should avoid semantic overreach. The skill's conversation quality is
better covered by evals than by deterministic unit tests.

## Rollout

Implement in one bounded change:

1. Add the new skill and template.
2. Add evals.
3. Update README, router, requirements-analysis boundary text, and invariant
   matrix.
4. Add focused tests for structural coverage.
5. Run the full unit suite.

If `MANIFEST.txt` is used as a release manifest, include the new skill files in
the same change. Avoid unrelated manifest cleanup.

## Self-Review

- No incomplete requirements remain.
- The design keeps intent framing independent from routing and requirements
  analysis.
- The default output is shared understanding, not task creation.
- Persistence is hybrid and bounded to avoid artifact explosion.
- Implementation scope is small enough for one follow-up plan.
