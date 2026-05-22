---
name: compiling-cybernetic-runtime-goals
description: 'Use only after clarification, goal contract, execution policy, and approved control review exist. Produces the final executable Codex /goal command that references the approved files. Does not clarify requirements, write plans, review plans, or implement code.'
---

# Compiling Cybernetic Runtime Goals

## Overview

Produce the final executable `/goal` command from approved control artifacts.

Inputs:

- clarification brief with status Complete
- goal contract
- execution policy / plan
- control review with status Approved

This skill is a thin compiler. It must not rewrite the control structure.

Use `scripts/control_chain_guard.py` and `scripts/compile_runtime_goal.py` when available.

## Preconditions

Do not output `/goal` unless:

- clarification status is Complete;
- goal contract exists;
- execution policy exists;
- control review status is Approved;
- files reference the same feature and do not visibly conflict;
- runtime `/goal` will not need to write or approve a new plan.

## Runtime Goal Contract

The final `/goal` must:

- reference the concrete clarification path;
- reference the concrete goal path;
- reference the concrete execution policy path;
- reference the concrete control review path;
- forbid reinterpreting requirements;
- forbid rewriting the control strategy;
- forbid replacing approved sensors without using approved sensor-governance rules;
- execute serially unless the approved review permits otherwise;
- stop if any referenced artifact is missing, not approved, or internally inconsistent;
- stop if artifacts conflict or become insufficient.

## Scripted Compilation

Preferred:

```bash
python3 .agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py \
  --clarification docs/superpowers/clarifications/YYYY-MM-DD-feature.md \
  --goal docs/superpowers/goals/YYYY-MM-DD-feature.md \
  --plan docs/superpowers/plans/YYYY-MM-DD-feature.md \
  --review docs/superpowers/control-reviews/YYYY-MM-DD-feature.md
```

## Output Format

```markdown
Runtime /goal is ready:

```text
/goal Execute the approved execution policy in ...
```

Preflight:
- Clarification: Complete
- Goal: present
- Execution policy: present
- Control review: Approved
```

Do not create or modify implementation files.

## Validation Checklist

- [ ] Guard passed or equivalent checks passed.
- [ ] No control artifact was rewritten.
- [ ] The final `/goal` references all approved files.
- [ ] The final `/goal` does not ask runtime Codex to write a new plan.
- [ ] The skill did not implement code.
