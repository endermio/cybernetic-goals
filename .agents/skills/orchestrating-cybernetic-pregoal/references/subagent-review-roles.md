# Subagent Review Roles for Pre-goal Compilation

Use these roles only when the user explicitly authorizes subagents.

## Requirement Traceability Reviewer

Input: `requirements.control.json`, `run.control.json`, the current generation
runtime strategy, and any expanded design/goal/plan artifacts named by the run.

Check:

- Every confirmed human decision appears in the current generation strategy or
  in the expanded artifact that owns it.
- Every confirmed human decision that affects structure appears in the solution
  model when a solution model is required.
- No confirmed meaning decision is weakened, reworded into ambiguity, or converted into an execution option.
- No new requirement appears without source.

## Intent Preservation / Obligation Preservation Reviewer

Input: `requirements.control.json`, `run.control.json`, current generation
runtime strategy, and any expanded artifacts named by the run.

Check:

- Required outcomes remain required outcomes through source requirements,
  current generation steps, work packages, verifier, and any expanded artifacts.
- Required implementation is not downgraded into readiness, future work,
  allowed action, prepare-only handling, or compatibility-only behavior.
- The review distinguishes tactical execution freedom from obligation removal.
- A required `/api/v2` implementation is not accepted as legacy Drogon
  compatibility readiness.
- Drift findings identify the earliest artifact that introduced the drift:
  requirements, design, goal, plan, review, run, or current generation.

Verdict:

- `Approved`: no intent drift or obligation downgrade.
- `NeedsRevision`: repairable drift exists; route to the named stage and
  rerun review after revision.
- `Blocked`: the drift cannot be repaired without a human decision, missing
  dependency, or unavailable fact.

## Solution Design Match Reviewer

Input: `requirements.control.json`, `run.control.json`, current generation
strategy, and expanded design/goal/plan artifacts when present.

Check:

- Design preserves requirements analysis meaning.
- Design defines objects/actors/roles, relationships, flows, limits, interfaces/contracts, failure model, and evidence model when relevant.
- Current generation strategy preserves design rules that cannot change.
- Runtime strategy does not redesign the solution model.
- Tactical degrees of freedom are not frozen as meaning rules that cannot change unless the design explicitly says so.

## Control Contract Reviewer

Input: `requirements.control.json`, `run.control.json`, current generation
runtime strategy, and `goal.control.json` when the run names one.

Check:

- Current generation has success conditions, limits, verification places, stop
  conditions, and source of truth.
- Runtime `/goal` does not generate or approve its own plan.
- Requirement meaning stays separate from execution tactics.

## Execution Policy / Cadence Reviewer

Input: current generation strategy plus expanded plan/design artifacts when the
run names them.

Check:

- Strategy contains dependency matrix or equivalent sequencing.
- Strategy defines work size, evidence budget, cadence, and destructive
  intermediate-state policy when relevant.
- Strategy defines batch-end openable or verifiable state.
- Strategy avoids both tiny evidence-check-bound steps and huge unobservable batches.
- Broad verification is assigned to integration or final checks unless justified.

## Evidence check / Evidence Governance Reviewer

Input: current generation strategy plus expanded artifacts when present.

Check:

- Approved evidence checks, checks, and evidence channels are treated as evidence checks, not objectives.
- Old evidence checks may be preserved, retired, or rewritten according to explicit rules.
- Target-state evidence dominates brittle realization-detail evidence checks.
- Evidence check hierarchy is explicit and stays in core cybernetic vocabulary.

## Runtime Limit Reviewer

Input: requirements, run control, current generation runtime, generation review
when required, and proposed runtime `/goal`.

Check:

- Runtime `/goal` only points to `runtime.control.json`.
- Runtime `/goal` does not rewrite requirements, plan, evidence checks, or review.
- Runtime `/goal` does not rewrite required solution design.
- `runtime.control.json` references requirements, run control, current
  generation, required review, and any expanded artifacts named by the run.
- Runtime execution stops if control JSON conflicts or becomes insufficient.
