---
name: compiling-cybernetic-runtime-goals
description: 'Use only after requirements analysis, any required solution design, control contract, execution policy, and approved control review exist. Produces the final executable Codex /goal command that references the approved files. Does not analyze requirements, design solutions, write execution policies, review control artifacts, or execute target work.'
---

# Compiling Cybernetic Runtime Goals

## Overview

Produce the final executable `/goal` command from approved control artifacts.

Inputs:

- requirements analysis brief with status Complete
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
- use `$superpowers:systematic-debugging` for unclear or repeated failures;
- use `$superpowers:verification-before-completion` before claiming completion;
- if runtime cannot load these skills, follow the equivalent discipline already written in the approved plan and control review.

## Preconditions

Do not output `/goal` unless:

- requirements analysis status is Complete;
- goal contract exists;
- solution design exists when Design Gate was required or a design artifact exists;
- execution policy exists;
- control review status is Approved;
- control review includes `Final Observer Check`;
- final observer check allows approval;
- any substantive post-review change has final re-review recorded;
- any deterministic-only exception has guard evidence recorded;
- files reference the same feature and do not visibly conflict;
- runtime `/goal` will not need to write or approve a new plan.
- runtime `/goal` will not need to create or revise solution design.
- runtime `/goal` will not need to invent or replace the final output contract.

## Runtime Goal Contract

The final `/goal` must:

- reference the concrete requirements path;
- reference the concrete design path when Design Gate was required or a design exists;
- reference the concrete goal path;
- reference the concrete execution policy path;
- reference the concrete control review path;
- carry the final output contract from the goal when one is present or required;
- forbid reinterpreting requirements;
- forbid rewriting the control strategy;
- forbid rewriting the solution design;
- forbid replacing the final output audience, purpose, medium, structure, detail level, destination, or machine-readable shape;
- forbid replacing approved sensors without using approved sensor-governance rules;
- execute serially unless the approved review permits otherwise;
- use `$superpowers:executing-plans` discipline against the approved execution policy;
- use `$superpowers:systematic-debugging` for unclear or repeated failures;
- use `$superpowers:verification-before-completion` before claiming completion;
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

```markdown
Runtime /goal is ready:

```text
/goal Execute the approved execution policy in ...
```

Preflight:
- Requirements analysis: Complete
- Goal: present
- Solution design: present or not required
- Execution policy: present
- Control review: Approved
- Final output contract: present when required
```

Do not create or modify target-work artifacts.

## Validation Checklist

- [ ] Guard passed or equivalent checks passed.
- [ ] No control artifact was rewritten.
- [ ] Final Observer Check is present and allows approval.
- [ ] The final `/goal` references all approved files.
- [ ] The final `/goal` carries the goal's Final Output Contract when present or required.
- [ ] The final `/goal` does not ask runtime Codex to write a new plan.
- [ ] The final `/goal` does not ask runtime Codex to create or revise solution design.
- [ ] The final `/goal` includes executing, debugging, and completion-verification discipline.
- [ ] The skill did not execute target work.
