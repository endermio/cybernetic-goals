# Review: [Name]

## Review Status

Status: `Needs Revision`

## Inputs Reviewed

- Requirements analysis: `[path]`
- Solution design: `[path or not required]`
- Goal: `[path]`
- Execution policy: `[path]`

## Review Independence

- Pre-goal review subagents authorized: `yes/no`
- Independent review passes completed:
  - Requirement traceability: `yes/no`
  - Human approved target check: `yes/no`
  - Design check: `yes/no`
  - Design answer method check: `yes/no`
  - Final answer format check: `yes/no`
  - Goal check: `yes/no`
  - Who does the work / context use: `yes/no`
  - User purpose evidence check: `yes/no`
  - Result placement check: `yes/no`
  - What counts as done check: `yes/no`
  - answer path check: `yes/no`
  - Work covered in this run and authority check: `yes/no`
  - Parallel agent safety check: `yes/no`
  - Work size / evidence check load: `yes/no`
  - Evidence check governance: `yes/no`
  - Execution cadence: `yes/no`
  - Runtime safety: `yes/no`
- Explicit human approval present: `yes/no`
- Approval allowed: `yes/no`

Notes:

- [independence note]

## Required Check Results

- Design Answer Method Check: `PASS / FAIL / Not applicable`
- Steps That Make The Result True Check: `PASS / FAIL / Not applicable`
- Work Coverage / Action Limits Check: `PASS / FAIL / Not applicable`
- Done / Purpose / Result Placement Check: `PASS / FAIL / Not applicable`
- Work Assignment / Subagent Check: `PASS / FAIL / Not applicable`

Required check rule:

- If Design Answer Method Check is `FAIL`, Review Status cannot be `Approved`.
- If any required check is `FAIL`, record `Needs Revision` or `Rejected` and route to the earliest failing artifact.

## Final Independent Check

- Last independent review completed at: `[time or review pass label]`
- Substantive artifact changes after last independent review: `yes/no`
- If yes, final re-review performed: `yes/no`
- Final reviewers confirming no Blocking/Major findings:
  - [reviewer / role]
- Deterministic-only exception used: `yes/no`
- Deterministic guard covering exception:
  - [command/result]
- Approval allowed after final observer check: `yes/no`

Rationale:

- [why the final observed artifact may or may not be approved]

## Structural Lint Result

- [pass/fail summary]

## Artifact Hygiene / Signal-to-Noise

Findings:

- [generated artifacts are compact/non-conversational/non-duplicative, or note required cleanup]

## Requirement Traceability

Findings:

- [finding]

## What The User Approved Check

Check:

- requirements analysis contains `What the User Approved: Approved` when full pre-goal orchestration is used;
- goal preserves the approved compact control commitment;
- design, goal, and execution policy do not reinterpret human purpose, input role binding, primary object, requested transformation, non-goals, How We Know The User Purpose Was Met, Where The Result Must Show Up, Final Answer Format, why this process is needed, or known assumptions;
- downstream artifacts do not expand or change the what the user approved without explicit human reapproval.

Findings:

- [finding]

## Goal Check

Findings:

- [finding]

## Design Check

Findings:

- [finding]

## Design Answer Method Check

Check:

- requirements `How this should be answered` and `What is not enough` are preserved when present;
- design instantiates the approved answer method or returns to requirements approval instead of substituting a weaker answer path;
- `coverage-ceiling-measurement` includes full workflow scope inventory, major removable source / bottleneck inventory, ceiling coverage criterion, candidate coverage matrix, same-workload full workflow run, and interpretation against coverage matrix;
- goal and execution policy do not weaken the design answer method.

Findings:

- [finding]

## Final Answer Format Check

Check:

- requirements `Final Answer Format` is preserved in goal `Final Answer Format`;
- design `Final Answer Format Design`, if present, is preserved in goal and execution policy;
- execution policy collects material needed for the final output;
- runtime `/goal` cannot replace audience, purpose, medium, structure, detail level, destination, or machine-readable shape.

Findings:

- [finding]

## Is The Plan Controllable

Findings:

- [finding]

## Who Does The Work / Context Use

Check:

- selected work assignment is explicit;
- Level 3/4 main-only execution has a context-load justification;
- delecheckd work packages define Context pack, Allowed actions, Return format, and Integration check;
- context packs include relevant control excerpts, current batch objective, allowed artifacts/places, forbidden changes, required evidence checks/evidence, stop conditions, and expected return format;
- parallel subagent-driven execution has explicit human approval, dependency independence, and control-review approval;
- subagents cannot modify approved files, widen scope, replace work assignment, or bypass integration checks;
- main agent owns dispatch, integration, progress log, and stop-condition detection;
- context compression is defined for batch limits;
- subagent outputs remain candidate results until main-agent integration;
- context overload is not assigned to the main agent.

Findings:

- [finding]

## Is The Work Split At The Right Size

Check:

- batches are coherent intended-result slices, not mechanical micro-steps;
- the plan chooses the largest coherent batch that remains diagnosable;
- broad verification is assigned to integration or final checks unless justified;
- evidence check cost does not dominate execution cost;
- stale evidence checks cannot block approved structural change without evidence check-governance review.

Findings:

- [finding]

## Evidence check / Evidence Governance

Findings:

- [finding]

## User Purpose Evidence Check

Classification:

- `User purpose evidence adequate / Internally verified, user purpose evidence pending / Purpose partially observed / User purpose evidence unavailable, honest handoff required / Purpose-limit evidence not required, justified`

Check:

- Block false completion claims, not necessarily continued execution.
- Internal progress evidence is not treated as purpose-achievement evidence unless the human purpose is internal-state correctness.
- Purpose-limit feedback is the smallest sufficient feedback for the human purpose, not heavy end-to-end evidence by default.
- Missing purpose feedback results in honest pending, partial, unavailable, or handoff wording instead of claiming purpose achieved.
- Goal success is tied to purpose-realizing outcome observed or justified internal-state correctness.

Findings:

- [finding]

## Result Placement Check

Classification:

- `result-placement adequate / result-placement partial / result-placement missing / result-placement unavailable / not applicable with justification`

Check:

- Strongest positive result claims require result-placement adequate.
- Partial, missing, unavailable, or not applicable with justification receives matching completion wording.
- Flag when local action is being treated as global intended-result realization.
- Required places are acted on, inspected, preserved, excluded, or discovered as planned.
- Old-state residuals, unknown places, preserved places, and excluded places are reconciled.
- Result-placement evidence is distinct from how we know the user purpose was met.

Findings:

- [finding]

## What Counts As Done Check

Check:

- there is exactly one what counts as done;
- no partial, diagnostic, blocked, invalid, unavailable, fallback, or not done report appears in Success Condition;
- no report-when-not-done status is listed under done states;
- execution policy includes a target-producing action or proof-of-impossibility path;
- the plan cannot terminate with `goal achieved: yes` without satisfying the what counts as done;
- any use of "valid final status" separates `goal achieved: yes` from `goal achieved: no`.

Findings:

- [finding]

## Answer Path Check

Check:

- execution decomposition starts from an actor-centered required answer path, not component inventory;
- every mainline work package maps to at least one required step;
- supporting-only work is explicitly marked and cannot satisfy goal progress by itself;
- no final integration path or primary use path is deferred to future work while achieved claims remain possible;
- component, module, or workflow evidence is not substituted for required step evidence;
- failed, blocked, or unobserved required steps are not moved into residual risk while review remains Approved.

Findings:

- [finding]

## Work Covered And Allowed Actions Check

Check:

- work covered in this run is not silently reduced to the first safe segment;
- what the agent may do limits define execute / prepare-only / observe-only / forbidden-not-executed handling, not scope removal;
- unauthorized live or irreversible actions remain in horizon accounting unless explicitly out of scope by What the User Approved;
- approved horizon items are not moved to future roadmap, handoff, or later goal because runtime lacks direct authority;
- execution policy can continue authorized downstream work that does not depend on forbidden actions;
- prepare-only or forbidden-not-executed items are not claimed as live complete;
- final report can distinguish executed, prepared-only, forbidden-not-executed, and explicitly out-of-scope by What the User Approved.

Findings:

- [finding]

## Parallel Agent Safety Check

Check:

- max-safe-parallel requests are preserved unless the policy records a concrete safe-frontier reason for serial execution;
- selected subagent execution mode matches selected work assignment and agent workflow;
- selected Superpowers workflow supports the selected execution mode;
- `$superpowers:subagent-driven-development` is not used with `parallel-max-safe`;
- `$superpowers:dispatching-parallel-agents` is used only for independent parallel domains and remains governed by the approved wave, lock, barrier, failure, and integration rules;
- serial subagent-driven execution uses one active subagent, ordered work package sequence, and integration after each package;
- parallel subagent-driven execution has dependency independence, concurrency frontier, wave matrix, conflict / lock model, integration barriers, and failure policy;
- no parallel work package can modify the same place without a lock rule or barrier;
- subagent outputs remain candidate results until main-agent integration;
- selected agent workflow matches the approved work packages.

Findings:

- [finding]

## Evidence Lifecycle / Evidence Budget

Check:

- execution policy does not store repeated full raw evidence check outputs per batch;
- raw evidence volume cannot exceed the controlled work size without justification;
- intermediate evidence records summary and delta instead of only full raw output;
- tracked evidence is reviewable;
- raw, pointer, summary/delta, and retained-full retention policy exists;
- evidence files are referenced by indexed summaries or raw pointer rather than loaded as context;
- reviewers do not need to read raw evidence to approve;
- evidence artifacts are separated into transient raw, raw pointer, reviewable summary/delta, and retained full classes;
- repeated full snapshots of the same evidence check are justified only when delta is impossible.

Findings:

- [finding]

## Batch Rhythm

Findings:

- [finding]

## Meaning vs Execution Detail

Findings:

- [finding]

## Runtime Suitability

Findings:

- [finding]

## Critical Findings

- [critical issue]

## Required Revisions

- [revision]

## Non-Critical Suggestions

- [suggestion]

## Convergence Notes

- [what changed across review iterations]

## Approval Conditions

The approved work chain may be approved only if:

- requirements analysis status is Complete;
- required solution design exists and preserves requirements analysis meaning;
- design answer method check preserves the approved answer method and answer method when What the User Approved records them;
- goal preserves requirements analysis meaning;
- goal and execution policy preserve required design rules;
- any upstream output contract is preserved in the goal and supported by the execution policy;
- execution policy preserves goal and requirements analysis;
- execution work assignment is explicit and does not create main-agent context overload;
- work size and evidence check load do not create micro-step overcontrol or evidence check overcoupling;
- evidence lifecycle keeps tracked evidence reviewable and prevents raw evidence check output explosion;
- purpose feedback adequacy supports the permitted completion wording and does not confuse internal progress evidence with purpose achievement;
- realization place result placement adequacy supports result claim wording and does not confuse local action with global realization;
- target achievement what counts as done check preserves a what counts as done;
- required answer path check preserves an actor-centered state-transition path and work-package mapping;
- work covered in this run and authority check preserves the approved horizon and does not convert authority limits into out-of-scope roadmap items;
- parallel agent safety check preserves the approved execution mode, wave/barrier model, and main-agent integration rule;
- evidence check/evidence governance is explicit;
- batch cadence is explicit;
- runtime execution does not need to synthesize a new plan.
- independent review discipline was satisfied or explicit human approval exists.
- no substantive artifact mutation remains unreviewed after the latest independent review.
- any deterministic-only exception is explicitly recorded and guard-covered.

## Final Decision

Status: `Needs Revision`

Rationale:

- [reason]
