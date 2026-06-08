---
name: compiling-cybernetic-runtime-goals
description: 'Use when requirements, any required design, goal contract, execution policy, and approved control review exist, and the final runtime /goal command must be checked or emitted before execution.'
---

# Compiling Cybernetic Runtime Goals

## Overview

Produce the final executable `/goal` command from approved control artifacts.

Inputs:

- requirements analysis brief with status Complete
- Human Setpoint Approval: Approved in the requirements analysis
- solution design, when Design Gate was required or a design exists
- goal contract
- execution policy / plan
- control review with status Approved

This skill is a thin compiler. It must not rewrite the control structure.

Use `scripts/control_chain_guard.py` and `scripts/compile_runtime_goal.py` when available.

## Required Infrastructure

Follow `$cybernetic-superpowers-infrastructure`.

This skill does not invoke runtime execution. It compiles runtime discipline into the final `/goal` command.

The final command must instruct runtime Codex to:

- use `$superpowers:executing-plans` discipline against the approved plan;
- use the approved execution topology defined in the execution policy;
- use the approved bounded subagent delegation protocol when the approved topology selects serial or parallel subagent-driven execution;
- use `$superpowers:subagent-driven-development` only when the approved plan records `Selected delegation substrate: superpowers-subagent-driven-development` for work packages that fit that implementation-plan, current-session workflow;
- treat subagent outputs as candidate results until main-agent integration against approved artifacts, progress log, evidence requirements, and stop conditions;
- execute only against the human-approved setpoint in the requirements analysis; do not reinterpret the human purpose, primary object, requested transformation, non-goals, Purpose Feedback Boundary, Realization Surface Closure, Completion Predicate, output contract, or workflow fit;
- use `$superpowers:systematic-debugging` for unclear or repeated failures;
- use `$superpowers:verification-before-completion` before claiming completion;
- Report completion status according to the highest purpose-relevant evidence actually observed.
- Do not claim the human purpose is achieved from internal sensors alone unless the approved goal says internal evidence is sufficient.
- If purpose feedback is missing, report what is verified, what is not yet observed, and the smallest next observation needed.
- Do not claim target-state realization from local action alone when Realization Surface Closure is required.
- Strongest positive target-realization claims require RSC adequate.
- Report surfaces covered, required surface actions completed or justified, residuals reconciled, pending or unknown surfaces, and smallest next reconciliation when RSC is partial, missing, unavailable, or not applicable with justification.
- Do not treat fallback, partial, diagnostic, unavailable, invalid, or blocked report statuses as goal achieved unless the approved Human Setpoint Approval explicitly defines the task as classification/reporting rather than target realization or measurement.
- Final reports must include goal achieved: yes/no, target-achieved status, report status, target-producing evidence, fallback reason, and smallest next target-producing attempt.
- if runtime cannot load these skills, follow the equivalent discipline already written in the approved plan and control review.

## Preconditions

Do not output `/goal` unless:

- requirements analysis status is Complete;
- requirements analysis includes `Human Setpoint Approval: Approved`;
- goal contract exists;
- solution design exists when Design Gate was required or a design artifact exists;
- execution policy exists;
- control review status is Approved;
- control review records `Context management / execution topology: yes` in Review Independence;
- control review includes meaningful `Context Management / Execution Topology` findings;
- goal includes a compact `Purpose Feedback Contract`;
- control review records `Purpose feedback adequacy: yes` in Review Independence;
- control review includes meaningful `Purpose Feedback Adequacy` findings;
- goal includes a compact `Realization Surface Contract`; simple direct tasks may record `RSC not applicable with justification`;
- execution policy includes `Realization Surface Closure Strategy`;
- control review records `Realization surface closure adequacy: yes` in Review Independence;
- control review includes meaningful `Realization Surface Closure Adequacy` findings;
- goal includes a compact `Completion Predicate Contract`;
- control review records `Completion predicate fidelity: yes` in Review Independence;
- control review includes meaningful `Completion Predicate Fidelity` findings;
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

The final `/goal` must:

- reference the concrete requirements path;
- reference the concrete design path when Design Gate was required or a design exists;
- reference the concrete goal path;
- reference the concrete execution policy path;
- reference the concrete control review path;
- carry the final output contract from the goal when one is present or required;
- execute only against the human-approved setpoint in the requirements analysis;
- forbid reinterpreting the human purpose, primary object, requested transformation, non-goals, Purpose Feedback Boundary, Realization Surface Closure, Completion Predicate, output contract, or workflow fit;
- forbid reinterpreting requirements;
- forbid rewriting the control strategy;
- forbid rewriting the solution design;
- forbid replacing the final output audience, purpose, medium, structure, detail level, destination, or machine-readable shape;
- forbid replacing approved sensors without using approved sensor-governance rules;
- use the approved execution topology defined in the execution policy;
- use `$superpowers:executing-plans` discipline against the approved execution policy;
- use the approved bounded subagent delegation protocol when the approved execution topology selects serial or parallel subagent-driven execution;
- use `$superpowers:subagent-driven-development` only when the approved execution policy records `Selected delegation substrate: superpowers-subagent-driven-development` for work packages that fit that implementation-plan, current-session workflow;
- state that subagent outputs remain candidate results until main-agent integration;
- use `$superpowers:systematic-debugging` for unclear or repeated failures;
- use `$superpowers:verification-before-completion` before claiming completion;
- Report completion status according to the highest purpose-relevant evidence actually observed.
- Do not claim the human purpose is achieved from internal sensors alone unless the approved goal says internal evidence is sufficient.
- If purpose feedback is missing, report what is verified, what is not yet observed, and the smallest next observation needed.
- Do not claim target-state realization from local action alone when Realization Surface Closure is required.
- Strongest positive target-realization claims require RSC adequate.
- Report surfaces covered, required surface actions completed or justified, residuals reconciled, pending or unknown surfaces, and smallest next reconciliation when RSC is partial, missing, unavailable, or not applicable with justification.
- Do not treat fallback, partial, diagnostic, unavailable, invalid, or blocked report statuses as goal achieved unless the approved Human Setpoint Approval explicitly defines the task as classification/reporting rather than target realization or measurement.
- Final reports must include goal achieved: yes/no, target-achieved status, report status, target-producing evidence, fallback reason, and smallest next target-producing attempt.
- follow equivalent discipline already written in the approved plan and control review if runtime cannot load those skills;
- stop if any referenced artifact is missing, not approved, or internally inconsistent;
- stop if artifacts conflict or become insufficient.

## Scripted Compilation

Preferred:

```bash
python3 .agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py \
  --requirements docs/cybernetics/requirements/YYYY-MM-DD-feature.md \
  --design docs/cybernetics/designs/YYYY-MM-DD-feature.md \
  --goal docs/cybernetics/goals/YYYY-MM-DD-feature.md \
  --plan docs/cybernetics/plans/YYYY-MM-DD-feature.md \
  --review docs/cybernetics/control-reviews/YYYY-MM-DD-feature.md
```

Do not use `--skip-guard` for official runtime `/goal` compilation. It is only for internal validation and requires the explicit `--i-understand-this-bypasses-phase-gates` acknowledgement.

## Output Format

These output formats are response-only. Do not write `$skill ...` commands, runtime `/goal` prompts, or conversational next-step prompts into requirements, design, goal, plan, or review artifacts.

### Approved runtime command

```markdown
Runtime /goal is ready:

```text
/goal Execute the approved execution policy in ...
```

Preflight:
- Requirements analysis: Complete
- Human Setpoint Approval: Approved
- Goal: present
- Solution design: present or not required
- Execution policy: present
- Control review: Approved
- Final output contract: present when required
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
- [ ] No control artifact was rewritten.
- [ ] Control review records `Context management / execution topology: yes` in Review Independence.
- [ ] Control review includes meaningful `Context Management / Execution Topology` findings.
- [ ] Final Observer Check is present and allows approval.
- [ ] The final `/goal` references all approved files.
- [ ] The final `/goal` carries the goal's Final Output Contract when present or required.
- [ ] The final `/goal` preserves the approved execution topology.
- [ ] The final `/goal` preserves the human-approved setpoint, including primary object, requested transformation, non-goals, Purpose Feedback Boundary, Realization Surface Closure, Completion Predicate, output contract, and workflow fit.
- [ ] The final `/goal` treats subagent outputs as candidate results until main-agent integration.
- [ ] The final `/goal` does not ask runtime Codex to write a new plan.
- [ ] The final `/goal` does not ask runtime Codex to create or revise solution design.
- [ ] The final `/goal` includes executing, debugging, and completion-verification discipline.
- [ ] The final `/goal` calibrates completion claims to the highest purpose-relevant evidence actually observed.
- [ ] The final `/goal` calibrates target-realization claims to Realization Surface Closure status.
- [ ] The final `/goal` calibrates goal-achieved claims to Completion Predicate Fidelity.
- [ ] If guard or preconditions fail, the response includes a response-only next step and no final `/goal`.
- [ ] The skill did not execute target work.
