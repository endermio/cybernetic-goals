# Pre-goal Orchestration Status: [Name]

## Current State

State: `RequirementsMissing` / `RequirementsComplete` / `DesignReady` / `GoalReady` / `PolicyReady` / `ReviewApproved` / `RuntimeGoalReady` / `Blocked`

## Artifact Chain

| Stage | Required | Path | Status | Check |
|---|---:|---|---|---|
| Requirements | yes | `[path]` | `Complete / Incomplete / missing` | `passed / blocked` |
| Design | `yes/no` | `[path or none]` | `Candidate / Reviewed / Approved / missing / not required` | `passed / blocked` |
| Final Answer Format | `yes/no` | `[requirements/design/goal section or none]` | `present / missing / not required` | `passed / blocked` |
| Goal | yes | `[path or none]` | `present / missing` | `passed / blocked` |
| Execution Policy | yes | `[path or none]` | `Candidate / Approved / missing` | `passed / blocked` |
| Control Review | yes | `[path or none]` | `Approved / Needs Revision / Needs Independent Review / Dirty / Needs Re-review / missing` | `passed / blocked` |
| Runtime Goal | yes | `[path or inline command / none]` | `compiled / not compiled` | `passed / blocked` |

## Next Allowed Action

`RunDesign` / `RunGoalWriting` / `RunExecutionPolicy` / `RunReview` / `RunRuntimeCompile` / `OutputRuntimeGoal` / `Blocked`

## Execution Work Assignment

- Who does the work: `Main-only / Serial subagent-driven / Parallel subagent-driven / not selected`
- Work Assignment source: `[execution policy path]`
- Orchestrator decision made: `no`

## Blocked Reason

- `[reason or "None"]`

## Subagent Authorization

Pre-goal review subagents authorized: `yes` / `no`

Runtime target-work subagents authorized by final `/goal` launch: `not compiled / compiled but not launched / launched`

Parallel runtime subagents approved in execution policy and review: `yes / no / not applicable`

Evidence:

- `[quote or instruction]`

## Guard Evidence

| Checkpoint | Command | Result |
|---|---|---|
| before-design | `python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py --state before-design ...` | `pass/fail/not run` |
| before-goal | `python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py --state before-goal ...` | `pass/fail/not run` |
| before-policy | `python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py --state before-policy ...` | `pass/fail/not run` |
| before-review | `python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py --state before-review ...` | `pass/fail/not run` |
| before-runtime-compile | `python3 .agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py --state before-runtime-compile ...` | `pass/fail/not run` |

## Notes

- `[note]`
