# Subagent Review Roles for Pre-goal Compilation

Use these roles only when the user explicitly authorizes subagents.

## Requirement Traceability Reviewer

Input: `requirements.control.json`, `design.control.json` when present, `goal.control.json`, and `plan.control.json`.

Check:

- Every confirmed human decision appears in the goal and plan.
- Every confirmed human decision that affects structure appears in the solution design.
- No confirmed meaning decision is weakened, reworded into ambiguity, or converted into an execution option.
- No new requirement appears without source.

## Solution Design Match Reviewer

Input: `requirements.control.json`, `design.control.json`, `goal.control.json`, and `plan.control.json`.

Check:

- Design preserves requirements analysis meaning.
- Design defines objects/actors/roles, relationships, flows, limits, interfaces/contracts, failure model, and evidence model when relevant.
- Goal preserves design rules that cannot change.
- Plan does not redesign the solution model.
- Tactical degrees of freedom are not frozen as meaning rules that cannot change unless the design explicitly says so.

## Control Contract Reviewer

Input: `requirements.control.json`, `design.control.json` when present, and `goal.control.json`.

Check:

- Goal has success conditions, limits, rules that cannot change, verification places, stop conditions, and source of truth.
- Goal does not ask runtime `/goal` to generate or approve its own plan.
- Goal separates requirement meaning from execution tactics.

## Execution Policy / Cadence Reviewer

Input: `design.control.json` when present, `goal.control.json`, and `plan.control.json`.

Check:

- Plan contains dependency matrix.
- Plan defines work size and evidence check budget.
- Plan defines batch cadence.
- Plan defines destructive intermediate-state policy.
- Plan defines batch-end openable or verifiable state.
- Plan avoids both tiny evidence check-bound steps and huge unobservable batches.
- Broad verification is assigned to integration or final checks unless justified.

## Evidence check / Evidence Governance Reviewer

Input: `design.control.json` when present, `goal.control.json`, and `plan.control.json`.

Check:

- Approved evidence checks, checks, and evidence channels are treated as evidence checks, not objectives.
- Old evidence checks may be preserved, retired, or rewritten according to explicit rules.
- Target-state evidence dominates brittle realization-detail evidence checks.
- Evidence check hierarchy is explicit and stays in core cybernetic vocabulary.

## Runtime Limit Reviewer

Input: all approved control JSON plus proposed runtime `/goal`.

Check:

- Runtime `/goal` only points to `runtime.control.json`.
- Runtime `/goal` does not rewrite requirements, plan, evidence checks, or review.
- Runtime `/goal` does not rewrite required solution design.
- `runtime.control.json` references requirements analysis, required design, goal, plan, and review control JSON.
- Runtime execution stops if control JSON conflicts or becomes insufficient.
