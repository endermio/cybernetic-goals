# Orchestration Output And Final Checks

Use this reference after the orchestration state machine has reached
`RuntimeGoalReady` or `Blocked`. These output formats are response-only. Do not
write `/goal` prompts, `$skill ...` commands, or conversational next-step
prompts into orchestration status, progress, goal, design, plan, review, or
requirements artifacts.

## Approved Compilation

```markdown
Pre-goal compilation complete.

Artifacts:
- Requirements analysis: `...`
- Solution design: `...` or `not required`
- Goal contract: `...`
- Execution policy: `...`
- Control review: `...` (`Approved`)

Control summary:
- Setpoint: ...
- Solution model: ...
- Invariants: ...
- Execution policy: ...
- Sensors: ...
- Runtime boundary: ...

Runtime goal contract:

`docs/cybernetics/runtime-goals/YYYY-MM-DD-slug.goal.md`

User-entered short `/goal` pointer:

```text
/goal Execute the runtime goal contract at docs/cybernetics/runtime-goals/YYYY-MM-DD-slug.goal.md. Read it first and follow it exactly. If any referenced artifact is missing, not approved, or inconsistent, stop and report the smallest required human decision.
```

Do not start the goal until you are ready for runtime execution.
```

## Blocked Compilation

```markdown
Pre-goal compilation blocked.

Reason:
- ...

Artifacts created or updated:
- ...

Unresolved issue:
- ...

Smallest human decision needed:
- ...

Next allowed action:
- `RunDesign` / `RunGoalWriting` / `RunExecutionPolicy` / `RunReview` / `RunRuntimeCompile` / `Blocked`

Response-only next step:
- Follow the guard's `NEXT:` value when available.
- If requirements are incomplete: return to `$analyzing-cybernetic-requirements` with the smallest missing decision.
- If required design is missing: invoke or request `$designing-cybernetic-solutions`; if that skill is unavailable, stay `Blocked`.
- If goal, execution policy, or review is missing or stale: run the matching next allowed pre-goal stage.
- If review is not `Approved` or Final Observer blocks approval: rerun or obtain the required review before runtime compilation.
```

## Validation Checklist

Before responding, verify:

- [ ] This skill did not execute target work.
- [ ] This skill did not start `/goal`.
- [ ] Pre-goal review subagents were used only if explicitly authorized.
- [ ] Required Superpowers substrate status was checked.
- [ ] No required Superpowers substrate was silently emulated.
- [ ] No required solution design synthesis was emulated inside the orchestrator.
- [ ] Requirements analysis was complete before creating downstream artifacts.
- [ ] Required solution design was created by `$designing-cybernetic-solutions` or explicitly provided before goal writing, otherwise blocked.
- [ ] Existing design artifact paths were propagated to goal, execution policy, review, and runtime compilation.
- [ ] Output contract presence was propagated and validated; no output contract was synthesized by the orchestrator.
- [ ] Goal contract preserved confirmed human decisions.
- [ ] Goal and execution policy preserved required solution design.
- [ ] Execution policy preserved the goal contract.
- [ ] Execution policy uses `$superpowers:writing-plans` for non-trivial execution policies or blocks.
- [ ] Review checked the whole control structure, including design when required, not only the plan.
- [ ] Review does not mark self-review as `Approved`.
- [ ] Any substantive post-review artifact mutation had final independent re-review before approval.
- [ ] Lint PASS was not used as a substitute for semantic/control-policy re-review.
- [ ] Review status is `Approved` before final runtime `/goal` is emitted.
- [ ] If not approved, the response is blocked and asks for the smallest necessary decision.
- [ ] If blocked, the response includes `Next allowed action` and a response-only next step.
- [ ] Runtime goal contract references requirements analysis, required design, goal, plan, and review files.
- [ ] User-entered `/goal` is pointer-only and length-bounded.
- [ ] User-entered `/goal` does not inline HSA, PFB, RSC, TAP, EHA, topology, sensor governance, or review discipline prose.
- [ ] Runtime goal contract includes the missing/not-approved/inconsistent artifact precondition.
- [ ] Runtime goal contract includes executing, debugging, and completion-verification discipline.
- [ ] User-entered `/goal` does not tell Codex to write or approve a new plan.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating this as an execution skill | Stop; this skill only compiles control artifacts |
| Spawning subagents without user authorization | Ask for authorization or run candidate-only mode |
| Creating a final `/goal` from an incomplete requirements analysis | Stop and return to requirements analysis |
| Skipping design when Design Gate is required | Run `$designing-cybernetic-solutions` before goal writing |
| Synthesizing solution design inside the orchestrator | Stop; invoke/request `$designing-cybernetic-solutions` or block |
| Dropping an existing design artifact because Design Gate is satisfied | Propagate the design path downstream |
| Reviewing only the plan | Review requirements analysis, design when required, goal, and runtime boundary |
| Replacing missing `$superpowers:writing-plans` with an ad hoc approved plan | Stop and report missing planning infrastructure |
| Marking Approved after fixing reviewer blockers without final re-review | Mark artifacts Dirty / Needs Re-review and run final independent re-review |
| Treating lint PASS as proof that semantic reviewer blockers are resolved | Use lint only as a structural sensor; require final observer pass for substantive changes |
| Choosing a new slug for downstream artifacts | Use the requirements analysis brief's date/slug unless the user explicitly specified other paths |
| Letting review revisions change confirmed semantics | Stop and ask the human |
| Infinite review-revision loops | Stop after two cycles |
| Marking self-review as Approved | Require subagent, external reviewer, or explicit human approval |
| Starting `/goal` after compiling it | Output the command only |
