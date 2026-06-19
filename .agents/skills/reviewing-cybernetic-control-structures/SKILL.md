---
name: reviewing-cybernetic-control-structures
description: 'Use when requirements analysis, any required design, goal.control.json, and execution policy exist before runtime /goal, and the cybernetic approved work chain needs independent approval, blocker review, or risk review.'
---

# Reviewing Cybernetic Control Structures

## Overview

Review whether the approved work chain is coherent enough to execute.

Input: requirements JSON, optional design, goal JSON, execution policy or
current generation strategy. Output: `review.control.json`.

This skill does not execute target work and does not start `/goal`.
Detailed review dimensions live in `references/control-review-detailed-rules.md`
and `references/review-rubric.md`.

## Independent Review Rule

Do not self-review and mark `Approved`.

Use authorized subagents, explicit human approval, or another independent
reviewer. Otherwise mark `Needs Independent Review`.

No `Approved` state is allowed after an unreviewed substantive artifact
mutation. If approved files change after review, mark `Dirty` or `Needs
Re-review` until final independent re-review passes.

## Semantic Review Verdicts

Subagent semantic review verdicts must be one of:

```text
`Approved` / `NeedsRevision` / `Blocked`
```

`NeedsRevision` is not a simple fail. It means the chain contains repairable
intent drift, obligation downgrade, or artifact misrouting.
runtime compilation is forbidden until the verdict is `Approved`.

## Required Checks

Always check:

- requirement traceability;
- Intent Preservation / Obligation Preservation Review;
- source-requirement-preservation when `source_requirements` exist;
- required outcome coverage;
- Counterexample Gate;
- design match when design exists;
- goal correctness;
- plan controllability;
- evidence governance;
- runtime suitability;
- review independence;
- final observer.

Use the detailed reference for the full rubric.

## Intent Preservation / Obligation Preservation Review

Reject or return to revision when implementation, measurement, repair,
diagnosis, or decision work is weakened into readiness, future work, allowed
action, compatibility-only behavior, a framework, or a plan.

Regression examples that must be `NeedsRevision`:

- required `/api/v2` implementation must not be accepted as legacy Drogon compatibility readiness;
- source request to measure E, S, A, M, Q, K, Se, Nout, Cckpt growth curves must
  not become define scan framework and dominance rules;
- implement /api/v2 download/extract/preview API family must not become
  compatible with future v2 exposure.

Route these to `ReturnToRequirementsAnalysis` if the source requirement itself
was weakened.

## Counterexample Gate

Every approved review must include `counterexample-gate`. It attempts to
disprove the target decomposition and runtime claim.

It must include reviewer provenance: `reviewer.kind`, `reviewer.id`, and
`reviewer.evidence_ref`. Self-written evidence is not enough.

Required `checked_transformations`:

```text
source_requirements->required_outcomes
required_outcomes->required_steps
required_steps->work_packages
required_steps->runtime_steps
pre_runtime_compile
blocked_or_goal_achieved
```

## Plan And Runtime Review

Each blocking required step needs a credible chain:

```text
required step -> what would make it true -> producing action -> mainline work package -> evidence after action
```

Flag plans that inspect old artifacts or compare current results while required
implementation, experiment, repair, or measurement is still needed.

Runtime completion claims must match the strongest evidence actually observed.
Missing purpose evidence supports not-done, not `goal_achieved: true`.

## Deterministic Lint

If scripts are available, run:

```bash
python3 .agents/skills/reviewing-cybernetic-control-structures/scripts/control_artifact_lint.py \
  --requirements [REQUIREMENTS] \
  --design [DESIGN] \
  --goal [GOAL] \
  --plan [PLAN]
```

Lint is structural evidence, not meaning approval.

## Output Format

This output format is response-only. Do not write `$skill ...` commands,
runtime `/goal` prompts, or conversational next-step prompts into the review
artifact.

```markdown
Created or updated review:
`docs/cybernetics/runs/YYYY-MM-DD-slug/review.control.json`

Review status:
- `Approved` / `Needs Revision` / `Needs Independent Review` / `Dirty` / `Needs Re-review` / `Blocked`

Review verdict:
- `Approved` / `NeedsRevision` / `Blocked`

Key findings:
- ...

Response-only next step:
- return to `$orchestrating-cybernetic-pregoal`, or
- revise the named artifact and rerun review, or
- report the smallest unresolved decision, dependency, or unavailable fact.
```

## Validation Checklist

- [ ] Review file was created or updated.
- [ ] Review status and verdict are explicit.
- [ ] Independent review basis is recorded.
- [ ] Counterexample Gate is present.
- [ ] Source requirements were compared to approved user request text.
- [ ] Final observer check is recorded.
- [ ] Lint PASS is not treated as semantic approval.
- [ ] Review does not execute target work or start `/goal`.
