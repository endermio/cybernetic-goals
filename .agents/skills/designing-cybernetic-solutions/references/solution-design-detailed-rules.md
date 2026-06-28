# Detailed Rules Snapshot


# Designing Cybernetic Solutions

## Overview

Instantiate the approved required answer path from confirmed requirements control JSON, then derive the support model needed for goal writing and execution policy.

This skill resolves the `required design` by turning:

```text
requirements analysis -> required answer path instance -> what supports each required step -> goal-ready design artifact
```

The design expresses the required answer path and the controllable support structure needed for later approved JSON control files. It must stay in the core cybernetic vocabulary and avoid importing adapter-specific terms.

Official persistent control facts are JSON only. Historical Markdown may be read as non-authoritative background, but do not create or compile Markdown as official guard, compiler, runtime, or long-term dual-path control input.

Output:

```text
docs/cybernetics/runs/<slug>/design.control.json
```

Use the approved design control JSON shape for the run directory. Do not use Markdown templates as official control input.

## Core Limit

This skill owns required answer path instantiation and what supports each required step after requirement meaning are formed.

Owned design:

- inspect completed requirements control JSON and relevant source artifacts;
- ask a small number of high-value design questions when solution structure cannot be safely inferred;
- create or update `design.control.json`;
- design complex output/report/schema/artifact-bundle structures when Final Answer Format Check requires structure synthesis;
- record open design questions and stop before approval;
- recommend a route-appropriate response-only handoff when the design is sufficient.

Routed elsewhere:

- unresolved requirement meaning return to `$analyzing-cybernetic-requirements`;
- goal control JSON goes to `$writing-cybernetic-goals`;
- execution policies go to `$writing-cybernetic-execution-policies`;
- whole-chain review goes to `$reviewing-cybernetic-control-structures`;
- runtime `/goal` compilation goes to `$compiling-cybernetic-runtime-goals`;
- target work starts only after an approved runtime `/goal`.

Keep the core support model neutral. Adapter-specific terms appear only when
they are part of the confirmed domain.

## Required Input

Use a completed requirements control JSON file, usually:

```text
docs/cybernetics/runs/<slug>/requirements.control.json
```

The design path must use the same run directory unless the user explicitly requests another path:

```text
docs/cybernetics/runs/<slug>/design.control.json
```

If the requirements analysis is missing, incomplete, or has open blocking human decisions, stop and return to `$analyzing-cybernetic-requirements`.

For `controlled_run` JSON pre-goal work, do not proceed unless the requirements analysis contains `What the User Approved: Approved`, or the current user message explicitly approves the compact control commitment. `ordinary_direct_work` and `bounded_runtime` design work do not require What the User Approved unless the requirements analysis records it as required.

If the current user message approves the compact control commitment, update the requirements analysis `What the User Approved` section first, quoting or referencing that approval, then continue. Do not rely on in-memory approval to pass orchestration or runtime guards.

For `controlled_run` requirements with schema `1.1.0+`, design may start only after `approved_control.information_sufficiency_check` is complete: status is `satisfied` or explicitly reviewed `not_required`; blocking facts have run-local `evidence_ref` values; `counterexample_review` is independent, approved, and covers the facts and transformations into design/plan. If this gate is absent, pending, missing evidence, or not independently reviewed, stop and route to `RunInformationSufficiencyCheck` / `$analyzing-cybernetic-requirements` before creating `design.control.json`.

## Optional Infrastructure

Use `$superpowers:brainstorming` only when the design space is exploratory or the user explicitly asks for design exploration.

Do not require brainstorming for a small required design where the requirements analysis or existing specs already fix the core structure. Record brainstorming workflow status in the design:

- `Not required`
- `Used`
- `Blocked`

## required design

required design is required when the goal is clear but the required answer path or support model is not.

Typical signals:

- multiple reasonable solution structures exist;
- controlled objects, actors, roles, or relationships are unclear;
- system/process inside/outside choices are unclear;
- information flow, state flow, evidence flow, or decision flow is unclear;
- interfaces, contracts, procedures, or user interactions are unclear;
- a new abstraction must be introduced;
- an old concept must be replaced without letting old realization details define the requirement;
- several subsystems or roles must coordinate around one model;
- runtime execution would otherwise invent objects, inside/outside choices, evidence checks, or flow.

required design is usually not required for:

- small local fixes;
- existing approved design or detailed spec;
- bounded audits with an explicit rubric and report shape;
- copy/style/local bug changes;
- obvious execution paths with no new solution structure.

See `references/design-check.md` for compact routing guidance.

## Final Answer Format Design

When the requirements analysis marks `Final Answer Format Check: required`, inspect whether the output need is simple or requires structure synthesis.

If the requirements already define a safe simple output shape, preserve it and avoid expanding the design.

If the output requires a table, matrix, schema, evidence index, structured report, artifact bundle, multi-audience split, or machine-readable shape, the design must define:

- output audience and purpose;
- output medium and destination;
- required sections, fields, tables, schemas, or artifact bundle parts;
- evidence-reference rules;
- detail-level split;
- acceptance condition;
- how the output structure maps to goal and execution-policy implications.

Do not leave runtime execution to invent the final output shape. Do not define output shape in the response-only handoff; put the design-owned structure in the design artifact.

## Required Answer Path Check

Design must be required answer path first. The first design-owned product is the required answer path instance; support objects, mechanisms, relationships, flows, and evidence model are derived from that answer path.

For `controlled_run` JSON pre-goal work, the design must preserve the approved way the task should be answered from What the User Approved.

When What the User Approved records `How this should be answered` or `What is not enough`, the design must include `## Required Answer Path Check` and record:

- approved way this should be answered;
- instantiated answer path;
- required steps coverage;
- whether the what is not enough was avoided.

The design must not replace the approved answer path with a weaker answer because it is easier to execute or verify. If the approved way this should be answered is insufficient, infeasible, or unsuitable, stop and return to `$analyzing-cybernetic-requirements` for What the User Approved revision instead of substituting another answer path.

Do not use predefined task categories or internal method registries to fill in the required answer path. Derive required steps only from the approved user meaning, explicit not-enough answers, domain facts already in source material, and design reasoning recorded in this artifact.

## Required Sections

The design artifact must include:

1. Design Status
2. Source Contracts
3. Human Purpose
4. Confirmed Meaning
5. Design Workflow
6. Required Answer Path Check, when What the User Approved records how this should be answered or what is not enough
7. Required Answer Path
8. What Supports Each Required Step
9. Design Details Tied To Required Steps
10. Final Answer Format Design, when Final Answer Format Check requires structure synthesis
11. Design-to-Goal Mapping
12. Design-to-Execution Mapping
13. Open Design Questions
14. Design Review Requirements

## Design Status

Use one of:

- `Candidate`: created by this skill and not independently reviewed or explicitly approved.
- `Reviewed`: independent design/review was performed but the full approved work chain is not approved yet.
- `Approved`: explicit human approval or independent review allows this design to be treated as approved input.

Do not mark self-authored design `Approved` solely because it looks consistent.

Open design questions that affect requirement meaning, controlled relationships, interfaces/contracts, evidence model, or inside/outside choices block `Approved`.

## Process

1. Read completed requirements control JSON.
2. For `controlled_run` JSON pre-goal work, verify `What the User Approved: Approved` before deriving or writing the design.
3. Verify the information sufficiency gate before design: `information_sufficiency_check` status is `satisfied` or reviewed `not_required`, includes run-local `evidence_ref` values, and has approved independent `counterexample_review`; otherwise route to `RunInformationSufficiencyCheck`.
4. Derive the design path from the requirements path.
5. Inspect the routing context from the user request, router output, and requirements checks.
6. Inspect only enough context to avoid generic design.
7. Identify whether `$superpowers:brainstorming` is required, used, blocked, or not required.
8. If What the User Approved records how this should be answered or what is not enough, instantiate that answer path and record Required Answer Path Check before deriving any model.
9. Build the target answer path instance: answer path nodes, answer/state transitions, required evidence, and completion conditions.
10. Derive the what supports each required step from answer path nodes: support objects, mechanisms, relationships, flows, inside/outside choices, alternatives, and rules that cannot change.
11. Write design details only as required-step mappings: mechanisms, interfaces/contracts, state/lifecycle, failure model, evidence/evidence check model, compatibility/integration, and decisions must each name the required step they support or be marked supporting-only.
12. If Final Answer Format Check requires structure synthesis, design the output structure and evidence-reference rules.
13. Separate design rules that cannot change from tactical degrees of freedom.
14. Map answer path and support model elements to goal implications and execution-policy implications.
15. If material design questions remain, record them and stop without marking Approved.
16. Do not create goal, plan, review, runtime `/goal`, or target-work files.

## Response-Only Handoff Rule

Do not write handoff prompts into the design artifact.

After design is sufficient, choose the response-only handoff from routing context:

- If the task is `controlled_run`, JSON pre-goal work, or the requirements checks show `execution-plan check: required` or `review check: required`, hand off to `$orchestrating-cybernetic-pregoal`.
- If the task is `bounded_runtime` work and no execution-policy or control-review check is required, hand off to `$writing-cybernetic-goals`.
- If routing context is absent or contradictory, do not default to `$writing-cybernetic-goals`; report that the original routing decision is needed.

The design-to-goal mapping means the future goal must reference the design. It does not mean this skill should directly dispatch goal writing for JSON pre-goal work.

## Output Format

This output format is response-only. Do not write `$skill ...` commands, runtime `/goal` prompts, or conversational next-step prompts into the design artifact.

After creating or updating a design:

```markdown
Created or updated solution design:

`docs/cybernetics/runs/YYYY-MM-DD-slug/design.control.json`

Design summary:
- Required answer path: ...
- Support model: ...
- Output contract, if designed: ...
- Inside/Outside Choices: ...
- Evidence model: ...

Design status:
- Status: `Candidate`
- Open design questions: ...

Response-only handoff:
- For `controlled_run` JSON pre-goal work: use `$orchestrating-cybernetic-pregoal` with the requirements analysis and this design.
- For `bounded_runtime` work only: use `$writing-cybernetic-goals` with the requirements analysis and this design.
```

If blocked:

```markdown
Solution design blocked.

Reason:
- ...

Smallest input needed:
- ...

Response-only next step:
- If requirements analysis is incomplete or has blocking human decisions: return to `$analyzing-cybernetic-requirements` with the missing decision.
- If `controlled_run` JSON pre-goal work lacks `What the User Approved: Approved`: return to `$analyzing-cybernetic-requirements` for approved target approval or revision.
- If a design decision is missing: answer the smallest design question, then rerun `$designing-cybernetic-solutions`.
- For `controlled_run` JSON pre-goal work: return this blocked status to `$orchestrating-cybernetic-pregoal`; do not write goal control JSON.
- If the human explicitly says required design is unnecessary: return to the route-appropriate next stage.

Do not write goal control JSON until this design decision is resolved or the human explicitly says the required design is unnecessary.
```

## Validation Checklist

- [ ] Requirements analysis is complete before design is approved.
- [ ] For `controlled_run` JSON pre-goal work, What the User Approved is Approved before design starts.
- [ ] For `controlled_run` JSON pre-goal work, `information_sufficiency_check` is `satisfied` or reviewed `not_required`, has run-local `evidence_ref` values, and has approved independent `counterexample_review`; otherwise route to `RunInformationSufficiencyCheck`.
- [ ] If What the User Approved records How this should be answered or What is not enough, the design includes Required Answer Path Check and does not substitute a weaker answer path.
- [ ] The design path uses the requirements analysis date/slug.
- [ ] The design stays within core cybernetic vocabulary unless an explicit adapter supplies additional terms.
- [ ] Required answer path instance appears before what supports each required step.
- [ ] Support objects/components/mechanisms map to answer path nodes or are marked supporting-only.
- [ ] Relationships, flows, and inside/outside choices are explicit as support for answer path nodes.
- [ ] Interfaces/contracts, lifecycle/state, failure model, and evidence/evidence check model are explicit when relevant.
- [ ] Output structure, evidence-reference rules, and acceptance condition are explicit when Final Answer Format Check requires structure synthesis.
- [ ] Alternatives and design decisions are recorded where there were plausible options.
- [ ] Design rules that cannot change are separated from tactical degrees of freedom.
- [ ] Design-to-goal and design-to-execution mappings are present.
- [ ] `$superpowers:brainstorming` is used only when required by exploratory design.
- [ ] The design artifact does not contain a next-step prompt.
- [ ] If blocked, the assistant response includes a response-only next step.
- [ ] `controlled_run` JSON pre-goal work hands off to `$orchestrating-cybernetic-pregoal`, not directly to `$writing-cybernetic-goals`.
- [ ] No goal, execution policy, review, runtime `/goal`, or target-work artifact was created.
