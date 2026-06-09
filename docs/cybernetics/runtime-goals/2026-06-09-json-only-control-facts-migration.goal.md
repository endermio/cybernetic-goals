# Runtime Goal

## Approved Control Chain

- Requirements: `docs/cybernetics/requirements/2026-06-09-json-only-control-facts-migration.md`
- Design: `docs/cybernetics/designs/2026-06-09-json-only-control-facts-migration.md`
- Goal: `docs/cybernetics/goals/2026-06-09-json-only-control-facts-migration.md`
- Execution policy: `docs/cybernetics/plans/2026-06-09-json-only-control-facts-migration.md`
- Review: `docs/cybernetics/control-reviews/2026-06-09-json-only-control-facts-migration.md`

## Runtime Execution Rule

Execute the approved execution policy under the approved control chain. Do not reinterpret what the user approved, how this should be answered, what counts as done, final answer format, who does the work, checks, or control strategy.
Treat What the User Approved as the source for primary object, requested transformation, non-goals, how this should be answered, what is not enough, work covered in this run, what the agent may do, forbidden actions, purpose feedback, where the result must show up, what counts as done, final answer format, why this process is needed, and known assumptions.

- Who does the work: `Parallel subagent-driven`
- Selected agent workflow: `superpowers-dispatching-parallel-agents`
- Subagent execution mode: `parallel-max-safe`
- Max concurrent subagents: `auto`

## Required Sections To Read

- Requirements `docs/cybernetics/requirements/2026-06-09-json-only-control-facts-migration.md`: `What the User Approved`, `How We Know The User Purpose Was Met`, `Where The Result Must Show Up`, `Final Answer Format`.
- Design `docs/cybernetics/designs/2026-06-09-json-only-control-facts-migration.md`: `Answer Method Check`, `Final Answer Format Design`, `Design-to-Goal Mapping`, `Design-to-Execution Mapping`.
- Goal `docs/cybernetics/goals/2026-06-09-json-only-control-facts-migration.md`: `Success Condition`, `What Counts As Done`, `Work Covered And Allowed Actions Contract`, `How We Know The User Purpose Was Met`, `Where The Result Must Show Up`, `Final Answer Format`.
- Execution policy `docs/cybernetics/plans/2026-06-09-json-only-control-facts-migration.md`: `Work Coverage And Action Limits Matrix`, `Steps That Make The Result True`, `Action That Can Make It Done`, `Candidate Plan Tasks`, `Who Does The Work / Context Use`, `Subagent execution mode`, `Parallel wave matrix`, `Conflict / lock model`, `Failure policy`, `Phase Checks`, `Progress Log Rules`, `User Purpose Strategy`, `Where The Result Must Show Up`, `Check / Evidence Rules`.
- Review `docs/cybernetics/control-reviews/2026-06-09-json-only-control-facts-migration.md`: `Design Answer Method Check`, `Work Covered And Allowed Actions Check`, `Parallel Agent Safety Check`, `Answer Path Check`, `What Counts As Done Check`, `User Purpose Evidence Check`, `Result Placement Check`, `Who Does The Work / Context Use`, `Final Observer Check`.

## Runtime Discipline

- Use `$superpowers:executing-plans` discipline against the approved execution policy.
- Use `$superpowers:systematic-debugging` for unclear or repeated failures.
- Use `$superpowers:verification-before-completion` before claiming completion.
- Follow the approved work assignment and agent workflow recorded in the execution policy.
- Because the selected agent workflow is `superpowers-dispatching-parallel-agents`, use `$superpowers:dispatching-parallel-agents` only for the approved independent work packages in the current wave, under the plan's required-step frontier, lock, barrier, failure, and main-agent integration rules.
- If `Subagent execution mode` is `serial-single-active`, run exactly one execution subagent at a time and integrate before launching the next.
- If `Subagent execution mode` is `parallel-max-safe`, launch only the current approved wave up to the approved cap, after dependencies are satisfied and conflict locks are disjoint; integrate at the approved barrier before launching the next wave.
- Treat subagent work as governed by the execution policy's bounded delegation protocol and integration checks.
- Treat approved evidence checks, checks, and evidence channels as evidence, not objectives.

## Final Report Required Fields

- goal achieved: yes/no
- what counts as done met: yes/no
- evidence needed to call it done
- required answer path coverage and step evidence
- answer method completion evidence when requirements/design define how this should be answered
- if no: not done reason
- if no: action that can make it done attempted or proof of impossibility
- if no: smallest next action that can make it done
- work covered in this run
- work coverage: complete / partial / unavailable / explicitly bounded by what the user approved
- executed
- prepared-only
- forbidden-not-executed
- explicitly out-of-scope by what the user approved
- user purpose evidence status and highest purpose-relevant evidence observed
- result places covered, actions completed or justified, old behavior checked, and pending or unknown places when result placement applies

## Stop Rule

If any referenced artifact is missing, not approved, inconsistent, or insufficient for runtime execution, stop and report the smallest required human decision.
