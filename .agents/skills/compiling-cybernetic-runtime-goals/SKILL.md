---
name: compiling-cybernetic-runtime-goals
description: 'Use when requirements, any required design, goal control, execution policy, and approved review exist, and runtime.control.json plus a short /goal pointer must be checked or emitted before execution.'
---

# Compiling Cybernetic Runtime Goals

## Overview

Produce `runtime.control.json` and a short executable `/goal` pointer from approved JSON control files.

Inputs:

- `requirements.control.json` with status Complete
- What the User Approved: Approved in the requirements analysis
- `design.control.json`, when required design was required or a design exists
- `goal.control.json`
- `plan.control.json`
- `review.control.json` with status Approved

This skill is a thin compiler. It must not rewrite the approved work chain or inline control discipline into the user-entered `/goal`.

Official persistent control facts are JSON only. Historical Markdown may be read as non-authoritative background, but do not create or compile Markdown as official guard, compiler, runtime, or long-term dual-path control input.

Use `scripts/control_chain_guard.py` and `scripts/compile_runtime_goal.py` when available.

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

This skill does not invoke runtime execution.

The user-entered `/goal` must be pointer-only and length-bounded. It points to `runtime.control.json` and names `.agents/skills/using-control-json`; the JSON contract indexes the approved control chain and required sections to read. Do not inline What the User Approved, user-purpose evidence, result-placement, what-counts-as-done, work assignment, evidence check governance, review discipline, or subagent protocol prose into the `/goal` hot path.

## Preconditions

Do not output `/goal` unless:

- requirements analysis status is Complete;
- requirements analysis includes `What the User Approved: Approved`;
- `goal.control.json` exists;
- solution design exists when required design was required or a design artifact exists;
- execution policy exists;
- review status is Approved;
- if What the User Approved records an answering method or how this should be answered, solution design includes `Answer Method Check`;
- if What the User Approved records an answering method or how this should be answered, review records `Design answer method check: yes` in Review Independence and includes meaningful `Design Answer Method Check` findings;
- review records `Who does the work / context use: yes` in Review Independence;
- review includes meaningful `Who Does The Work / Context Use` findings;
- when subagent-driven work assignment is selected, execution policy records `Subagent execution mode` and `Max concurrent subagents`;
- when a Superpowers agent workflow is selected, execution policy uses a compatible mode: `$superpowers:subagent-driven-development` only for `serial-single-active`, and `$superpowers:dispatching-parallel-agents` only for `parallel-max-safe`;
- when subagent-driven work assignment is selected, review records `Parallel agent safety check: yes` in Review Independence and includes meaningful `Parallel Agent Safety Check` findings;
- goal includes a compact `How We Know The User Purpose Was Met`;
- review records `User purpose evidence check: yes` in Review Independence;
- review includes meaningful `User Purpose Evidence Check` findings;
- goal includes a compact `Where The Result Must Show Up`; simple direct tasks may record `result-placement not applicable with justification`;
- execution policy includes `Where The Result Must Show Up`;
- review records `Result placement check: yes` in Review Independence;
- review includes meaningful `Result Placement Check` findings;
- goal includes a compact `What Counts As Done`;
- goal `What Counts As Done` includes a required answer path reference;
- execution policy includes `Steps That Make The Result True`;
- execution policy includes `Action That Can Make It Done`;
- execution policy `Candidate Plan Tasks` map work packages to `Required step(s)`;
- review records `What counts as done check: yes` in Review Independence;
- review includes meaningful `What Counts As Done Check` findings;
- review records `answer path check: yes` in Review Independence;
- review includes meaningful `Answer Path Check` findings;
- goal includes a compact `Work Covered And Allowed Actions Contract`;
- execution policy includes `Work Coverage And Action Limits Matrix`;
- review records `Work covered in this run and authority check: yes` in Review Independence;
- review includes meaningful `Work Covered And Allowed Actions Check` findings;
- review includes `Final Independent Check`;
- final observer check allows approval;
- any substantive post-review change has final re-review recorded;
- any deterministic-only exception has guard evidence recorded;
- files reference the same feature and do not visibly conflict;
- runtime `/goal` will not need to write or approve a new plan.
- runtime `/goal` will not need to create or revise solution design.
- runtime `/goal` will not need to invent or replace the final output contract.
- runtime `/goal` will not need to invent or replace work assignment.

## Runtime Control JSON

The contract artifact must be `docs/cybernetics/runs/<slug>/runtime.control.json`, not a long copied prompt. It must include:

- approved control chain paths for requirements, design when present, goal, execution policy, and review;
- a runtime execution rule that forbids reinterpreting the what the user approved, answering method, answer method, what counts as done, output contract, work assignment, evidence checks, or control strategy;
- a What the User Approved rule that treats primary object, requested transformation, non-goals, answering method, what is not enough, how this should be answered, work covered in this run, what the agent may do, forbidden actions, user purpose evidence, where the result must show up, what counts as done, output contract, why this process is needed, and known assumptions as source-owned by requirements;
- required sections to read, including `What the User Approved`, design `Answer Method Check` when design exists, `What Counts As Done`, `Work Covered And Allowed Actions Contract`, `How We Know The User Purpose Was Met`, `Where The Result Must Show Up`, `Work Coverage And Action Limits Matrix`, `Steps That Make The Result True`, `Action That Can Make It Done`, `Candidate Plan Tasks`, `Who Does The Work / Context Use`, workflow compatibility, subagent execution mode/concurrency sections, `Design Answer Method Check`, `Work Covered And Allowed Actions Check`, `Parallel Agent Safety Check`, `Answer Path Check`, `What Counts As Done Check`, `User Purpose Evidence Check`, `Result Placement Check`, and `Final Independent Check`;
- final report fields: `goal achieved: yes/no`, `what counts as done met: yes/no`, evidence needed to call it done, required answer path coverage and step evidence, answer method completion evidence when requirements/design define how this should be answered, not done reason when no, action that can make it done attempted or proof of impossibility when no, smallest next action that can make it done when no, work covered in this run, work coverage, executed, prepared-only, forbidden-not-executed, explicitly out-of-scope by what the user approved, user purpose evidence status and highest purpose-relevant evidence observed, and result places covered, actions completed or justified, old behavior checked, and pending or unknown places when result-placement applies;
- a stop rule for missing, unapproved, inconsistent, or insufficient referenced artifacts.

The final `/goal` command must only point to `runtime.control.json` and tell runtime Codex to use `.agents/skills/using-control-json`.

## Scripted Compilation

Preferred:

```bash
python3 .agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py \
  --run-dir docs/cybernetics/runs/YYYY-MM-DD-feature
```

The official compiler input is the JSON run directory. Do not combine Markdown artifact inputs or legacy Markdown runtime output with official runtime compilation.

Do not use `--skip-guard` for official runtime `/goal` compilation. It is only for internal validation and requires the explicit `--i-understand-this-bypasses-phase-checks` acknowledgement.

## Output Format

These output formats are response-only. Do not write `$skill ...` commands, runtime `/goal` prompts, or conversational next-step prompts into requirements, design, goal, plan, review, or runtime control JSON.

### Approved runtime control and command

```markdown
Runtime control JSON written:
`docs/cybernetics/runs/YYYY-MM-DD-feature/runtime.control.json`

Use this /goal:

```text
/goal Use .agents/skills/using-control-json and execute docs/cybernetics/runs/YYYY-MM-DD-feature/runtime.control.json. If the JSON is missing, invalid, inconsistent, or insufficient, stop and report the smallest required human decision.
```

Preflight:
- Requirements analysis: Complete
- What the User Approved: Approved
- Goal: present
- Solution design: present or not required
- Execution policy: present
- Review: Approved
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
- [ ] Review records `Who does the work / context use: yes` in Review Independence.
- [ ] Review includes meaningful `Who Does The Work / Context Use` findings.
- [ ] Subagent-driven work assignment records `Subagent execution mode` and `Max concurrent subagents`.
- [ ] Selected Superpowers workflow supports the approved subagent execution mode.
- [ ] Subagent-driven work assignment has `Parallel Agent Safety Check` review evidence.
- [ ] Final Independent Check is present and allows approval.
- [ ] `runtime.control.json` references all approved control JSON files.
- [ ] `runtime.control.json` indexes the goal's Final Output Contract when present or required.
- [ ] `runtime.control.json` preserves the approved work assignment through the plan section index.
- [ ] `runtime.control.json` preserves the What the User Approved through the requirements section index.
- [ ] `runtime.control.json` indexes design `Answer Method Check` and review `Design Answer Method Check` when design exists.
- [ ] `runtime.control.json` includes final report fields for work coverage and action limits, user-purpose evidence, result-placement, and what-counts-as-done claim calibration.
- [ ] `runtime.control.json` indexes the approved Steps That Make The Result True and review check section.
- [ ] The user-entered `/goal` is pointer-only and length-bounded.
- [ ] The user-entered `/goal` does not inline What the User Approved, user-purpose evidence, result-placement, what-counts-as-done, work assignment, evidence check-governance, review, or subagent protocol prose.
- [ ] The final `/goal` does not ask runtime Codex to write a new plan.
- [ ] The final `/goal` does not ask runtime Codex to create or revise solution design.
- [ ] `runtime.control.json` includes executing, debugging, and completion-verification discipline.
- [ ] If guard or preconditions fail, the response includes a response-only next step and no final `/goal`.
- [ ] The skill did not execute target work.
