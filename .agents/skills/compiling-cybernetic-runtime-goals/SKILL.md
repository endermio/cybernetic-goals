---
name: compiling-cybernetic-runtime-goals
description: 'Use when requirements, any required design, goal contract, execution policy, and approved control review exist, and a runtime goal contract plus short /goal pointer must be checked or emitted before execution.'
---

# Compiling Cybernetic Runtime Goals

## Overview

Produce a runtime goal contract artifact and a short executable `/goal` pointer from approved approved files.

Inputs:

- requirements analysis brief with status Complete
- What the User Approved: Approved in the requirements analysis
- solution design, when required design was required or a design exists
- goal contract
- execution policy / plan
- control review with status Approved

This skill is a thin compiler. It must not rewrite the approved work chain or inline control discipline into the user-entered `/goal`.

Use `scripts/control_chain_guard.py` and `scripts/compile_runtime_goal.py` when available.

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

This skill does not invoke runtime execution.

The user-entered `/goal` must be pointer-only and length-bounded. It points to a runtime goal contract artifact, and the contract indexes the approved control chain and required sections to read. Do not inline What the User Approved, user-purpose evidence, result-placement, what-counts-as-done, work assignment, evidence check governance, review discipline, or subagent protocol prose into the `/goal` hot path.

## Preconditions

Do not output `/goal` unless:

- requirements analysis status is Complete;
- requirements analysis includes `What the User Approved: Approved`;
- goal contract exists;
- solution design exists when required design was required or a design artifact exists;
- execution policy exists;
- control review status is Approved;
- if What the User Approved records an answering method or how this should be answered, solution design includes `Answer Method Check`;
- if What the User Approved records an answering method or how this should be answered, control review records `Design answer method check: yes` in Review Independence and includes meaningful `Design Answer Method Check` findings;
- control review records `Who does the work / context use: yes` in Review Independence;
- control review includes meaningful `Who Does The Work / Context Use` findings;
- when subagent-driven work assignment is selected, execution policy records `Subagent execution mode` and `Max concurrent subagents`;
- when a Superpowers agent workflow is selected, execution policy uses a compatible mode: `$superpowers:subagent-driven-development` only for `serial-single-active`, and `$superpowers:dispatching-parallel-agents` only for `parallel-max-safe`;
- when subagent-driven work assignment is selected, control review records `Subagent concurrency check: yes` in Review Independence and includes meaningful `Subagent Concurrency Check` findings;
- goal includes a compact `How We Know The User Purpose Was Met`;
- control review records `User purpose evidence check: yes` in Review Independence;
- control review includes meaningful `User Purpose Evidence Check` findings;
- goal includes a compact `Where The Result Must Show Up`; simple direct tasks may record `result-placement not applicable with justification`;
- execution policy includes `Where The Result Must Show Up`;
- control review records `Result placement check: yes` in Review Independence;
- control review includes meaningful `Result Placement Check` findings;
- goal includes a compact `What Counts As Done`;
- goal `What Counts As Done` includes a required answer path reference;
- execution policy includes `Steps That Make The Result True`;
- execution policy includes `Action That Can Make It Done`;
- execution policy `Candidate Plan Tasks` map work packages to `Required step(s)`;
- control review records `What counts as done check: yes` in Review Independence;
- control review includes meaningful `What Counts As Done Check` findings;
- control review records `answer path check: yes` in Review Independence;
- control review includes meaningful `Answer Path Check` findings;
- goal includes a compact `Work Covered And Allowed Actions Contract`;
- execution policy includes `Work Coverage And Action Limits Matrix`;
- control review records `Work covered in this run and authority fidelity: yes` in Review Independence;
- control review includes meaningful `Work Covered And Allowed Actions Check` findings;
- control review includes `Final Independent Check`;
- final observer check allows approval;
- any substantive post-review change has final re-review recorded;
- any deterministic-only exception has guard evidence recorded;
- files reference the same feature and do not visibly conflict;
- runtime `/goal` will not need to write or approve a new plan.
- runtime `/goal` will not need to create or revise solution design.
- runtime `/goal` will not need to invent or replace the final output contract.
- runtime `/goal` will not need to invent or replace work assignment.

## Runtime Goal Contract

The contract artifact must be an index-style goal contract, not a long copied prompt. It must include:

- approved control chain paths for requirements, design when present, goal, execution policy, and control review;
- a runtime execution rule that forbids reinterpreting the what the user approved, answering method, answer method, what counts as done, output contract, work assignment, evidence checks, or control strategy;
- a What the User Approved rule that treats primary object, requested transformation, non-goals, answering method, what is not enough, how this should be answered, work covered in this run, what the agent may do, forbidden actions, user purpose evidence, where the result must show up, what counts as done, output contract, workflow fit, and known assumptions as source-owned by requirements;
- required sections to read, including `What the User Approved`, design `Answer Method Check` when design exists, `What Counts As Done`, `Work Covered And Allowed Actions Contract`, `How We Know The User Purpose Was Met`, `Where The Result Must Show Up`, `Work Coverage And Action Limits Matrix`, `Steps That Make The Result True`, `Action That Can Make It Done`, `Candidate Plan Tasks`, `Who Does The Work / Context Use`, workflow compatibility, subagent execution mode/concurrency sections, `Design Answer Method Check`, `Work Covered And Allowed Actions Check`, `Subagent Concurrency Check`, `Answer Path Check`, `What Counts As Done Check`, `User Purpose Evidence Check`, `Result Placement Check`, and `Final Independent Check`;
- final report fields: `goal achieved: yes/no`, `what counts as done met: yes/no`, evidence needed to call it done, required answer path coverage and step evidence, answer method completion evidence when requirements/design define how this should be answered, not done reason when no, action that can make it done attempted or proof of impossibility when no, smallest next action that can make it done when no, work covered in this run, work coverage, executed, prepared-only, forbidden-not-executed, explicitly out-of-scope by what the user approved, user purpose evidence status and highest purpose-relevant evidence observed, and result places covered, actions completed or justified, old behavior checked, and pending or unknown places when result-placement applies;
- a stop rule for missing, unapproved, inconsistent, or insufficient referenced artifacts.

The final `/goal` command must only point to this runtime goal contract and tell runtime Codex to read it first.

## Scripted Compilation

Preferred:

```bash
python3 .agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py \
  --requirements docs/cybernetics/requirements/YYYY-MM-DD-feature.md \
  --design docs/cybernetics/designs/YYYY-MM-DD-feature.md \
  --goal docs/cybernetics/goals/YYYY-MM-DD-feature.md \
  --plan docs/cybernetics/plans/YYYY-MM-DD-feature.md \
  --review docs/cybernetics/control-reviews/YYYY-MM-DD-feature.md \
  --out docs/cybernetics/runtime-goals/YYYY-MM-DD-feature.goal.md
```

The `--out` path must end with `.goal.md`; the output file is a runtime goal contract, not a copyable command transcript.

Do not use `--skip-guard` for official runtime `/goal` compilation. It is only for internal validation and requires the explicit `--i-understand-this-bypasses-phase-gates` acknowledgement.

## Output Format

These output formats are response-only. Do not write `$skill ...` commands, runtime `/goal` prompts, or conversational next-step prompts into requirements, design, goal, plan, or review artifacts.

### Approved runtime contract and command

```markdown
Runtime goal contract written:
`docs/cybernetics/runtime-goals/YYYY-MM-DD-feature.goal.md`

Use this /goal:

```text
/goal Execute the runtime goal contract at docs/cybernetics/runtime-goals/YYYY-MM-DD-feature.goal.md. Read it first and follow it exactly. If any referenced artifact is missing, not approved, or inconsistent, stop and report the smallest required human decision.
```

Preflight:
- Requirements analysis: Complete
- What the User Approved: Approved
- Goal: present
- Solution design: present or not required
- Execution policy: present
- Control review: Approved
- Runtime command: pointer-only and length-bounded
```

### Blocked runtime compilation

Use this when `scripts/control_chain_guard.py` fails or any precondition is not satisfied.

```markdown
Runtime goal compilation blocked.

Reason:
- ...

Guard result:
- `FAIL`
- `NEXT: ...` if emitted by the guard

Response-only next step:
- For Level 3/4 or full pre-goal work: return to `$orchestrating-cybernetic-pregoal` with the failing guard output.
- For an explicit manual chain: run the smallest missing upstream step, such as `$designing-cybernetic-solutions`, `$writing-cybernetic-goals`, `$writing-cybernetic-execution-policies`, or `$reviewing-cybernetic-control-structures`.
- Do not output a runtime `/goal` until the guard passes and review is `Approved`.
```

Do not create or modify target-work artifacts.

## Validation Checklist

- [ ] Guard passed or equivalent checks passed.
- [ ] Requirements analysis contains What the User Approved: Approved.
- [ ] Design Answer Method Check is reviewed when What the User Approved records an answering method or answer method.
- [ ] No approved file was rewritten.
- [ ] Control review records `Who does the work / context use: yes` in Review Independence.
- [ ] Control review includes meaningful `Who Does The Work / Context Use` findings.
- [ ] Subagent-driven work assignment records `Subagent execution mode` and `Max concurrent subagents`.
- [ ] Selected Superpowers workflow supports the approved subagent execution mode.
- [ ] Subagent-driven work assignment has `Subagent Concurrency Check` review evidence.
- [ ] Final Independent Check is present and allows approval.
- [ ] Runtime goal contract references all approved files.
- [ ] Runtime goal contract indexes the goal's Final Output Contract when present or required.
- [ ] Runtime goal contract preserves the approved work assignment through the plan section index.
- [ ] Runtime goal contract preserves the What the User Approved through the requirements section index.
- [ ] Runtime goal contract indexes design `Answer Method Check` and review `Design Answer Method Check` when design exists.
- [ ] Runtime goal contract includes final report fields for work coverage and action limits, user-purpose evidence, result-placement, and what-counts-as-done claim calibration.
- [ ] Runtime goal contract indexes the approved Steps That Make The Result True and review fidelity section.
- [ ] The user-entered `/goal` is pointer-only and length-bounded.
- [ ] The user-entered `/goal` does not inline What the User Approved, user-purpose evidence, result-placement, what-counts-as-done, work assignment, evidence check-governance, review, or subagent protocol prose.
- [ ] The final `/goal` does not ask runtime Codex to write a new plan.
- [ ] The final `/goal` does not ask runtime Codex to create or revise solution design.
- [ ] Runtime goal contract includes executing, debugging, and completion-verification discipline.
- [ ] If guard or preconditions fail, the response includes a response-only next step and no final `/goal`.
- [ ] The skill did not execute target work.
