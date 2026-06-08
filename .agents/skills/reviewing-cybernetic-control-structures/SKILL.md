---
name: reviewing-cybernetic-control-structures
description: 'Use when requirements analysis, any required design, goal contract, and execution policy exist before runtime /goal, and the cybernetic approved work chain needs independent approval, blocker review, or risk review.'
---

# Reviewing Cybernetic Control Structures

## Overview

Review whether the AI approved work chain is coherent enough to execute.

Inputs:

- requirements analysis brief
- solution design, when required design is required or a design exists
- goal contract
- execution policy / plan

Output:

```text
docs/cybernetics/control-reviews/YYYY-MM-DD-<slug>.md
```

Use `assets/control-review-template.md`.

This skill does not execute target work and does not start `/goal`.

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

This skill requires independent review discipline before it may mark a approved work chain `Approved`.

Do not self-review and mark `Approved`. Do not run target execution. Do not dispatch execution agents during pre-goal control review.

If pre-goal review subagents are explicitly authorized, use independent reviewer passes for the approved work chain. This is not the full `$superpowers:subagent-driven-development` execution workflow; it is independent review discipline only.

If pre-goal review subagents are not authorized and no explicit human approval or other independent reviewer exists, produce a review marked `Needs Independent Review`. Do not mark `Approved`.

## Final Observer Rule

No `Approved` state is allowed after an unreviewed substantive artifact mutation.

A approved work chain may be marked `Approved` only when the last substantive change to the reviewed approved files, meaning the requirements analysis, solution design, goal, or execution policy, has been followed by an independent review pass that reports no Blocking or Major findings.

If any approved file changes after the latest independent review, the review state becomes `Dirty` / `Needs Re-review` and cannot be `Approved`.

Substantive changes to the control review's final decision, reviewer findings, approval rationale, or Final Independent Check after approval also require re-review or explicit human approval. Mechanical recording of already-reviewed findings into the review file does not itself create a new review cycle.

Deterministic-only changes may skip subagent re-review only when all of the following are true:

- the change is explicitly listed as deterministic-only;
- a deterministic guard covers the changed condition and passes;
- the control review records that no meaning or control-policy content changed.

Substantive changes include changes to:

- confirmed meaning;
- What the User Approved or the approved compact control commitment;
- solution design objects, relationships, flows, boundaries, interfaces/contracts, evidence model, or design invariants;
- goal success conditions;
- scope, boundaries, or invariants;
- execution policy or batch cadence;
- who does the work / context use;
- evidence check or evidence structure;
- user purpose evidence limit, user purpose evidence strategy, or completion-claim wording;
- where the result must show up, residual reconciliation, or result claim wording;
- work covered in this run, what the agent may do, forbidden-action handling, or work covered in this run coverage matrix;
- evidence lifecycle, retention, budget, or tracked-evidence policy;
- progress log required fields;
- stop conditions;
- runtime limit;
- approval criteria;
- artifact consistency rules;
- anything required by a prior reviewer as a Blocking or Major finding.

Deterministic-only changes include:

- heading capitalization required by lint;
- Markdown fence repair;
- path typo repair when the intended path is unambiguous;
- manifest ordering;
- whitespace.

The author of a post-review revision must not be the sole approver of that revision.

## Check Cascade Rule

Record required check results before detailed findings:

1. Design Answer Method Check
2. Steps That Make The Result True Check
3. Work Coverage / Action Limits Check
4. what-counts-as-done / user-purpose evidence / result-placement Check
5. Work Assignment / Subagent Check

If Design Answer Method Check is `FAIL`, the review cannot be `Approved`; route back to design or What the User Approved according to the failing answer method contract. If another required check is `FAIL`, route to the earliest failing artifact before evaluating downstream polish.

## Review Dimensions

### 1. Requirement Traceability

Every confirmed human decision in the requirements analysis brief must appear in the goal and execution policy.

### 2. What The User Approved Check

For Level 3/4 or full pre-goal work, requirements analysis must contain `What the User Approved: Approved`.

Check that design, goal, and execution policy preserve the approved compact control commitment:

- human purpose;
- input role binding;
- primary object;
- requested transformation;
- non-goals;
- How We Know The User Purpose Was Met Limit;
- Where The Result Must Show Up;
- What counts as done;
- Evidence needed to call it done;
- report when not done handling;
- How this should be answered;
- What is not enough;
- How this should be answered;
- Final Answer Format;
- Work covered in this run;
- What the agent may do;
- Forbidden live / irreversible actions;
- Required handling for unauthorized actions;
- Explicitly out-of-scope items;
- Agent delegation preference;
- Agent workflow preference;
- Parallel execution authority;
- Parallelism cap;
- workflow fit;
- known assumptions.

Flag as Major or Blocking when downstream artifacts reinterpret, expand, remove, or contradict the approved compact control commitment. If a downstream artifact changes the primary object, requested transformation, non-goals, user-purpose evidence, result-placement, what-counts-as-done condition, final answer format, or workflow fit, require what the user approved revision or explicit human reapproval before approval.

### 3. Goal Check

The goal must not add, remove, downscope, or reinterpret requirement meaning.

### 4. Design Check

When a solution design exists or required design was required:

- the design must preserve requirements analysis meaning;
- the goal must preserve design invariants;
- the plan must preserve design objects, relationships, boundaries, flows, interfaces/contracts, lifecycle/failure model, and evidence model;
- tactical degrees of freedom must not be frozen as meaning invariants unless the design explicitly says so;
- the plan must not redesign the solution model.

### 5. Design Answer Method Check

When What the User Approved records `How this should be answered`, `What is not enough`, or `How this should be answered`, the design is a meaning compiler for that approved answering method.

Flag as Major or Blocking when:

- design substitutes a weaker answer method for the approved answering method;
- design instantiates a different how this should be answered without returning to What the User Approved;
- design reports the what is not enough as sufficient;
- `coverage-ceiling-measurement` lacks full workflow scope inventory, major removable source / bottleneck inventory, ceiling coverage criterion, candidate coverage matrix, same-workload full workflow run, or interpretation against coverage matrix;
- goal or execution policy inherits a weaker answer method than the design;
- review approves run-validation evidence as coverage-ceiling evidence.

If the approved answer method is infeasible or unsuitable, require return to requirements/What the User Approved. Do not approve a design that silently changes task type.

### 6. Final Answer Format Check

When requirements analysis, solution design, or goal includes an final answer format:

- the requirements `Final Answer Format` must be preserved in the goal `Final Final Answer Format`;
- the design `Final Answer Format Design`, if present, must be preserved in the goal and execution policy;
- the execution policy must collect the material needed for the final output;
- evidence-reference, destination, machine-readable, and acceptance-condition requirements must not be weakened;
- runtime `/goal` must not be able to replace the audience, purpose, medium, structure, detail level, destination, or machine-readable shape.

### 7. Control Law Quality

The execution policy must define a sane execution rule:

- dependency matrix
- who does the work / context use
- context budget
- execution granularity
- evidence check budget
- evidence lifecycle / evidence budget
- batch cadence
- phase checks
- repair policy
- stop conditions

### 8. Evidence check / Evidence Governance

Approved evidence checks, checks, and evidence channels are evidence checks, not objectives.

Flag plans that:

- overfit old evidence checks;
- require every micro-step to pass;
- lack stale evidence check retirement rules;
- lack intended-result evidence.

### 9. User Purpose Evidence Check

Block false completion claims, not necessarily continued execution.

Classify user purpose evidence as one of:

- User purpose evidence adequate
- Internally verified, user purpose evidence pending
- Purpose partially observed
- User purpose evidence unavailable, honest handoff required
- Purpose-limit evidence not required, justified

Flag as Major or Blocking when:

- evidence is used to claim purpose achieved without observing the human purpose or beneficiary/observer limit;
- internal checks, scripts, lint, API smoke, or other convenient evidence checks are treated as purpose-achievement evidence without justification;
- purpose-limit feedback is missing and the plan does not provide honest pending, partial, or unavailable status wording;
- the plan demands heavy end-to-end or operational feedback when a smaller purpose-limit observation would suffice;
- the goal defines success as evidence check success; purpose-realizing outcome evidence is required unless the purpose is internal-state correctness.

### 10. Evidence Lifecycle / Evidence Budget

Flag as Major or Blocking when:

- the execution policy stores repeated full raw evidence check outputs per batch;
- raw evidence volume can exceed the controlled work size without justification;
- intermediate evidence lacks summary or delta;
- tracked evidence is not reviewable;
- no raw, pointer, summary/delta, and retained-full retention policy exists;
- evidence files are loaded as context; indexed references are the required form;
- reviewers would need to read raw evidence to approve;
- evidence artifacts are not separated into transient raw, raw pointer, reviewable summary/delta, and retained full classes;
- repeated full snapshots of the same evidence check are allowed without explaining why delta is impossible.

Use `Major` when execution-policy revision can repair evidence lifecycle. Use `Blocking` when evidence check output would likely swamp review, context management, or runtime completion.

### 11. Result Placement Check

Classify result-placement as one of:

- result-placement adequate
- result-placement partial
- result-placement missing
- result-placement unavailable
- result-placement not applicable with justification

Flag as Major or Blocking when:

- local action is being treated as global intended-result realization;
- the intended result spans places but the policy lacks a place model;
- required actions are unclear for places that carry the intended result;
- old-state residuals, unknown places, preserved places, or excluded
  places lack reconciliation;
- result-placement evidence is used as human-purpose achievement evidence without user-purpose evidence support;
- result-placement not applicable is claimed without justification.

Use `Major` when policy or goal revision can repair result-placement wording. Use
`Blocking` when runtime could claim intended-result realization while important
places or residuals remain unresolved.

### 12. What Counts As Done Check

Flag as Major or Blocking when:

- there is more than one what counts as done;
- any partial, diagnostic, blocked, invalid, unavailable, fallback, or report when not done appears in Success Condition;
- any report-when-not-done status is listed under target-achieved states;
- the execution policy lacks a target-producing action or proof-of-impossibility path;
- the plan can terminate with `goal achieved: yes` without satisfying the what counts as done;
- "valid final status" is used without separating `goal achieved: yes` from `goal achieved: no`.

### 13. Answer Path Check

Flag as Major or Blocking when:

- implementation decomposes by components without a required answer path;
- no mainline work package owns the actor-centered path from initial state to what counts as done;
- candidate tasks lack `Required step(s)`, `Role`, state-transition, transition-evidence, integration-check, or goal-progress fields;
- supporting-only work is allowed to satisfy goal progress by itself;
- final integration path, primary use path, or required-step transition evidence is deferred to future work while achieved claims remain possible;
- component, module, or workflow evidence replaces required-step transition evidence;
- failed, blocked, or unobserved required-step transitions are recorded only as residual risk while review remains Approved.

### 14. Work Covered And Allowed Actions Check

Flag as Major or Blocking when:

- approved full work covered in this run is silently reduced to the first safe segment;
- what the agent may do limits are used as scope removal instead of execute / prepare-only / observe-only / forbidden-not-executed handling;
- unauthorized live or irreversible actions are moved to future roadmap, handoff, or later goal while still inside the approved work covered in this run;
- approved work covered in this run items lack coverage in the execution policy;
- prepare-only or forbidden-not-executed work is claimed as executed or live complete;
- the final report cannot distinguish executed, prepared-only, forbidden-not-executed, and explicitly out-of-scope by What the User Approved.

### 15. Who Does The Work / Context Use

Flag as Major or Blocking when:

- no who does the work exists;
- Level 3/4 work assigns all target work to the main agent without a context-load justification;
- the plan creates context overload by making the main agent coordinator, worker, integrator, and verifier for context-heavy work;
- delegated work packages lack Context pack, Allowed actions, Return format, or Integration check;
- context packs contain only artifact path lists; bounded operating context requires relevant control excerpts, current batch objective, allowed artifacts/places, forbidden changes, required evidence checks/evidence, stop conditions, and expected return format;
- parallel subagent-driven execution lacks explicit human approval, dependency independence, or control-review approval;
- a subagent may modify approved files, widen scope, replace work assignment, or bypass integration gates;
- progress-log ownership or stop-condition detection is unclear;
- context compression or bounded return material is missing for delegated work;
- subagent outputs can be treated as final completion before main-agent integration.

Use `Major` when execution-policy revision can repair work assignment. Use `Blocking` when context overload would likely make runtime lose requirements, design invariants, final answer format, stop conditions, or approval boundaries.

### 16. Subagent Concurrency Check

Flag as Major or Blocking when:

- the What the User Approved requests max-safe-parallel but the plan selects serial without a concrete safe-frontier reason;
- What the User Approved requests `superpowers-subagent-driven-development` and max-safe-parallel at the same time without returning to what the user approved revision;
- selected subagent execution mode does not match who does the work or agent workflow;
- the selected Superpowers workflow does not support the selected execution mode;
- `$superpowers:subagent-driven-development` is used with `parallel-max-safe`;
- `$superpowers:dispatching-parallel-agents` is treated as if it provides the implementer/spec-review/code-quality review loop from subagent-driven-development;
- serial subagent-driven execution lacks `serial-single-active`, `Max concurrent subagents: 1`, ordered sequence, or integration after each package;
- parallel subagent-driven execution lacks dependency independence, concurrency frontier, wave matrix, conflict / lock model, integration barriers, or failure policy;
- two parallel work packages can touch the same place without a lock rule or barrier;
- subagent outputs can become final without main-agent integration;
- selected agent workflow does not fit the approved work packages.

### 17. Execution Granularity / Evidence check Load

Flag as Major or Blocking when:

- batches are mechanical micro-steps; coherent intended-result slices are the required form;
- every step requires full observability;
- evidence check cost dominates execution cost;
- broad verification is required after every small edit;
- stale evidence checks can block approved structural change;
- batch-end gates are too weak to detect drift;
- batch-end gates are so heavy that they prevent progress;
- the plan does not explain why batch size is diagnosable.

Use `Major` when execution-policy revision can repair the execution rule. Use `Blocking` when the granularity or evidence check load would prevent runtime completion or let evidence checks override confirmed meaning.

### 18. Batch Rhythm

Flag:

- excessively tiny steps;
- huge unobservable batches;
- no batch-end openability requirement;
- no destructive intermediate-state policy.

### 19. Meaning vs Tactical Limit

Meaning invariants must be frozen. Tactical execution details must remain adjustable.

### 20. Runtime Suitability

The runtime `/goal` must be able to execute the approved artifacts without inventing new approved work chains. Any required runtime discipline, including approved work assignment, bounded subagent delegation protocol, and conditionally selected Superpowers workflow, must be precompiled into the approved plan, review, or final `/goal`.

Runtime completion claims must be calibrated to the highest purpose-relevant evidence actually observed. If user purpose evidence is missing, runtime must report what is verified, what is not yet observed, and the smallest next observation needed. Purpose-achieved wording is reserved for observed or approved user purpose evidence.

Runtime result claims must also be calibrated to Where The Result Must Show Up
Placement status. Do not claim intended-result realization from local action alone
when Where The Result Must Show Up is required. Strongest positive
result claims require result-placement adequate.

Runtime what-counts-as-done claims must be calibrated to the what counts as done. report when not done may stop execution honestly, but they do not support `goal achieved: yes`.

### 21. Review Independence

The review must record:

- whether subagents were explicitly authorized;
- which independent review passes were completed;
- whether approval is allowed;
- why approval is blocked when independent review is missing.

### 22. Final Independent Check

The review must record whether any substantive artifact changed after the latest independent review pass and whether a final independent observer confirmed no Blocking or Major findings after that change.

## Deterministic Lint

If scripts are available, run:

```bash
python3 .agents/skills/reviewing-cybernetic-control-structures/scripts/control_artifact_lint.py \
  --requirements [REQUIREMENTS] \
  --design [DESIGN] \
  --goal [GOAL] \
  --plan [PLAN]
```

Use the lint output as a structural evidence check. Do not treat lint as meaning approval.

## Output Status

The review must be either:

- `Needs Revision`
- `Needs Independent Review`
- `Dirty`
- `Needs Re-review`
- `Approved`

Only mark `Approved` when:

- requirements analysis, required design, goal, and plan are consistent;
- What the User Approved is Approved when full pre-goal orchestration is used, and What The User Approved Check has no Blocking/Major findings;
- Work Covered And Allowed Actions Check has no Blocking/Major findings for full-route or multi-batch work;
- required design exists and is consistent with requirements analysis, goal, and plan;
- Design Answer Method Check has no Blocking/Major findings when What the User Approved records an answering method or answer method;
- any upstream final answer format is preserved in the goal and supported by the execution policy;
- no unresolved meaning decision remains;
- execution policy does not self-authorize uncontrolled changes;
- work assignment is explicit and does not create main-agent context overload;
- execution granularity and evidence check load do not create micro-step overcontrol or evidence check overcoupling;
- user purpose evidence check supports the permitted completion wording and does not confuse internal progress evidence with purpose achievement;
- result placement check supports result claim wording and does not confuse local action with global realization;
- what counts as done check preserves the what counts as done;
- evidence lifecycle keeps tracked evidence reviewable and prevents raw evidence check output explosion;
- evidence check/evidence governance is explicit;
- runtime `/goal` can execute without writing or approving a new plan.
- independent review discipline was satisfied or explicit human approval exists.
- no substantive artifact mutation remains unreviewed after the latest independent review.
- any deterministic-only exception is explicitly recorded and guard-covered.

## Response-Only Handoff Rule

Do not write handoff prompts into the review artifact.

After review status is set:

- If invoked by `$orchestrating-cybernetic-pregoal` or full pre-goal context, return the review path and status to `$orchestrating-cybernetic-pregoal`.
- If standalone/manual and status is `Approved`, hand off to `$compiling-cybernetic-runtime-goals`.
- If status is `Needs Revision`, `Dirty`, or `Needs Re-review`, revise the relevant approved files and rerun review; do not compile runtime `/goal`.
- If status is `Needs Independent Review`, obtain independent review or explicit human approval; do not compile runtime `/goal`.

## Output Format

This output format is response-only. Do not write `$skill ...` commands, runtime `/goal` prompts, or conversational next-step prompts into the review artifact.

```markdown
Created or updated control review:

`docs/cybernetics/control-reviews/YYYY-MM-DD-slug.md`

Review status:
- `Approved` / `Needs Revision` / `Needs Independent Review` / `Dirty` / `Needs Re-review`

Key findings:
- ...

Response-only next step:
- If full pre-goal orchestration owns the chain: return to `$orchestrating-cybernetic-pregoal` with the review path and status.
- If standalone/manual and `Approved`: run `$compiling-cybernetic-runtime-goals`.
- If `Needs Revision`, `Dirty`, or `Needs Re-review`: revise the named artifacts and rerun `$reviewing-cybernetic-control-structures`.
- If `Needs Independent Review`: obtain independent review or explicit human approval before runtime compilation.
```

## Validation Checklist

- [ ] The review file was created.
- [ ] Review status is explicit.
- [ ] Review independence is recorded.
- [ ] What The User Approved Check was checked when full pre-goal orchestration is used.
- [ ] Design Answer Method Check was checked when What the User Approved records an answering method or answer method.
- [ ] Final observer check is recorded.
- [ ] The review does not mark self-review as `Approved`.
- [ ] If subagents were not authorized and no human approval exists, status is `Needs Independent Review`.
- [ ] If any substantive artifact changed after independent review, including required design, status is `Dirty` or `Needs Re-review` until final independent re-review reports no Blocking or Major findings.
- [ ] Lint PASS is not treated as meaning/control-policy approval.
- [ ] Critical findings distinguish meaning, design, goal, plan, evidence check, and runtime issues.
- [ ] Output contract check was checked when any upstream final answer format exists.
- [ ] Evidence lifecycle and evidence budget were checked.
- [ ] User purpose evidence check was checked.
- [ ] Result placement check was checked.
- [ ] What Counts As Done Check was checked.
- [ ] Answer Path Check was checked.
- [ ] Work Covered And Allowed Actions Check was checked.
- [ ] Subagent Concurrency Check was checked.
- [ ] Execution granularity and evidence check load were checked.
- [ ] Required revisions are actionable.
- [ ] Response-only handoff matches the review status and does not bypass `$orchestrating-cybernetic-pregoal` when full pre-goal orchestration owns the chain.
- [ ] The assistant response includes a response-only next step for every review status.
- [ ] The review did not execute target work.
- [ ] The review did not output final runtime `/goal`.
