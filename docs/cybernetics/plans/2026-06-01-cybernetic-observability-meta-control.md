# Execution Policy: Cybernetic Observability Meta-Control

## Execution Policy Status

Status: `Candidate`

## Source Contracts

- Requirements analysis: `docs/cybernetics/requirements/2026-06-01-cybernetic-observability-meta-control.md`
- Solution design: `docs/cybernetics/designs/2026-06-01-cybernetic-observability-meta-control.md`
- Goal contract: `docs/cybernetics/goals/2026-06-01-cybernetic-observability-meta-control.md`

## Superpowers Planning Substrate

- Required substrate: `$superpowers:writing-plans`
- Substrate status: `Used`
- Planning status: `Candidate`

Cybernetic constraints supplied to the substrate:

- confirmed semantic invariants;
- candidate solution-design invariants;
- tactical degrees of freedom;
- dependency matrix;
- execution granularity and sensor budget;
- batch cadence;
- destructive intermediate-state policy;
- output material/evidence collection;
- sensor/evidence governance;
- stale sensor retirement and rewrite policy.

The planning substrate was loaded before this policy was written. This artifact uses repository-specific file paths, task batches, verification commands, and progress checkpoints while preserving the cybernetic boundary that target implementation starts only at runtime.

## Confirmed Semantic Invariants

These cannot be changed during runtime execution without stopping.

- Metadata-only is the default recording and sync mode.
- Local recording and network sync remain separate.
- Ordinary skills may write local events but must not upload.
- Upload beyond metadata-only, including content summaries/excerpts, requires explicit opt-in and redaction.
- Real upload or issue creation requires explicit destination/token/config and must not be default.
- Cloud outputs are candidates only, not accepted control-law changes.
- No automatic skill modification, automatic release publishing, or automatic machine update.
- Events include event id and skill-pack version or source commit.
- Machine identity is pseudonymous, locally generated, and not derived from hostname by default.
- Manual sync preserves pending/sent state and refuses duplicate real sends unless explicitly forced.
- Raw prompts, content summaries/excerpts, artifact bodies, code/log excerpts, credentials, customer data, real paths, and real repository names are not uploaded by default.
- Runtime must not retire or replace approved verification commands and evidence channels; if a sensor is inadequate, runtime stops for control review or human decision.

## Tactical Degrees of Freedom

These may change during execution if invariants are preserved.

- Exact local state directory name and environment variable names.
- Whether schema validation is implemented as full JSON Schema support or repository-owned stdlib validation for the MVP, provided Batch 1 validates the sample against the required contract before dependent work begins.
- Exact CLI option names when the same contracts and safe defaults are preserved.
- Whether GitHub sync initially exports files only, uses `gh`, or uses REST, as long as real upload remains explicit and pending/sent idempotency is preserved.
- Exact test framework, with `unittest` preferred if no test dependency exists.
- Whether workflow aggregation creates issue body artifacts first before live issue creation; non-live aggregation dry-run remains required.
- Documentation placement beyond required observability docs and necessary README/MANIFEST updates.

## Dependency Matrix

| Workstream | Owns | Depends on | Can run in parallel with | Gate |
|---|---|---|---|---|
| Schema and taxonomy | `observability/schemas/`, `observability/taxonomies/`, examples, minimal `scripts/validate_run_events.py` | Requirements and design | Documentation outline | Sample event validates against schema/taxonomy contract |
| Local scripts | `scripts/record_run_event.py`, `scripts/validate_run_events.py`, `scripts/redact_run_event.py`, `scripts/sync_run_events_to_github.py` | Schema/taxonomy contracts | Recording skill after CLI contracts stabilize | Focused script checks pass, including pending/sent duplicate-send behavior |
| Tests and fixtures | `tests/observability/`, safe examples | Schema and scripts | Docs updates | Unit tests pass |
| Recording skill | `.agents/skills/recording-cybernetic-run-outcomes/` | Logger/redactor contracts | Workflow scaffolding | Skill evals cover privacy/no-upload/no-self-modification |
| Cloud aggregation scaffold | `.github/workflows/`, issue template, report/eval templates, `scripts/aggregate_run_events.py`, machine-readable summary/eval outputs | Schema/taxonomy and sync package shape | Recording skill | Workflow is inert/manual and non-live aggregation dry-run validates fixtures |
| Docs and manifest | `observability/README.md`, `README.md`, `MANIFEST.txt` | All artifact paths | Final verification | Docs state defaults and release boundaries |

## Execution Granularity and Sensor Budget

### Batch Granularity

Each batch represents a coherent target-state slice, not a mechanical micro-step.

| Batch | Coherent target-state slice | Why this is one batch | Too-small split avoided |
|---|---|---|---|
| Batch 1 | Schema, taxonomy, examples, docs skeleton, and minimal validator establish the observability contract | Every later component depends on the same event and failure vocabulary | Separate schema-only and taxonomy-only batches would create unverified contract fragments |
| Batch 2 | Local scripts and focused tests implement local record/redact/dry-run sync and idempotency behavior | These scripts form one local control surface and need shared fixtures | One-script-per-batch would overfit to isolated CLI success |
| Batch 3 | Recording skill, template, and evals bind agent behavior to local-only recording | The skill is useful only after script contracts exist | Splitting SKILL, template, and evals would leave untested behavior |
| Batch 4 | Cloud aggregation scaffold, non-live aggregation dry-run, and issue/report/eval candidate templates implement candidate-only cloud outputs | Aggregation and candidate outputs share taxonomy/version semantics | Workflow-only work without dry-run candidate outputs would be unobservable |
| Batch 5 | Integration docs, manifest updates, progress evidence, and final verification close the handoff | Final output contract requires cross-artifact evidence | Running broad checks after every prior edit would overload sensors |

Rules:

- Do not require every micro-step to be openable.
- Intermediate states inside a batch may be broken when this policy explicitly allows it.
- Each batch must end in an openable or meaningfully verifiable state.
- If a batch cannot be verified meaningfully, merge it with the next batch or redefine the gate.
- If a batch is too large to diagnose failures, split by dependency boundary or sensor boundary.

### Sensor Budget

| Batch | Required strong sensors | Optional/weak sensors | Deferred sensors | Final-only sensors |
|---|---|---|---|---|
| Batch 1 | Schema/example validator check; taxonomy parse check | Markdown wording scan | Full test suite | Final privacy/release grep |
| Batch 2 | `py_compile`; focused script/unit tests; dry-run outputs | Help text review | Workflow validation | Full repository artifact scan |
| Batch 3 | Skill eval structure; grep for upload/self-modification prohibitions | Manual read of skill prose | Runtime `/goal` execution evidence | Full final report |
| Batch 4 | Workflow syntax/readability checks; non-live aggregation fixture dry-run; machine-readable summary/eval-candidate output checks | Live GitHub upload or issue creation | Live upload and issue creation unless explicitly configured | Final candidate-output evidence |
| Batch 5 | Unit test discovery; focused CLI checks; final grep; progress log review | External GitHub execution if credentials unavailable | None unless environment lacks optional tools | Final response evidence |

Rules:

- Use the smallest sensor set that can detect semantic or structural drift.
- Do not run expensive broad checks at every batch unless they are the only reliable drift sensor.
- Treat broad verification as integration-gate or completion-gate work by default.
- If many sensors fail because they encode old semantics, preserve the target state and stop for control review or human decision before retiring or rewriting approved sensors.

## Batch Cadence

- Intermediate steps inside a batch may temporarily break local observability or artifact consistency when necessary.
- Each batch must end in an openable or meaningfully verifiable state.
- Batch size should avoid both micro-step local minima and huge unobservable changes.
- Commit cadence may follow batch boundaries unless the human requests a different commit strategy.

## Destructive Intermediate-State Policy

Allowed inside a batch:

- Creating new directories before their contents are complete.
- Adding scripts before every CLI path is wired, if batch-end checks cover them.
- Adding workflow scaffolding before live GitHub execution is possible.
- Updating README/MANIFEST after artifacts exist rather than before.

Not allowed even inside a batch:

- Enabling real upload by default.
- Adding automatic skill modification, release publishing, or machine update.
- Adding credentials, real paths, real repository names, raw prompts, code/log excerpts, or artifact bodies to fixtures.
- Moving or deleting existing cybernetic skills unrelated to observability.
- Treating cloud-generated candidates as accepted changes.

Batch-end requirements:

- Batch 1: sample event validates against the chosen repository-owned validation contract, taxonomy parses, and the sample contains event id, version identity, and non-hostname pseudonymous machine id.
- Batch 2: scripts compile and focused script tests/dry-runs pass, including pending/sent state and duplicate-send refusal.
- Batch 3: recording skill exists with evals showing local-only/no-upload/no-self-modification behavior.
- Batch 4: aggregation scaffold is manual/inert by default and a non-live dry-run produces machine-readable summary and eval-candidate outputs only.
- Batch 5: final checks pass and progress/final report evidence is ready.

## Output Material / Evidence Collection

| Required output material | Producing batch/checkpoint | Evidence reference location | Ready before final output? | Missing material blocks completion? |
|---|---|---|---|---|
| Machine-readable run-event schema | Batch 1 | `observability/schemas/run-event.schema.json` and validator output | yes | yes; scripts and workflow need it |
| Failure taxonomy | Batch 1 | `observability/taxonomies/failure-taxonomy.yaml` | yes | yes; aggregation cannot classify patterns |
| Safe metadata-only sample event | Batch 1 | `observability/examples/metadata-only-event.json` | yes | yes; redaction/sync tests need it |
| Local logger, validator, redactor, sync helper | Batch 1 and Batch 2 | `scripts/` and focused command output | yes | yes; MVP requires local recording and manual sync path |
| Pending/sent sync ledger and duplicate-send evidence | Batch 2 | sync dry-run/test output and progress log | yes | yes; runtime must not invent idempotency semantics |
| Tests/fixtures | Batch 2 and Batch 5 | `tests/observability/` and unit-test output | yes | yes if equivalent command evidence is absent |
| Recording skill and evals | Batch 3 | `.agents/skills/recording-cybernetic-run-outcomes/` | yes | yes; agent-facing local recording is required |
| Aggregation workflow, candidate templates, and machine-readable summary/eval outputs | Batch 4 | `.github/`, `observability/templates/`, `scripts/aggregate_run_events.py`, `observability/examples/aggregation-summary.json`, `observability/examples/eval-candidates.json`, aggregation dry-run output | yes | yes; runtime must not invent aggregation output contracts |
| Privacy/release documentation | Batch 5 | `observability/README.md`, README/MANIFEST updates | yes | yes; maintainers need the boundary |
| Final verification evidence | Batch 5 | progress log and final response | yes | yes |

Final output readiness:

- Progress log includes each batch's commands and sensor interpretation.
- Final response can cite concrete paths and command results for every major invariant.
- Any deferred or unavailable sensor is documented with reason and residual risk.

Blocking missing material:

- Missing redaction evidence, dry-run refusal evidence, version identity, or no-self-modification boundary blocks completion.

## Sensor / Evidence Governance

Approved sensors, checks, and evidence channels are sensors, not objectives.

Strong sensors to preserve:

- `python3 -m py_compile` for new scripts.
- Repository-owned event validation command.
- Focused unit tests for redaction and dry-run sync.
- Focused unit tests for pending/sent ledger behavior and duplicate-send refusal.
- Non-live aggregation dry-run that emits machine-readable summary and eval-candidate outputs.
- Grep checks for prohibited automatic behavior and unsafe defaults.
- Progress log entries with command output summaries.

Weak or stale sensors to inspect before obeying:

- Live GitHub upload behavior when credentials or destination are absent.
- Workflow execution in environments without GitHub Actions.
- README/MANIFEST presence before target artifacts exist.

Obsolete sensors that may be proposed for retirement or rewrite only after review:

- Any future check that assumes observability must run on every ordinary skill invocation.
- Any fixture that uses real paths, real repo names, or raw content as sample data.

Target-state evidence has priority over preserving brittle old sensors, but runtime must not replace approved sensors on its own.

## Stale Sensor Retirement and Rewrite Policy

A sensor, check, or evidence channel may be proposed for retirement or rewrite when:

- it encodes old requirement semantics;
- it over-constrains execution details;
- it conflicts with confirmed semantic invariants;
- it prevents correct structural change;
- it requires live credentials for a path that the goal defines as dry-run or optional.

Runtime must not retire or replace an approved sensor, check, verification command, or evidence channel by itself. If an approved sensor is inadequate, obsolete, unavailable, or conflicts with confirmed semantics, runtime must stop and report the smallest required control review or human decision. Any reviewed sensor change must be recorded in the progress log with reason and replacement evidence coverage.

## Phase Gates

Before execution:

- control review status must be Approved.

Before moving to next batch:

- current batch-end condition met;
- required strong sensors for this batch have been interpreted;
- deferred and final-only sensors remain deferred by policy, not by omission;
- progress log updated;
- no confirmed semantic invariant violated.

Before completion:

- final verification evidence recorded;
- no unresolved conflict among requirements analysis, solution design, goal, plan, and review;
- final output contract material is present.

## Execution Rhythm

- Execute serially unless review explicitly approves parallel subagents.
- If subagents are used during runtime, use them only for disjoint verification or implementation slices named in the progress log.
- Do not let runtime `/goal` rewrite this policy.

## Stop Conditions

Stop if:

- the plan conflicts with requirements analysis or goal;
- the plan conflicts with required solution design;
- confirmed semantics appear wrong or insufficient;
- sensor governance is insufficient for a failing check;
- an approved verification command or evidence channel is inadequate and cannot be executed as reviewed;
- executing further requires a new human decision;
- the approved batch cadence cannot be followed;
- real upload, issue creation, or release behavior becomes required for MVP completion;
- a default behavior would upload unsafe content or modify/release/update skills automatically.

## Progress Log Rules

Maintain:

- `docs/cybernetics/progress/2026-06-01-cybernetic-observability-meta-control.md`

Each entry must include:

- batch/checkpoint
- files changed
- commands run
- result
- sensor interpretation
- deferred/final-only sensors and reason
- current risk
- next step

## Candidate Plan Tasks

### Batch 1: Schema, Taxonomy, and Safe Examples

Goal:

- Establish the machine-readable event and failure-vocabulary contracts used by all later artifacts.

Allowed intermediate breakage:

- `observability/` may exist before every file is populated.
- The validator may be minimal in Batch 1 and extended in Batch 2, but Batch 1 must still validate the sample against required schema/taxonomy fields before dependent work begins.

Batch-end gate:

- Schema, taxonomy, minimal validator, sample event, and observability README skeleton exist.
- Sample event is safe metadata only and contains event id, version identity, and non-hostname pseudonymous machine id.

Batch sensors:

- Required strong sensors: run minimal validator; parse taxonomy; inspect sample event for unsafe fields.
- Deferred/final-only sensors: full unit-test discovery and final privacy grep.

Steps:

- [ ] Create `observability/schemas/run-event.schema.json` with required fields for event type, timestamp, privacy mode, pseudonymous machine id, skill pack version/source commit, status/outcome, and optional taxonomy codes.
- [ ] Create `observability/taxonomies/failure-taxonomy.yaml` with routing, requirements, design, goal, execution policy, review, runtime, and observability failure categories.
- [ ] Create `observability/examples/metadata-only-event.json` containing a safe `skill_invoked` or `route_decided` sample with no raw prompt, content summary/excerpt, artifact body, credential, real path, or real repository name.
- [ ] Create a minimal `scripts/validate_run_events.py` that can validate the sample's required fields, privacy mode, event id, version identity, taxonomy codes, and non-hostname pseudonymous machine id.
- [ ] Create `observability/README.md` skeleton documenting metadata-only defaults, local-first storage, redaction, manual sync, cloud candidate outputs, and release gates.
- [ ] Run `python3 -m json.tool observability/examples/metadata-only-event.json`.
- [ ] Run `python3 scripts/validate_run_events.py --taxonomy observability/taxonomies/failure-taxonomy.yaml observability/examples/metadata-only-event.json`.
- [ ] Update the progress log with Batch 1 evidence and deferred sensors.

### Batch 2: Local Logger, Validator, Redactor, Sync Helper, and Focused Tests

Goal:

- Implement local event recording, safe export, pending/sent idempotency, and dry-run sync behavior without network-by-default behavior.

Allowed intermediate breakage:

- Scripts may exist before tests pass.
- Sync helper may initially support dry-run/export only if real upload is gated by explicit config.

Batch-end gate:

- Scripts compile.
- Focused tests or dry-run commands demonstrate metadata-only append, validation, redaction, upload refusal without config, pending/sent state, and duplicate-send refusal.

Batch sensors:

- Required strong sensors: `py_compile`, focused unit tests, dry-run command outputs.
- Deferred/final-only sensors: full final artifact scan and optional live GitHub behavior.

Steps:

- [ ] Create `scripts/record_run_event.py` to accept CLI fields or JSON input, validate required safe metadata, and append JSONL to a local path or dry-run output.
- [ ] Extend `scripts/validate_run_events.py` to validate JSON/JSONL event batches and taxonomy codes using repository-owned stdlib checks.
- [ ] Create `scripts/redact_run_event.py` to strip, hash, or reject unsafe fields in `metadata_only` mode and report redaction actions.
- [ ] Create `scripts/sync_run_events_to_github.py` to default to dry-run/export, maintain pending/sent records, and refuse real upload or duplicate sends without explicit destination/token/config and force flag.
- [ ] Create `tests/observability/test_run_event_scripts.py` covering safe sample validation, unsafe content rejection, redaction, dry-run sync, pending/sent state, duplicate-send refusal, and no network default.
- [ ] Run `python3 -m py_compile scripts/record_run_event.py scripts/validate_run_events.py scripts/redact_run_event.py scripts/sync_run_events_to_github.py`.
- [ ] Run `python3 -m unittest discover -s tests -p 'test_*.py'`.
- [ ] Update the progress log with Batch 2 evidence and deferred sensors.

### Batch 3: Recording Skill and Evals

Goal:

- Add an agent-facing skill for local outcome recording that cannot upload or self-modify skills.

Allowed intermediate breakage:

- Skill evals may be added before docs are final.

Batch-end gate:

- Recording skill, template, and evals exist and reference local recording only.

Batch sensors:

- Required strong sensors: JSON parse for evals; negative/static scan for forbidden upload/self-modification/release/update instructions; manual interpretation recorded in progress log.
- Deferred/final-only sensors: full skill-pack eval runner if none exists locally.

Steps:

- [ ] Create `.agents/skills/recording-cybernetic-run-outcomes/SKILL.md` with boundaries: local event generation only, no upload, no skill modification, no release, no machine update.
- [ ] Create `.agents/skills/recording-cybernetic-run-outcomes/assets/run-outcome-template.md` with fields that map to safe metadata.
- [ ] Create `.agents/skills/recording-cybernetic-run-outcomes/evals/evals.json` covering metadata-only recording, content-upload refusal, no self-modification, and improvement-candidate boundaries.
- [ ] Run `python3 -m json.tool .agents/skills/recording-cybernetic-run-outcomes/evals/evals.json`.
- [ ] Run a static scan that distinguishes prohibitions from permissions and confirms the skill does not instruct upload, self-modification, release publishing, or machine update.
- [ ] Record manual interpretation of the scan in the progress log.
- [ ] Update the progress log with Batch 3 evidence and deferred sensors.

### Batch 4: Cloud Aggregation and Candidate Output Scaffold

Goal:

- Provide workflow-ready aggregation/report/issue/eval-candidate scaffolding plus non-live machine-readable aggregation outputs that remain candidate-only and manual/inert by default.

Allowed intermediate breakage:

- Workflow may be static-scaffolded if live GitHub execution is not available.
- Issue creation may be represented as a generated candidate body rather than live issue mutation.

Batch-end gate:

- Aggregation workflow/template artifacts exist, a non-live dry-run produces machine-readable summary/eval-candidate outputs, and no artifact can publish releases, modify skills, or update machines.

Batch sensors:

- Required strong sensors: static scan for forbidden release/update/write behavior; required non-live fixture aggregation dry-run; machine-readable summary/eval-candidate output validation.
- Deferred/final-only sensors: live GitHub Actions and issue creation.

Steps:

- [ ] Create `.github/workflows/aggregate-cybernetic-outcomes.yml` with manual trigger or artifact-processing scaffold, schema validation, summary artifact generation, and no automatic release/update behavior.
- [ ] Create `.github/ISSUE_TEMPLATE/cybernetic-improvement-pattern.md` for aggregate-pattern issues.
- [ ] Create `observability/templates/eval-candidate.md`, `observability/templates/weekly-summary.md`, and machine-readable output contract examples for aggregation summary and eval candidates.
- [ ] Create `scripts/aggregate_run_events.py` and focused tests for validating redacted metadata packages, grouping by taxonomy/version, and emitting `observability/examples/aggregation-summary.json` plus `observability/examples/eval-candidates.json`.
- [ ] Run `python3 scripts/aggregate_run_events.py --input observability/examples/metadata-only-event.json --out observability/examples/aggregation-summary.json --eval-candidates-out observability/examples/eval-candidates.json --dry-run`.
- [ ] Run static scans for forbidden default behavior across `.github`, `observability`, and `scripts`.
- [ ] Update the progress log with Batch 4 evidence and deferred sensors.

### Batch 5: Integration, Docs, and Final Verification

Goal:

- Close the implementation with cross-artifact evidence and final output material.

Allowed intermediate breakage:

- README/MANIFEST may be updated after all new artifacts exist.

Batch-end gate:

- Final checks pass or skipped optional sensors are justified.
- Final report material is ready.

Batch sensors:

- Required strong sensors: full unit-test discovery, focused CLI checks, final grep, progress log completeness.
- Deferred/final-only sensors: live upload and live issue creation unless explicitly configured.

Steps:

- [ ] Update `README.md` and `MANIFEST.txt` if required by repository conventions.
- [ ] Run all focused commands from the goal's `Verification Surface`.
- [ ] Run `python3 -m unittest discover -s tests -p 'test_*.py'`.
- [ ] Run final grep checks for unsafe defaults and forbidden automatic behavior.
- [ ] Review `docs/cybernetics/progress/2026-06-01-cybernetic-observability-meta-control.md` for batch evidence, deferred sensors, and residual risks.
- [ ] Produce the final response using the goal's `Final Output Contract`.
