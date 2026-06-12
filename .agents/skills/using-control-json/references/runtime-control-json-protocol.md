# Runtime Control JSON Protocol

## Validate First

Before writing runtime files, load the approved control chain from JSON. Parse every required JSON file, check schema or registry validators when available, and confirm the artifacts identify the same run, required steps, work coverage, verifier, generation, and final report contract.

This protocol is not for Level 2 bounded runtime. Level 2 bounded goals use
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

`final-report.json` is the terminal report. Write it after progress evidence exists and after verifier evaluation. If the verifier does not permit completion, the final report must carry `goal_achieved: false` plus the unmet step, missing evidence, or blocker.

## Verifier Gate

Run the configured verifier before `goal_achieved: true`. The verifier command or module should come from `runtime.control.json`, the approved plan JSON, or a schema-backed run configuration. If no verifier is configured, stop.

Verifier permission means the verifier output explicitly allows or permits the completion claim for the current control chain and progress evidence. A successful command that checks only one component is supporting evidence, not completion permission.

In generation-aware mode, verifier permission is scoped to
`run.control.json.current_generation`. Progress from superseded generations does
not satisfy current generation steps unless the current runtime explicitly
imports that evidence and does not invalidate it. Unresolved amendment proposals
block `goal_achieved: true`. Discovery generations and synthetic required steps
also block `goal_achieved: true`; they are for finding or refining the strategy,
not for final completion.

When the verifier fails, append the verifier result to `progress.jsonl` through `.agents/skills/using-control-json/scripts/append_progress_event.py`, update `runtime-status.json`, and write a non-achieved final report only if the runtime contract calls for a terminal report.

## Short `/goal` Adapter

The `/goal` entry is a short pointer, not a control fact. It should name the runtime JSON location and this skill, for example:

```text
/goal Execute the runtime control JSON at docs/cybernetics/runs/<slug>/runtime.control.json using .agents/skills/using-control-json. Read it first; if required JSON is missing, invalid, or inconsistent, stop and report the smallest required human decision.
```

The adapter should not inline approved requirements, design, plan, review, evidence policy, work assignment, or final report prose. Those facts live in approved JSON and are interpreted through this protocol.
