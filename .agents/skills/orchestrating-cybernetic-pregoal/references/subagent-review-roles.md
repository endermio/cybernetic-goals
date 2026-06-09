# Subagent Review Roles for Pre-goal Compilation

Use these roles only when the user explicitly authorizes subagents.

## Requirement Traceability Reviewer

Input: requirements analysis brief, solution design when present, goal file, execution policy.

Check:

- Every confirmed human decision appears in the goal and plan.
- Every confirmed human decision that affects structure appears in the solution design.
- No confirmed meaning decision is weakened, reworded into ambiguity, or converted into an execution option.
- No new requirement appears without source.

## Solution Design Match Reviewer

Input: requirements analysis brief, solution design, goal file, execution policy.

Check:

- Design preserves requirements analysis meaning.
- Design defines objects/actors/roles, relationships, flows, limits, interfaces/contracts, failure model, and evidence model when relevant.
- Goal preserves design rules that cannot change.
- Plan does not redesign the solution model.
- Tactical degrees of freedom are not frozen as meaning rules that cannot change unless the design explicitly says so.

## Control Contract Reviewer

Input: requirements analysis brief, solution design when present, and goal file.

Check:

- Goal has success conditions, limits, rules that cannot change, verification places, stop conditions, and source of truth.
- Goal does not ask runtime `/goal` to generate or approve its own plan.
- Goal separates requirement meaning from execution tactics.

## Execution Policy / Cadence Reviewer

Input: solution design when present, goal file, and execution policy.

Check:

- Plan contains dependency matrix.
- Plan defines work size and evidence check budget.
- Plan defines batch cadence.
- Plan defines destructive intermediate-state policy.
- Plan defines batch-end openable or verifiable state.
- Plan avoids both tiny evidence check-bound steps and huge unobservable batches.
- Broad verification is assigned to integration or final checks unless justified.

## Evidence check / Evidence Governance Reviewer

Input: solution design when present, goal file, and execution policy.

Check:

- Approved evidence checks, checks, and evidence channels are treated as evidence checks, not objectives.
- Old evidence checks may be preserved, retired, or rewritten according to explicit rules.
- Target-state evidence dominates brittle realization-detail evidence checks.
- Evidence check hierarchy is explicit and stays in core cybernetic vocabulary.

## Runtime Limit Reviewer

Input: all artifacts plus proposed runtime `/goal`.

Check:

- Runtime `/goal` only executes approved artifacts.
- Runtime `/goal` does not rewrite requirements, plan, evidence checks, or review.
- Runtime `/goal` does not rewrite required solution design.
- Runtime `/goal` references requirements analysis, required design, goal, plan, and review.
- Runtime `/goal` stops if artifacts conflict or become insufficient.
