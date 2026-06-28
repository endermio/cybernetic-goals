# Runtime Control JSON Protocol

## Validate First

Before writing runtime files, load the approved control chain from JSON. Parse every required JSON file, check schema or registry validators when available, and confirm the artifacts identify the same run, required steps, work coverage, verifier, generation, and final report contract.

This protocol is not for `bounded_runtime`. Bounded runtime goals use
`using-bounded-control-json`; a directory with only `goal.control.json` and
`runtime.control.json` is valid for bounded runtime but invalid for this
control-chain protocol.

Stop on missing, invalid, or inconsistent JSON before writing progress or status. Report the exact file or relationship that failed and the smallest human decision needed to continue.

Historical Markdown can remain as background only. A runtime JSON chain that needs Markdown as an official guard, compiler, or runtime control input is inconsistent JSON for this protocol.

## Read-Only Approved JSON

approved control JSON is read-only during runtime.

Full-chain mode:

- `requirements.control.json`
- `design.control.json`
- `goal.control.json`
- `plan.control.json`
- `review.control.json`
- `runtime.control.json`

Generation-aware mode:

- `requirements.control.json`
- `run.control.json`
- the current `gen-N/runtime.control.json`
- the current generation review file when `run.control.json` names one

Use approved JSON to decide what work is authorized, what counts as done, where results must appear, what evidence is required, and what the final report shape must contain. A runtime executor records facts about execution; it does not edit approved JSON after execution starts.

If the approved target, plan, review, or runtime contract appears wrong, stale, or insufficient, append an observation through `.agents/skills/using-control-json/scripts/append_progress_event.py` when `progress.jsonl` is available and valid. If the current strategy cannot produce a blocking required outcome but the approved anchors can remain unchanged, append a `control.amendment.proposed` event instead of hard-completing with substitute evidence. If the needed change would alter approved anchors or authority, stop and report the smallest required human decision.

If execution discovers a fact that should have been known before design or
planning, treat it as an `information_sufficiency_check` issue. Runtime must
not invent a new sufficiency standard, silently continue from assumptions, or
convert the missing fact into a design detail. Record the observation, and when
the current strategy can be repaired without changing approved anchors, append
a reviewed amendment proposal with affected source requirements and a patch.
If the missing fact changes source requirements, required outcomes, authority,
or what counts as done, stop for human reapproval.

Generation-aware runs declare a generation `strategy_kind`:

- `discovery`: may start from a narrow observation horizon and may use synthetic steps from requirements, but cannot permit `goal_achieved: true`.
- `execution`: may permit final completion only when the generation has an approved review and non-synthetic executable steps.
- `amendment`: must have a parent, amendment source, approved review, and non-synthetic executable steps.

`max_auto_amendment_rounds` in `run.control.json` limits automatic reviewed replanning. When the generation history exceeds that limit, stop instead of continuing another automatic amendment.

## Approved Hashes

`review.control.json` binds the approved pre-runtime inputs by hash.
`runtime.control.json` binds all read-only control JSON, including itself.

When calculating the hash for `runtime.control.json`, exclude the top-level `approved_control_hashes` field. This avoids an impossible self-reference loop.
All other read-only control JSON hashes include the full JSON object.

If any approved hash does not match the current file content, stop before
writing progress. Runtime execution must not repair approved JSON hashes.

## Writable Runtime Files

runtime writes only these control-output files:

- `progress.jsonl`
- `runtime-status.json`
- `final-report.json`

Non-control evidence artifacts are separate. Runtime may write evidence files
only under `runtime.control.json.runtime.writable_evidence_paths`, such as
`evidence/`, when the approved requirements, plan, or verifier require those
evidence artifacts. Do not add evidence artifact paths to `writable_files`;
`writable_files` is reserved for the three control-output files above.

`progress.jsonl` is the append-only event log. Runtime must append to `progress.jsonl` only through `.agents/skills/using-control-json/scripts/append_progress_event.py`; direct writes to `progress.jsonl` are invalid runtime behavior. Each event should be a small observation about a command, evidence item, required-step state, blocker, deviation, amendment proposal, generation switch, or verifier result. Progress observations are additive; do not mutate approved JSON to make the contract match the run.

Corrections to earlier observations use `observation.recorded` with correction
metadata such as `corrects_event_ref`, `classification`, `summary`,
`evidence_id`, or `evidence_path`. Do not invent new event types such as
`observation.corrected`; unsupported event types must be rejected at append
time.

Every progress event includes `runtime_generation`. Event families are validated
separately:

- step events require `work_package_id`, `required_step`, `status`, and
  `evidence`;
- amendment events require `amendment_id` and amendment-specific fields;
- generation events require generation-specific fields such as `reason` when a
  generation is superseded.
- runtime counterexample review events use `counterexample.review.completed`
  and require `status`, `verdict`, `reviewer`, `reviewed_steps`,
  `reviewed_outcomes`, `checked_transformations`, and `evidence`.

Do not add fake `work_package_id`, `required_step`, `status`, or `evidence`
fields just to make amendment or generation events look like step events.

Amendment events use `control.amendment.proposed`,
`control.amendment.approved`, `control.amendment.rejected`, or
`control.amendment.blocked`.

`control.amendment.proposed` must also include:

- `reason`
- `triggering_observation`
- `affected_stages`
- `affected_source_requirements`
- `semantic_base_change`
- `required_outcomes_changed`
- `authority_expanded`
- `proposed_changes`
- `review_required`
- `patch_ref`

The schemas preserve v1.0 parse compatibility for historical amendment events.
Current runtime execution policy requires `affected_source_requirements` on
every `control.amendment.proposed` event so affected source requirements can be
reviewed before a new generation is approved.

`patch_ref` names a JSON patch artifact inside the same run directory. The patch
describes the next strategy candidate, including refined required steps and any
derived runtime updates such as verifier config, evidence import, or evidence
invalidation. The patch must not contain target-anchor changes. A proposal
without a patch is incomplete, and a patch without an approved amendment review
cannot switch `run.control.json.current_generation`.

When runtime observes that current strategy can only produce weaker evidence
for a blocking source requirement, append `control.amendment.proposed` with
`affected_source_requirements`. Do not claim completion from substitute
evidence. Amendment may change derived strategy only; it may not weaken source
requirements, required outcomes, approved authority, or semantic base.

If any of `semantic_base_change`, `required_outcomes_changed`, or
`authority_expanded` is true, that amendment is a request for human decision,
not an automatically reviewable strategy change.

`runtime-status.json` is the current bounded status snapshot. It can summarize active step state, blockers, next action, and last evidence pointer.

`final-report.json` is the terminal runtime report. It records the runtime's
completion or non-completion claim, evidence, work coverage, and remaining gaps.
It does not grant verifier permission to itself. A legacy `verification` object
may be present for compatibility, but the configured verifier is a structural
final-claim gate for whether the current JSON/progress evidence permits
`goal_achieved: true`. Verifier success is not a semantic quality gate; the
requirements-approved Counterexample Gate is the adversarial quality gate.

Write `final-report.json` after progress evidence exists. Then run the verifier.
If the verifier does not permit completion, rewrite or replace the terminal
report with `goal_achieved: false` plus the unmet step, missing evidence, or
blocker before reporting the run as terminal.

## Verifier Gate

Gate routing semantics follow
`.agents/skills/references/transition-gate-protocol.md`. A structural or
quality gate result with `terminal: false` means the runtime agent must execute
the returned `next_action`, record the required evidence or status, and rerun
the same gate. It must not report the gate result itself as completion or as a
human approval request unless `may_ask_user` is true.

### Structural Gates And Quality Gate

Structural gates are schema validation, `control_chain_guard`,
`validate_control_chain`, and `verify_runtime_progress`. They check file shape,
hashes, declared coverage, generation consistency, progress format, and final
report consistency. A structural pass is not quality approval.

Quality gate means `counterexample-gate`: an independent reviewer attempts to
disprove the target decomposition, runtime strategy, blocked claim, or
completion claim. `counterexample-gate` is the final quality gate for
`goal_achieved: true` and terminal blocked claims.

The quality gate scope comes from the requirements-approved
`counterexample_gate_contract`. Runtime, design, orchestration, and review must
not invent, weaken, or replace that contract. Missing or inconsistent
requirements-approved gate contract means the run is not executable until
requirements are fixed.
Requirements define `information_sufficiency_check`, and runtime treats that
check as approved control. Blocking facts must have been derived from source
requirements/outcomes and independently challenged before design or planning. A
runtime completion or blocked claim cannot rely on facts invented afterward
unless a reviewed amendment or human reapproval updates the control structure.
Each blocking required outcome also has a per-outcome `counterexample_gate`;
its checked transformations must be covered before the outcome can support
`goal_achieved: true` or a terminal blocked claim.

Run the configured verifier before accepting, reporting, or acting on
`goal_achieved: true`. The verifier command or module should come from
`runtime.control.json`, the approved plan JSON, or a schema-backed run
configuration. If no verifier is configured, stop.

Verifier permission means the verifier output explicitly allows or permits the completion claim for the current control chain and progress evidence. A successful command that checks only one component is supporting evidence, not completion permission.

In generation-aware mode, verifier permission is scoped to
`run.control.json.current_generation`. Progress from superseded generations does
not satisfy current generation steps unless the current runtime explicitly
imports that evidence and does not invalidate it. Unresolved amendment proposals
block `goal_achieved: true`. Discovery generations and synthetic required steps
also block `goal_achieved: true`; they are for finding or refining the strategy,
not for final completion.

The approved generation review must include a `counterexample-gate` check before
runtime relies on the generation for completion or blocked claims. Counterexample
Gate means an independent reviewer attempts to disprove the candidate control
claim. It must cover the requirements-approved target decomposition and runtime
claim points plus per-outcome gate points, including at least:

```text
source_requirements->required_outcomes
required_outcomes->required_steps
required_steps->work_packages
required_steps->runtime_steps
pre_runtime_compile
blocked_or_goal_achieved
```

An approved `counterexample-gate` must record independent reviewer provenance
with `reviewer.kind`, `reviewer.id`, and `reviewer.evidence_ref`. Accepted
reviewer kinds are `subagent`, `human`, and `external`. The execution agent's own
summary is not enough.

Before `goal_achieved: true`, runtime must also append a current-generation
`counterexample.review.completed` event. This event is the hard runtime
Counterexample Gate for the final completion claim. It must be `status: pass`
and `verdict: approved`, must include independent reviewer provenance, and must
cover every current runtime `required_step` plus every blocking required outcome.
It must also cover the requirements-approved counterexample contract points and
the per-outcome counterexample gate points. If any decomposed step or blocking
outcome is missing from this review, the verifier must reject `goal_achieved:
true` even when all step events and final-report fields are otherwise present.

If runtime discovers a counterexample that was missed by review, record it as an
observation or amendment proposal. Do not claim `goal_achieved: true`, and do
not turn the missed work into `blocked` unless the blocked claim itself is
reviewed under the Counterexample Gate.

When the verifier fails, append the verifier result to `progress.jsonl` through `.agents/skills/using-control-json/scripts/append_progress_event.py`, update `runtime-status.json`, and write a non-achieved final report only if the runtime contract calls for a terminal report.

## Short `/goal` Adapter

The `/goal` entry is a short pointer, not a control fact. It should name the runtime JSON location and this skill, for example:

```text
/goal Execute the runtime control JSON at docs/cybernetics/runs/<slug>/runtime.control.json using .agents/skills/using-control-json. Read it first; if required JSON is missing, invalid, or inconsistent, stop and report the smallest required human decision.
```

The adapter should not inline approved requirements, design, plan, review, evidence policy, work assignment, or final report prose. Those facts live in approved JSON and are interpreted through this protocol.
