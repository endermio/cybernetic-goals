# Goal Contract: Cybernetic Observability Meta-Control

## Human Purpose

Build a higher-level feedback loop for the cybernetic skill group so local and multi-machine use can produce process evidence, recurring failure patterns, eval candidates, and reviewed improvement proposals without allowing automatic self-modification, automatic release, or automatic machine update.

## Objective

Implement a local-first, metadata-only-by-default observability/meta-control MVP for the cybernetic skill group, using the approved solution design as the source model.

## Success Condition

Codex may stop only when:

- repository artifacts define a run-event schema, failure taxonomy, safe sample event, privacy/release documentation, local logger, validator, redactor, manual sync helper with pending/sent idempotency, recording skill, skill evals, aggregation dry-run support, and workflow-ready aggregation/issue-candidate structure;
- default behavior records only safe metadata locally and performs no network upload from ordinary skill execution;
- redaction/export refuses or removes raw prompts, content summaries/excerpts, artifact bodies, code/log excerpts, credentials, real paths, real repository names, customer data, and other unsafe content in metadata-only mode;
- real upload or issue creation is disabled unless explicitly configured and cannot happen by default;
- cloud-side automation, if scaffolded, produces reports/issues/eval candidates only and cannot modify skills, publish releases, or update machines;
- version identity is recorded in events;
- pseudonymous machine identity is locally generated and not derived from hostname by default;
- focused verification demonstrates schema validation, local JSONL append, redaction behavior, sync dry-run/refusal, pending/sent duplicate-send behavior, non-live aggregation dry-run, and recording-skill privacy boundaries;
- the progress log and final report cite evidence paths and commands.

## Source of Truth

Read first:

- `docs/cybernetics/requirements/2026-06-01-cybernetic-observability-meta-control.md`
- `docs/cybernetics/designs/2026-06-01-cybernetic-observability-meta-control.md`

## Scope and Boundaries

Allowed:

- Create `observability/` schemas, taxonomy, examples, docs, templates, and aggregation report scaffolding.
- Create local scripts under `scripts/` for recording, validating, redacting, manually syncing run events, and aggregating redacted fixture packages.
- Create tests/fixtures that validate metadata-only defaults, redaction, dry-run sync behavior, and schema/taxonomy consistency.
- Create `.agents/skills/recording-cybernetic-run-outcomes/` with skill instructions, a run outcome template, and evals.
- Create workflow-ready `.github/` workflow and issue template scaffolding that is inert unless manually triggered/configured.
- Update repository docs or manifest only when needed to expose the new observability artifacts.

Forbidden unless explicitly approved:

- Automatically modifying any installed or repository skill as a result of observed failures.
- Automatically publishing releases.
- Automatically updating machines from `main`.
- Uploading raw prompts, content summaries/excerpts, artifact bodies, code, logs, credentials, real paths, real repository names, customer data, or other sensitive content by default.
- Adding network behavior to ordinary cybernetic skills.
- Requiring every ordinary skill run to use observability as a gate.
- Treating generated issues, eval candidates, reports, or patch proposals as accepted changes.

## Invariants

Do not regress:

- Metadata-only is the default recording and sync mode.
- Local recording and network sync remain separate mechanisms.
- Ordinary skill execution may write local events but must not upload.
- Upload beyond metadata-only requires explicit opt-in and redaction.
- Real upload or issue creation requires explicit destination/token/config and must not be the default path.
- Cloud outputs remain candidates for review, not automatic skill changes.
- Skill changes require review, evals, release tagging, and pinned distribution.
- Events include event id and skill-pack version or source commit.
- Machine identity is pseudonymous, locally generated, and not derived from hostname by default.
- Manual sync preserves pending/sent state and refuses duplicate real sends unless explicitly forced.
- Sensor evidence must not override privacy, release, or no-self-modification boundaries.
- Runtime must not retire or replace approved verification commands and evidence channels; if a required sensor is inadequate, stop and report the smallest required control review or human decision.

## Verification Surface

Focused checks:

- `python3 -m py_compile scripts/record_run_event.py scripts/validate_run_events.py scripts/redact_run_event.py scripts/sync_run_events_to_github.py scripts/aggregate_run_events.py`
- `python3 scripts/validate_run_events.py observability/examples/metadata-only-event.json`
- `python3 scripts/record_run_event.py --event skill_invoked --skill routing-cybernetic-workflows --status success --dry-run`
- `python3 scripts/redact_run_event.py observability/examples/metadata-only-event.json --mode metadata_only --dry-run`
- `python3 scripts/sync_run_events_to_github.py --dry-run --input observability/examples/metadata-only-event.json`
- `python3 scripts/aggregate_run_events.py --input observability/examples/metadata-only-event.json --out observability/examples/aggregation-summary.json --eval-candidates-out observability/examples/eval-candidates.json --dry-run`

Broader checks:

- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 scripts/validate_run_events.py --taxonomy observability/taxonomies/failure-taxonomy.yaml observability/examples/metadata-only-event.json`
- `rg -n "auto.*(modify|release|update)|raw prompt|artifact body|credential|real path|real repo|metadata_only|dry-run" observability scripts .agents/skills/recording-cybernetic-run-outcomes .github README.md MANIFEST.txt`

Artifact checks:

- `observability/schemas/run-event.schema.json`
- `observability/taxonomies/failure-taxonomy.yaml`
- `observability/examples/metadata-only-event.json`
- `observability/examples/aggregation-summary.json`
- `observability/examples/eval-candidates.json`
- `observability/README.md`
- `scripts/record_run_event.py`
- `scripts/validate_run_events.py`
- `scripts/redact_run_event.py`
- `scripts/sync_run_events_to_github.py`
- `scripts/aggregate_run_events.py`
- `.agents/skills/recording-cybernetic-run-outcomes/SKILL.md`
- `.agents/skills/recording-cybernetic-run-outcomes/assets/run-outcome-template.md`
- `.agents/skills/recording-cybernetic-run-outcomes/evals/evals.json`
- `.github/workflows/aggregate-cybernetic-outcomes.yml`
- `.github/ISSUE_TEMPLATE/cybernetic-improvement-pattern.md`
- `docs/cybernetics/progress/2026-06-01-cybernetic-observability-meta-control.md`

## Final Output Contract

| Element | Requirement |
|---|---|
| Audience | Maintainer, future Codex agents, reviewers, and optional GitHub aggregation workflow users. |
| Purpose | Execution record, privacy/release assurance, implementation handoff, and evidence for reviewed process-improvement candidates. |
| Medium | Final chat summary plus persistent progress log and machine-readable repository artifacts. |
| Required structure | Final response must include: control summary, files created/changed, verification commands/results, privacy/release invariant evidence, output artifact list, and residual risks. Repository output must include schema, taxonomy, sample metadata-only event, scripts, recording skill, evals, docs, workflow/issue template scaffold, machine-readable aggregation summary, and machine-readable eval-candidate output. |
| Detail level | Standard; concise in chat, with evidence details recorded in files and command output. |
| Evidence references required | Yes. Cite file paths, command results, generated examples, and progress log entries. |
| Machine-readable required | Yes for run events, schema, taxonomy, sync packages, aggregation summaries, and eval candidates. The final chat report itself may be human-readable. |
| Destination path | Runtime progress log: `docs/cybernetics/progress/2026-06-01-cybernetic-observability-meta-control.md`; repository artifacts under `observability/`, `scripts/`, `.agents/skills/recording-cybernetic-run-outcomes/`, `.github/`, and tests/fixtures. |
| Acceptance condition | A maintainer can verify local metadata-only recording, redaction, dry-run sync, aggregation candidate flow, and no automatic self-modification/release/update behavior without runtime inventing data policy or output shape. |

Runtime must not substitute a different audience, purpose, medium, structure, detail level, evidence-reference rule, destination, or machine-readable shape. If this contract is insufficient for execution or acceptance, stop and report the smallest required upstream decision.

## Evaluation Rubric / Error Function

This is not a status-classification audit. Interpret verification against the success condition and invariants.

| Rubric element | Confirmed meaning |
|---|---|
| Status meanings / pass-fail categories | Pass only when all required artifacts, privacy boundaries, release boundaries, and focused verification evidence exist. |
| Evidence levels / evidence strength | Strong evidence is command output, schema-validated examples, tests, and generated dry-run artifacts. Weak evidence is prose without executable or machine-readable support. |
| Minimum evidence for strongest positive status | Focused checks and broader checks pass or any skipped broad check is justified by environment absence and covered by an alternative focused sensor. |
| Downgrade rules | Missing redaction evidence, missing dry-run refusal, missing version identity, or any default upload path prevents success. |
| External/unobservable dependency handling | Live GitHub upload/issue creation is optional and must be dry-run or disabled unless explicitly configured. |
| Confidence / evidence grade | Final report must state residual risks when a sensor is dry-run-only or environment-dependent. |

## Checkpoint Loop

For each checkpoint:

1. State checkpoint and expected observable state.
2. Make the smallest coherent change for that checkpoint within the approved execution policy.
3. Run the checkpoint's focused verification.
4. If verification fails, inspect evidence and repair the cause without weakening invariants.
5. Update `docs/cybernetics/progress/2026-06-01-cybernetic-observability-meta-control.md`.
6. Run broader verification only at integration or final gates unless the execution policy requires it earlier.

## Repair Policy

- Use root-cause debugging for unclear failures.
- Do not weaken privacy, release, sync, or no-self-modification invariants to satisfy convenience or sensors.
- Do not retire, replace, or rewrite approved verification sensors during runtime; if they are inadequate, stop for control review or human decision.
- Do not treat stale documentation or absent optional GitHub credentials as a reason to enable live upload.
- If a script would upload unsafe data by default, stop and repair the design-consistent boundary.
- Stop if implementation requires a new human decision about repository destination, token behavior, raw content upload, or automatic update policy.

## Progress Log

Maintain:

- `docs/cybernetics/progress/2026-06-01-cybernetic-observability-meta-control.md`

Each entry must include:

- checkpoint
- files changed
- commands run
- result
- sensor interpretation
- deferred/final-only sensors and reason
- current risk
- next step

## Stop Conditions

Stop successfully when:

- every success condition is met and final verification evidence is recorded.

Stop early and report if:

- any default path uploads raw or unredacted content;
- any ordinary skill instruction performs network sync;
- any generated cloud automation can modify skills, publish releases, or update machines automatically;
- version identity cannot be recorded in events;
- event id, pending/sent state, duplicate-send prevention, or non-hostname pseudonymous machine identity cannot be implemented;
- schema/redaction/sync dry-run verification fails and cannot be repaired without changing confirmed semantics;
- approved verification sensors are inadequate and cannot be executed as reviewed;
- live upload, issue creation, token storage, or destination selection is required to proceed;
- the approved solution design, goal, execution policy, or control review conflict.

## Blocked Report Format

If blocked, report:

- attempted paths
- evidence gathered
- current hypothesis
- exact blocker
- remaining risk
- smallest human decision or input needed

## Final Report Format

When complete, report:

- goal achieved status
- files created or changed
- verification commands and results
- evidence that metadata-only, redaction, dry-run sync, no self-modification, no auto-release, and no auto-update invariants hold
- generated machine-readable artifacts
- known residual risks
