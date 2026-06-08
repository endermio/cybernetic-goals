---
name: compiling-cybernetic-runtime-goals
description: 'Use when requirements, any required design, goal contract, execution policy, and approved control review exist, and a runtime goal contract plus short /goal pointer must be checked or emitted before execution.'
---

# Compiling Cybernetic Runtime Goals

## Overview

Produce a runtime goal contract artifact and a short executable `/goal` pointer from approved control artifacts.

Inputs:

- requirements analysis brief with status Complete
- Human Setpoint Approval: Approved in the requirements analysis
- solution design, when Design Gate was required or a design exists
- goal contract
- execution policy / plan
- control review with status Approved

This skill is a thin compiler. It must not rewrite the control structure or inline control discipline into the user-entered `/goal`.

Use `scripts/control_chain_guard.py` and `scripts/compile_runtime_goal.py` when available.

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

This skill does not invoke runtime execution.

The user-entered `/goal` must be pointer-only and length-bounded. It points to a runtime goal contract artifact, and the contract indexes the approved control chain and required sections to read. Do not inline HSA, PFB, RSC, TAP, topology, sensor governance, review discipline, or subagent protocol prose into the `/goal` hot path.

## Preconditions

Do not output `/goal` unless:

- requirements analysis status is Complete;
- requirements analysis includes `Human Setpoint Approval: Approved`;
- goal contract exists;
- solution design exists when Design Gate was required or a design artifact exists;
- execution policy exists;
- control review status is Approved;
- if HSA records an answering method or task skeleton family, solution design includes `Task Skeleton Fidelity`;
- if HSA records an answering method or task skeleton family, control review records `Design skeleton fidelity: yes` in Review Independence and includes meaningful `Design Skeleton Fidelity` findings;
- control review records `Context management / execution topology: yes` in Review Independence;
- control review includes meaningful `Context Management / Execution Topology` findings;
- when subagent-driven topology is selected, execution policy records `Subagent execution mode` and `Max concurrent subagents`;
- when a Superpowers delegation substrate is selected, execution policy uses a compatible mode: `$superpowers:subagent-driven-development` only for `serial-single-active`, and `$superpowers:dispatching-parallel-agents` only for `parallel-max-safe`;
- when subagent-driven topology is selected, control review records `Subagent concurrency fidelity: yes` in Review Independence and includes meaningful `Subagent Concurrency Fidelity` findings;
- goal includes a compact `Purpose Feedback Contract`;
- control review records `Purpose feedback adequacy: yes` in Review Independence;
- control review includes meaningful `Purpose Feedback Adequacy` findings;
- goal includes a compact `Realization Surface Contract`; simple direct tasks may record `RSC not applicable with justification`;
- execution policy includes `Realization Surface Closure Strategy`;
- control review records `Realization surface closure adequacy: yes` in Review Independence;
- control review includes meaningful `Realization Surface Closure Adequacy` findings;
- goal includes a compact `Target Achievement Contract`;
- goal `Target Achievement Contract` includes a target-producing spine reference;
- execution policy includes `Target-Producing Spine`;
- execution policy includes `Target-Producing Action Strategy`;
- execution policy `Candidate Plan Tasks` map work packages to `Spine node(s)`;
- control review records `Target achievement predicate fidelity: yes` in Review Independence;
- control review includes meaningful `Target Achievement Predicate Fidelity` findings;
- control review records `Target-producing spine fidelity: yes` in Review Independence;
- control review includes meaningful `Target-Producing Spine Fidelity` findings;
- goal includes a compact `Execution Horizon and Authority Contract`;
- execution policy includes `Horizon and Authority Coverage Matrix`;
- control review records `Execution horizon and authority fidelity: yes` in Review Independence;
- control review includes meaningful `Execution Horizon and Authority Fidelity` findings;
- control review includes `Final Observer Check`;
- final observer check allows approval;
- any substantive post-review change has final re-review recorded;
- any deterministic-only exception has guard evidence recorded;
- files reference the same feature and do not visibly conflict;
- runtime `/goal` will not need to write or approve a new plan.
- runtime `/goal` will not need to create or revise solution design.
- runtime `/goal` will not need to invent or replace the final output contract.
- runtime `/goal` will not need to invent or replace execution topology.

## Runtime Goal Contract

The contract artifact must be an index-style control contract, not a long copied prompt. It must include:

- approved control chain paths for requirements, design when present, goal, execution policy, and control review;
- a runtime execution rule that forbids reinterpreting the approved setpoint, answering method, task skeleton, target-achieved predicate, output contract, topology, sensors, or control strategy;
- a human-approved setpoint rule that treats primary object, requested transformation, non-goals, answering method, not-sufficient substitute, task skeleton family, execution horizon, runtime authority, forbidden actions, purpose feedback, realization surface closure, single target-achieved predicate, output contract, workflow fit, and known assumptions as source-owned by requirements;
- required sections to read, including `Human Setpoint Approval`, design `Task Skeleton Fidelity` when design exists, `Target Achievement Contract`, `Execution Horizon and Authority Contract`, `Purpose Feedback Contract`, `Realization Surface Contract`, `Horizon and Authority Coverage Matrix`, `Target-Producing Spine`, `Target-Producing Action Strategy`, `Candidate Plan Tasks`, `Context Management / Execution Topology`, substrate compatibility, subagent execution mode/concurrency sections, `Design Skeleton Fidelity`, `Execution Horizon and Authority Fidelity`, `Subagent Concurrency Fidelity`, `Target-Producing Spine Fidelity`, `Target Achievement Predicate Fidelity`, `Purpose Feedback Adequacy`, `Realization Surface Closure Adequacy`, and `Final Observer Check`;
- final report fields: `goal achieved: yes/no`, `single target-achieved predicate met: yes/no`, target-producing evidence, target-producing spine coverage and transition evidence, skeleton completion evidence when HSA/design define a task skeleton family, non-achieved reason when no, target-producing action attempted or proof of impossibility when no, smallest next target-producing attempt when no, approved execution horizon, horizon coverage, executed, prepared-only, forbidden-not-executed, explicitly out-of-scope by HSA, purpose feedback status and highest purpose-relevant evidence observed, and realization surfaces covered, actions completed or justified, residuals reconciled, and pending or unknown surfaces when RSC applies;
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
- Human Setpoint Approval: Approved
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
- [ ] Requirements analysis contains Human Setpoint Approval: Approved.
- [ ] Design Skeleton Fidelity is reviewed when HSA records an answering method or skeleton family.
- [ ] No control artifact was rewritten.
- [ ] Control review records `Context management / execution topology: yes` in Review Independence.
- [ ] Control review includes meaningful `Context Management / Execution Topology` findings.
- [ ] Subagent-driven topology records `Subagent execution mode` and `Max concurrent subagents`.
- [ ] Selected Superpowers substrate supports the approved subagent execution mode.
- [ ] Subagent-driven topology has `Subagent Concurrency Fidelity` review evidence.
- [ ] Final Observer Check is present and allows approval.
- [ ] Runtime goal contract references all approved files.
- [ ] Runtime goal contract indexes the goal's Final Output Contract when present or required.
- [ ] Runtime goal contract preserves the approved execution topology through the plan section index.
- [ ] Runtime goal contract preserves the human-approved setpoint through the requirements section index.
- [ ] Runtime goal contract indexes design `Task Skeleton Fidelity` and review `Design Skeleton Fidelity` when design exists.
- [ ] Runtime goal contract includes final report fields for EHA, PFB, RSC, and TAP claim calibration.
- [ ] Runtime goal contract indexes the approved Target-Producing Spine and review fidelity section.
- [ ] The user-entered `/goal` is pointer-only and length-bounded.
- [ ] The user-entered `/goal` does not inline HSA, PFB, RSC, TAP, topology, sensor-governance, review, or subagent protocol prose.
- [ ] The final `/goal` does not ask runtime Codex to write a new plan.
- [ ] The final `/goal` does not ask runtime Codex to create or revise solution design.
- [ ] Runtime goal contract includes executing, debugging, and completion-verification discipline.
- [ ] If guard or preconditions fail, the response includes a response-only next step and no final `/goal`.
- [ ] The skill did not execute target work.
