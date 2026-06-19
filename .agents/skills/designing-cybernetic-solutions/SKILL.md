---
name: designing-cybernetic-solutions
description: 'Use when requirements analysis exists but the required answer path, support model, inside/outside choices, flows, interfaces, lifecycle, failure model, evidence model, or output structure is not explicit enough for goal writing or execution policy.'
---

# Designing Cybernetic Solutions

## Overview

Create the solution model needed between approved requirements and goal writing.

This skill owns design strategy, not requirement meaning, execution policy,
review, runtime compilation, or target execution.

Official persistent control facts are JSON only. Historical Markdown may be read
as background, but must not become official control input.

Detailed rules live in `references/solution-design-detailed-rules.md`.
Use `references/design-check.md` for the design trigger rubric.

## Hot Path

1. Read approved `requirements.control.json`.
2. Confirm `What the User Approved` is Approved when `controlled_run` work is
   involved.
3. Identify the model gap: objects, roles, relationships, information flow,
   authority, lifecycle, failure model, evidence model, or output structure.
4. Produce `design.control.json` only for the model needed downstream.
5. Preserve requirement meaning exactly. If design would change the approved
   target, return to requirements.
6. Mark tactical choices as tactical; do not freeze them as meaning rules unless
   requirements approved them.

## Required Sections

The design artifact should include:

- source requirements and requirements path;
- design status;
- objects/actors/roles;
- relationships and flows;
- inside/outside boundary;
- interfaces or contracts;
- lifecycle and failure model;
- evidence model;
- required answer path support;
- final answer format design when output structure matters;
- open questions or blocked decisions.

## Required Answer Path Check

If requirements say how the task must be answered, design must preserve that
answer path. It must not replace required implementation, measurement, repair,
or diagnosis with a framework, readiness, compatibility, or classification-only
answer because that is easier.

## Output Format

Output the design path and status:

```text
Created or updated design:
`docs/cybernetics/runs/<slug>/design.control.json`

Design status:
- `approved` / `candidate` / `blocked`

Key design decisions:
- ...

Open questions:
- ...

Response-only next step:
- return to `$orchestrating-cybernetic-pregoal`, or
- if manual fallback is being used, continue to `$writing-cybernetic-goals`.
```

Do not write runtime `/goal` prompts or target-work commands into the design
artifact.

## Validation Checklist

- [ ] Design consumes approved requirements.
- [ ] Requirement meaning was not changed.
- [ ] Required answer path is preserved.
- [ ] Solution model is explicit enough for goal and execution policy.
- [ ] Output structure is designed only when required.
- [ ] Open human decisions are not hidden as tactical defaults.
- [ ] No target work was executed.
