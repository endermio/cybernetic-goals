---
name: orchestrating-cybernetic-pregoal
description: 'Use when completed requirements analysis exists and routing or requirements require JSON pre-goal orchestration before runtime /goal. Level 3 defaults to lean pre-goal; full pre-goal is an exception for high-risk, irreversible, externally impactful, non-replannable, or explicitly full workflows.'
---

# Orchestrating Cybernetic Pre-goal

## Overview

This skill orchestrates the **pre-goal compilation chain** after requirements have been analyzed.

It turns completed requirements control JSON into approved JSON control files.

Lean default:

```text
requirements.control.json
  -> run.control.json
  -> gen-000/runtime.control.json plus short /goal pointer
```

Full exception:

```text
requirements.control.json
  -> solution design, when required design is required
  -> design.control.json
  -> goal.control.json
  -> plan.control.json
  -> review.control.json
  -> runtime.control.json plus short /goal pointer
```

This skill is a thin orchestrator. It does not replace the other cybernetic skills. It coordinates them. Full-chain orchestration is a safety exception or migration bridge, not the default Level 3 startup path.

Official persistent control facts are JSON only. Historical Markdown may be read as non-authoritative background, but do not create or compile Markdown as official guard, compiler, runtime, or long-term dual-path control input.

## What This Skill Owns

This skill owns pre-goal artifact orchestration. It coordinates existing
cybernetic skills and preserves their ownership limits.

Owned orchestration:

- inspect completed requirements control JSON
- call existing cybernetic skills in the correct order
- emulate narrow cybernetic formatting only when a downstream cybernetic skill is unavailable and that fallback is explicitly allowed
- create or update approved control files under `docs/cybernetics/runs/<slug>/`
- invoke, request, or validate a solution design when required design is required
- propacheck and validate output contract presence across downstream artifacts
- use explicitly authorized subagents as independent reviewers
- run an Intent Preservation / Obligation Preservation subagent review pass
  when subagent review is authorized
- iterate review and revision up to the configured limit
- compile `runtime.control.json` and the final short `/goal` pointer after approval

Routed elsewhere or held for approval:

- new requirement analysis goes to `$analyzing-cybernetic-requirements`
- required solution design goes to `$designing-cybernetic-solutions`
- output contract identification belongs to requirements analysis; complex output-structure synthesis belongs to solution design; final output contract preservation belongs to goal writing
- target work starts only after the final runtime `/goal` is launched separately
- requirement decisions remain human decisions
- pre-goal review subagents require explicit authorization in the current request
- `/goal` execution uses an approved plan; runtime plan writing and approval stay outside `/goal`

Approval requires resolved meaning conflicts and the configured independent
review discipline.

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

This orchestrator may emulate cybernetic artifact formatting when a downstream cybernetic skill is unavailable. It must not emulate required Superpowers infrastructure.

It must not emulate solution design synthesis. Solution design is a substantive approved file, not narrow formatting.

It must not synthesize output contracts. Output contract identification belongs to requirements analysis; complex output-structure synthesis belongs to solution design; final output contract preservation belongs to goal writing.

Required infrastructure limits:

- non-trivial execution policy generation requires `$superpowers:writing-plans` as planning workflow;
- review `Approved` requires independent review discipline or explicit human approval;
- review `Approved` requires a final observer pass after the last substantive artifact mutation;
- runtime `/goal` compilation must include `$superpowers:executing-plans`, `$superpowers:systematic-debugging`, and `$superpowers:verification-before-completion` discipline.

If a required workflow is unavailable, stop and report the missing infrastructure. Do not self-substitute and do not mark the approved work chain `Approved`.

## Relationship to Other Skills

Use this skill only after completed `requirements.control.json` exists and
one of these fit checks is satisfied:

- `$routing-cybernetic-workflows` has recommended Level 3 lean pre-goal, Level 4 full pre-goal, or explicit full pre-goal exception handling;
- `$analyzing-cybernetic-requirements` has explicitly recorded that JSON pre-goal orchestration is required.

The same requirements brief must record `What the User Approved: Approved`,
or the current user message must explicitly approve the compact control
commitment recorded in that requirements brief.

If the current user message approves the compact control commitment, update the requirements analysis `What the User Approved` section first, quoting or referencing that approval, then continue. Do not rely on in-memory approval to pass orchestration or runtime guards.

A user request to use full pre-goal compilation is not sufficient by itself.
If the request expresses method preference, uncertainty, dissatisfaction, or
process distrust, route to `$framing-cybernetic-intent` or
`$routing-cybernetic-workflows` first.

This skill orchestrates:

- `$writing-cybernetic-goals`
- `$designing-cybernetic-solutions`
- `$writing-cybernetic-execution-policies`
- `$reviewing-cybernetic-control-structures`
- `$compiling-cybernetic-runtime-goals`
- `$cybernetic-superpowers-infrastructure`

It should not duplicate their templates or rules unless they are unavailable. If a downstream cybernetic skill is available, prefer using it. If a downstream cybernetic skill is unavailable, emulate only its narrow cybernetic responsibility and state that the fallback was used.

Never emulate required Superpowers workflows. In particular:

- do not replace `$designing-cybernetic-solutions` with orchestrator-authored solution design when required design is required;
- do not replace `$superpowers:writing-plans` with ad hoc internal planning for non-trivial execution policies;
- do not replace independent review discipline with self-review;
- do not compile a runtime `/goal` that omits required runtime execution, debugging, and verification discipline.

## Process Need Check

Before creating downstream artifacts, confirm the lightest workflow that
controls the task. Level 3 defaults to lean pre-goal. Full pre-goal is selected
only by exception criteria.

Reject or downgrade when:

- the input is pre-task intent;
- the task is Level 0/1/2;
- existing artifacts already control the meaning;
- full orchestration would produce formal artifacts without reducing runtime
  uncertainty;
- evidence/context/review budget cannot be bounded.

## User Approval Check

Before invoking or validating solution design, goal writing, execution-policy
writing, review, or runtime compilation, verify What the User Approved
Approval.

If missing or not `Approved`, stop before design and output:

```text
Blocked: What the User Approved missing.
Next: ask the user to approve or revise the compact control commitment in the requirements analysis.
```

Do not compensate by asking the user to review design, goal, or execution
policy later. Human answers are inputs; they are not approval unless the user
explicitly approves the compact control commitment. If the current user message
approves the compact control commitment, update the requirements analysis
`What the User Approved` section first before downstream guard checks.

## Required Input

A completed requirements control JSON file, usually:

```text
docs/cybernetics/runs/<slug>/requirements.control.json
```

When the input path follows this pattern, the same run directory is the artifact identity for the whole pre-goal chain. Do not choose a different slug unless the user explicitly requests different output paths.

The user should invoke this skill with an explicit requirements path, for example:

```text
$orchestrating-cybernetic-pregoal 根据 docs/cybernetics/runs/2026-05-22-collaborative-supervision/requirements.control.json 自动完成 pre-goal 编译。允许使用 subagents 做独立 review。若 review 无法收敛，停止并报告阻塞点。
```

## Subagent Authorization Rule

Pre-goal review subagents and runtime target-work subagents use different authorization meaning.

Pre-goal review subagents require explicit authorization in the same orchestration request. Do not spawn pre-goal review subagents unless the user explicitly authorizes subagents in that request.

Runtime target-work subagents are authorized only when the final `/goal` explicitly contains the approved subagent-driven execution work assignment and the user launches that `/goal`. Compiling or displaying the final `/goal` does not itself start runtime target-work subagents.

Parallel runtime subagents require explicit human approval recorded in the execution policy and review before the final `/goal` is compiled.

Phrases that count as authorization include:

- `允许使用 subagents`
- `可以使用 subagents`
- `use subagents`
- `spawn subagents`
- `use independent subagent reviewers`

If pre-goal review subagents are not authorized:

- You may create candidate design, goal, and execution policy files.
- You may create a draft review marked `Needs Independent Review`.
- You must not claim independent review or mark the approved work chain `Approved` unless a separate reviewer, explicit human approval, or an authorized subagent review exists.
- Ask the user to authorize pre-goal review subagents or provide explicit control-review approval of the review findings before compiling a final runtime `/goal`.

## Pre-goal Orchestration Modes

### Mode A: Candidate-Only Mode

Use when pre-goal review subagents are not authorized.

Behavior:

1. Check requirements control JSON.
2. Create or validate solution design if required design is required.
3. Create or update `goal.control.json`.
4. Create or update execution policy only if required planning workflow is satisfied or not required.
5. Create a review draft marked `Needs Independent Review`.
6. Do not compile final runtime `/goal` unless the review has independent approval or the user gives explicit control-review approval of the review findings. Do not ask for artifact-by-artifact review as a substitute for What the User Approved.

### Mode B: Subagent-Reviewed Compilation Mode

Use when pre-goal review subagents are explicitly authorized.

Behavior:

1. Check requirements control JSON.
2. Create or validate solution design if required design is required.
3. Create or update `goal.control.json`.
4. Create or update execution policy only if required planning workflow is satisfied or not required.
5. Run independent subagent review passes without running target execution or dispatching execution agents.
6. Revise artifacts based on review findings.
7. Re-review until approval or stop after the maximum review cycles.
8. Create an approved review if findings converge.
9. Compile final runtime `/goal` command.
10. Do not start `/goal`.

## Maximum Review Cycles

Default maximum review-revision cycles: `2`.

If review does not converge after two cycles, stop and report:

- unresolved conflicts
- reviewer disagreements
- exact artifact sections involved
- smallest required human decision

Do not continue self-revising indefinitely.

## NeedsRevision Routing Rule

Subagent semantic review must use normalized verdicts:

```text
`Approved` / `NeedsRevision` / `Blocked`
```

`NeedsRevision` is a review/revision loop result, not a terminal project
failure. It means the approved work chain has repairable intent drift,
obligation downgrade, or stage mismatch. `Blocked` is reserved for cases where
the next revision would require a human decision, missing dependency, or
external fact that cannot be safely inferred.

NeedsRevision routes to the earliest artifact that introduced drift:

- Requirements drift -> `ReturnToRequirementsAnalysis`: approved meaning,
  required outcome, authorization, or non-goal must be revised or reapproved.
- Design drift -> `RunDesign`: the solution model weakened or redirected the
  approved outcome.
- Goal drift -> `RunGoalWriting`: success conditions, scope, limits, or
  what-counts-as-done no longer preserve the approved outcome.
- Plan drift -> `RunExecutionPolicy`: execution policy downgrades required
  work into readiness, future work, allowed action, prepare-only handling, or
  compatibility-only work while still allowing approval.

After the routed revision, rerun independent review and Final Observer before
runtime compilation. Until the review verdict is `Approved`, do not compile `runtime.control.json`.

Regression example: a required `/api/v2` implementation must not be accepted
as legacy Drogon compatibility readiness. That is `NeedsRevision`, routed to
the first artifact that converted implementation into compatibility readiness.

## Finalize Approved Control Chain

Before `ReviewApproved -> RunRuntimeCompile`, all control JSON that enters
runtime must be in final approved state:

```text
requirements.control.json status == approved
design.control.json status == approved
goal.control.json status == approved
plan.control.json status == approved
review.control.json status == approved
runtime.control.json status == compiled
```

`Candidate`, `Reviewed`, `NeedsRevision`, `Needs Revision`, `Dirty`, and
`Needs Re-review` artifacts may enter downstream drafting or review loops, but
may not enter runtime compilation.

If subagent or independent review approves a candidate design, goal, or plan,
the orchestrator must perform an approved control-chain commit before runtime
compile:

1. set the approved artifacts to `status == approved`;
2. recompute `review.control.json` `approved_control_hashes`;
3. delete or rebuild stale `runtime.control.json`;
4. compile `runtime.control.json`;
5. run both:

```bash
control_chain_guard.py --run-dir docs/cybernetics/runs/<slug>
python3 .agents/skills/using-control-json/scripts/validate_control_chain.py docs/cybernetics/runs/<slug>
```

The second command must return `ok: true`. If either command fails, stay in
pre-goal revision/repair. Do not output the runtime `/goal`.

## Runtime Amendment Orchestration

When a running generation writes `control.amendment.proposed`, the orchestrator
must not treat the event as completion evidence. It must either apply the
reviewed amendment or stop for human approval.

Use:

```bash
python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/amendment_orchestrator.py --run-dir docs/cybernetics/runs/<slug>
```

The amendment orchestrator:

1. validates the current JSON control chain;
2. reads unresolved amendment proposals for `run.control.json.current_generation`;
3. stops with `HumanApprovalRequired` if the proposal changes semantic base,
   required outcomes, or authority;
4. refuses to exceed `max_auto_amendment_rounds`;
5. creates a reviewed `gen-N+1` amendment generation for anchor-preserving
   proposals;
6. updates `run.control.json.current_generation`;
7. compiles the new generation runtime;
8. appends `control.amendment.approved`.

Generation selection comes only from `run.control.json.current_generation`.
Do not pass a separate generation override that can diverge from the manifest.

## Workflow

Read `references/orchestration-protocol.md` for the control-layer map, then use
the state machine below. Before each transition, run
`scripts/orchestration_guard.py` with the matching `--state` when available. If
the guard fails, stop and report the next allowed action from the guard.

### Validate Inputs

The requirements analysis is acceptable only when:

- `Requirements Analysis Status: Complete`;
- `What the User Approved: Approved`;
- routing or requirements recorded Level 3/4 or full pre-goal fit.

If requirements analysis is incomplete or What the User Approved is missing/not Approved, stop
before design.

### Determine Artifact Paths

Derive the run directory from the requirements control path unless the user specifies paths.

From:

```text
docs/cybernetics/runs/YYYY-MM-DD-<slug>/requirements.control.json
```

Use:

```text
docs/cybernetics/runs/YYYY-MM-DD-<slug>/design.control.json
docs/cybernetics/runs/YYYY-MM-DD-<slug>/goal.control.json
docs/cybernetics/runs/YYYY-MM-DD-<slug>/plan.control.json
docs/cybernetics/runs/YYYY-MM-DD-<slug>/review.control.json
docs/cybernetics/runs/YYYY-MM-DD-<slug>/runtime.control.json
docs/cybernetics/runs/YYYY-MM-DD-<slug>/progress.jsonl
docs/cybernetics/runs/YYYY-MM-DD-<slug>/runtime-status.json
docs/cybernetics/runs/YYYY-MM-DD-<slug>/final-report.json
docs/cybernetics/runs/YYYY-MM-DD-<slug>/evidence/
```

The design, goal, plan, review, runtime control JSON, and runtime outputs must use the same run directory. This keeps queue-friendly `/goal` commands emitted by `$analyzing-cybernetic-requirements` stable. If the requested path is ambiguous or lacks a deterministic slug, stop and ask for the smallest path decision; keep the slug unresolved until the decision exists.

Do not use Markdown orchestration status as official control input. If historical Markdown status exists, treat it as non-authoritative background only.

## Design Dispatch Rule

When required design is required, the orchestrator must invoke or request `$designing-cybernetic-solutions` before goal writing.

The orchestrator owns:

- sequencing
- artifact path derivation
- lifecycle checks
- source-contract checks
- blocking when design is missing or invalid
- downstream propagation of the design path
- downstream propagation and validation of any output contract

The orchestrator does not own solution-model synthesis.

The orchestrator does not own output-contract synthesis.

Do not synthesize solution design inside the orchestrator. Do not treat solution design as narrow formatting fallback.

If `$designing-cybernetic-solutions` is unavailable when required design is required, stop and report the missing downstream skill.

Design artifacts with status `Candidate`, `Reviewed`, or `Approved` may enter downstream stages when all are true:

- the artifact was produced by `$designing-cybernetic-solutions` or explicitly provided by the user;
- it references the requirements analysis in `Source Contracts`;
- it has no blocking open design questions;
- if What the User Approved records `How this should be answered` or `What is not enough`, the design records a Required Answer Path check that preserves the approved answer path and avoids what is not enough;
- final review will check Design Match and Required Answer Path when What the User Approved records how this should be answered.

If any design artifact exists, propacheck its path to goal writing, execution-policy writing, review, and runtime compilation, even when required design is satisfied or no longer required.

## Required Answer Path Check

Before goal writing, validate that design preserves the approved answer path when What the User Approved records how this should be answered.

The design must instantiate the approved how this should be answered. It must not replace the approved answer path with what the user marked as not enough because the substitute is easier to run or verify.

If the approved how this should be answered cannot be instantiated, return to requirements for revision. Do not ask the user to review downstream goal or plan artifacts as compensation.

## Non-Fallback Rule

The orchestrator may emulate narrow formatting only for downstream cybernetic artifacts where this skill explicitly allows it.

It must not emulate:

- requirements analysis
- solution design synthesis
- execution-policy workflow
- independent review
- runtime compilation guard

If any non-emulatable stage is required and unavailable, stop and report the missing dependency.

## Orchestration State Machine

| Current State | Required condition | Next Action | Forbidden Action |
|---|---|---|---|
| `RequirementsMissing` | requirements absent, incomplete, or What the User Approved missing/not Approved | `Blocked` / `ReturnToRequirementsAnalysis` | design / goal / policy / review / runtime compile |
| `RequirementsComplete` | requirements Complete and What the User Approved Approved; required design required and design missing | `RunDesign` | goal writing |
| `DesignReady` | design exists, references requirements, has no blocking open questions, and passes Required Answer Path Check when What the User Approved records how this should be answered | `RunGoalWriting` | execution policy |
| `GoalReady` | `goal.control.json` exists and references requirements plus any design path | `RunExecutionPolicy` | review |
| `PolicyReady` | execution policy exists, references requirements, goal, any design path, and records selected execution work assignment | `RunReview` | runtime compile |
| `ReviewNeedsRevision` | review verdict/status is `NeedsRevision` / `Needs Revision`, `Dirty`, `Needs Re-review`, or `Needs Independent Review` | route by NeedsRevision Routing Rule or obtain independent review | runtime compile |
| `ReviewApproved` | review is Approved and Final Observer allows approval | `RunRuntimeCompile` | execution |
| `RuntimeGoalReady` | `runtime.control.json` and final short `/goal` pointer are compiled | output command | start `/goal` |
| `Blocked` | any required check fails | report blocker | continue |

### Stage Responsibilities

- `RunDesign`: invoke/request `$designing-cybernetic-solutions` when required design is required or a design artifact must be validated.
- `RunGoalWriting`: invoke/request `$writing-cybernetic-goals`; goal writing consumes requirements and any required design.
- `RunExecutionPolicy`: invoke/request `$writing-cybernetic-execution-policies`; the orchestrator passes work assignment decisions through and does not choose them.
- `RunReview`: invoke/request `$reviewing-cybernetic-control-structures`; use authorized independent review, and apply Final Observer discipline after substantive mutations.
- `RunRuntimeCompile`: invoke/request `$compiling-cybernetic-runtime-goals`; runtime compilation must pass the compiler guard and must not start `/goal`.

If a required downstream skill or required Superpowers workflow is unavailable,
stop and report the missing dependency. If review returns `Needs Revision`,
`Dirty`, `Needs Re-review`, or `Needs Independent Review`, return to the
required prior stage instead of compiling runtime `/goal`.

### Final Output

Output:

- artifact paths
- review status
- short control summary
- final runtime `/goal` command if approved
- blocked status if not approved

Do not start `/goal`.

## Output And Final Checks Reference

After the orchestration state machine reaches `RuntimeGoalReady` or `Blocked`,
read `references/output-and-final-checks.md` for response-only output shapes,
the final validation checklist, common mistakes, and runtime `/goal`
precondition reminders. Do not write those response-only prompts into control
artifacts.
