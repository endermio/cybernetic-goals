# Runtime Control JSON Protocol

## Validate First

Before writing runtime files, load the approved control chain from JSON. Parse every required JSON file, check schema or registry validators when available, and confirm the artifacts identify the same run, required steps, work coverage, verifier, and final report contract.

Stop on missing, invalid, or inconsistent JSON before writing progress or status. Report the exact file or relationship that failed and the smallest human decision needed to continue.

Historical Markdown can remain as background only. A runtime JSON chain that needs Markdown as an official guard, compiler, or runtime control input is inconsistent JSON for this protocol.

## Read-Only Approved JSON

approved control JSON is read-only during runtime:

- `requirements.control.json`
- `design.control.json`
- `goal.control.json`
- `plan.control.json`
- `review.control.json`
- `runtime.control.json`

Use approved JSON to decide what work is authorized, what counts as done, where results must appear, what evidence is required, and what the final report shape must contain. A runtime executor records facts about execution; it does not edit approved JSON after execution starts.

If the approved target, plan, review, or runtime contract appears wrong, stale, or insufficient, stop and report the inconsistency. Append an observation only when `progress.jsonl` is available and valid.

## Writable Runtime Files

runtime writes only these control-output files:

- `progress.jsonl`
- `runtime-status.json`
- `final-report.json`

`progress.jsonl` is the append-only event log. Append to `progress.jsonl` as one JSON object per line. Each event should be a small observation about a command, evidence item, required-step state, blocker, deviation, or verifier result. Progress observations are additive; do not mutate approved JSON to make the contract match the run.

`runtime-status.json` is the current bounded status snapshot. It can summarize active step state, blockers, next action, and last evidence pointer.

`final-report.json` is the terminal report. Write it after progress evidence exists and after verifier evaluation. If the verifier does not permit completion, the final report must carry `goal_achieved: false` plus the unmet step, missing evidence, or blocker.

## Verifier Gate

Run the configured verifier before `goal_achieved: true`. The verifier command or module should come from `runtime.control.json`, the approved plan JSON, or a schema-backed run configuration. If no verifier is configured, stop.

Verifier permission means the verifier output explicitly allows or permits the completion claim for the current control chain and progress evidence. A successful command that checks only one component is supporting evidence, not completion permission.

When the verifier fails, append the verifier result to `progress.jsonl`, update `runtime-status.json`, and write a non-achieved final report only if the runtime contract calls for a terminal report.

## Short `/goal` Adapter

The `/goal` entry is a short pointer, not a control fact. It should name the runtime JSON location and this skill, for example:

```text
/goal Execute the runtime control JSON at docs/cybernetics/runs/<slug>/runtime.control.json using .agents/skills/using-control-json. Read it first; if required JSON is missing, invalid, or inconsistent, stop and report the smallest required human decision.
```

The adapter should not inline approved requirements, design, plan, review, evidence policy, work assignment, or final report prose. Those facts live in approved JSON and are interpreted through this protocol.
