# Cybernetic Skills Pack

This package contains a pre-goal control pipeline for Codex-style agent work.

The core idea is:

```text
skills = compile-time control tools
/goal = runtime executor
Superpowers = planning/review/execution substrate
```

For complex work, do not let `/goal` analyze requirements, invent the solution design, write its own plan, review its own plan, or invent a new control strategy during execution. Instead, prepare and approve control artifacts first, then compile the final runtime `/goal` command.

Superpowers dependencies are stage-specific infrastructure, not optional style suggestions. See `docs/cybernetic-framework/superpowers-infrastructure-policy.md`.

## Install

From this package root, copy the skill directories into either your user-level skill directory:

```bash
mkdir -p ~/.agents/skills
cp -R .agents/skills/* ~/.agents/skills/
```

or into a repository-local skill directory:

```bash
mkdir -p .agents/skills
cp -R cybernetic-skills-pack/.agents/skills/* .agents/skills/
```

## Recommended workflow

For complex work:

```text
$routing-cybernetic-workflows
  -> decide whether full pipeline is appropriate

$analyzing-cybernetic-requirements
  -> docs/cybernetics/requirements/YYYY-MM-DD-feature.md

$designing-cybernetic-solutions
  -> docs/cybernetics/designs/YYYY-MM-DD-feature.md when Design Gate is required

$orchestrating-cybernetic-pregoal
  -> run the remaining pre-goal compilation chain after requirements analysis/design are complete
```

The orchestrator drives the following skills and stops if the review cannot converge:

```text
$designing-cybernetic-solutions
  -> docs/cybernetics/designs/YYYY-MM-DD-feature.md when Design Gate is required

$writing-cybernetic-goals
  -> docs/cybernetics/goals/YYYY-MM-DD-feature.md

$writing-cybernetic-execution-policies
  -> docs/cybernetics/plans/YYYY-MM-DD-feature.md

$reviewing-cybernetic-control-structures
  -> docs/cybernetics/control-reviews/YYYY-MM-DD-feature.md

$compiling-cybernetic-runtime-goals
  -> final executable /goal command
```

For simple work, the router should reject the full pipeline and recommend an inline prompt or inline `/goal`.

## Included skills

- `routing-cybernetic-workflows`: classify complexity and route to the right workflow.
- `analyzing-cybernetic-requirements`: analyze human intent and create a requirements analysis brief.
- `clarifying-cybernetic-tasks`: deprecated compatibility alias for `analyzing-cybernetic-requirements`.
- `designing-cybernetic-solutions`: create a general solution/system model when Design Gate is required.
- `orchestrating-cybernetic-pregoal`: orchestrate the pre-goal compilation chain after requirements analysis/design.
- `cybernetic-superpowers-infrastructure`: define stage-specific Superpowers substrate dependencies and non-substitution rules.
- `writing-cybernetic-goals`: create a control contract, not a runtime `/goal`, for complex work.
- `writing-cybernetic-execution-policies`: create an execution policy / plan as a control law.
- `reviewing-cybernetic-control-structures`: review requirements analysis, design when required, goal, and plan as a coherent control system.
- `compiling-cybernetic-runtime-goals`: compile the final runtime `/goal` command only after approval gates pass.

## Scripts

The scripts are intentionally small and deterministic. They check structure and phase gates; they do not decide product semantics.

- `control_artifact_lint.py`: lint requirements analysis/design/goal/plan/review artifacts.
- `check_pregoal_inputs.py`: check that orchestration starts from the expected requirements analysis input.
- `control_chain_guard.py`: block premature runtime goal compilation.
- `compile_runtime_goal.py`: compile the final executable `/goal` command from approved artifacts.

## Why this structure exists

Pre-goal skills synthesize and review the solution model and control structure. `/goal` runs the approved control structure. This separates controller synthesis from controller execution and prevents an execution agent from designing, approving, and running its own control law.
