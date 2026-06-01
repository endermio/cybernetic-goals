# Cybernetic Solution Design: Cybernetic Observability Meta-Control

## Design Status

Status: `Candidate`

## Source Contracts

- Requirements analysis: `docs/cybernetics/requirements/2026-06-01-cybernetic-observability-meta-control.md`
- Rubric, if any: not applicable
- Existing source-artifact context:
  - `.agents/skills/`
  - `docs/cybernetics/`
  - `docs/cybernetic-framework/superpowers-infrastructure-policy.md`

## Human Purpose

Create a local-first feedback loop for the cybernetic skill group so repeated use across machines produces process evidence, failure-pattern visibility, eval candidates, and improvement proposals without allowing the skill system to rewrite, release, or update itself automatically.

## Confirmed Semantics

- The system may automatically observe, summarize, and propose improvements.
- The system must not automatically modify installed skills.
- The system must not automatically publish releases.
- The system must not automatically update machines from `main`.
- Local recording defaults to safe metadata only.
- Raw prompts, content summaries/excerpts, artifact bodies, code, logs, credentials, customer data, real paths, and real repository names are not uploaded by default.
- Upload beyond metadata-only requires explicit opt-in and redaction.
- Ordinary skills may write local events but must not perform network sync.
- Sync, aggregation, issue creation, and eval-candidate creation belong to scripts or GitHub automation.
- Skill changes require review, evals, release tagging, and pinned distribution.
- Events must carry skill-pack version or source commit.
- Observability is adjacent process-improvement infrastructure, not a required gate for every ordinary task.

## Design Substrate

- Design Gate: `Required`
- `$superpowers:brainstorming` status: `Not required`
- Reason: the requirements analysis already fixes the conservative privacy, release, sync, and self-modification boundaries. The remaining design work is solution-model synthesis from confirmed requirements, not open-ended exploration.

## Conceptual Design

### Core Objects / Actors / Roles

| Concept | Meaning | Notes |
|---|---|---|
| Run event | One metadata-only observation about skill usage, routing, artifact creation, blocking, human feedback, or runtime outcome | Stored as JSON-compatible data and validated by schema |
| Event schema | Machine-readable contract for run events | Defines allowed event types, required metadata, privacy defaults, and version fields |
| Failure taxonomy | Controlled vocabulary for recurring process failures | Used for aggregation and eval-candidate generation |
| Local event store | Local append-only JSONL storage | Default location is user-local state; repository-local fixtures are only examples/tests |
| Recording skill | Agent-facing skill for summarizing a run outcome into local events | It records locally only and does not upload |
| Local logger | Script that appends schema-shaped events to the local event store | No network behavior |
| Redactor | Script that removes, hashes, or rejects sensitive fields before export | Required before optional content upload |
| Sync package | Metadata-only export bundle selected for manual upload | Must be inspectable before upload |
| Sync ledger | Local pending/sent record of packages and event ids | Prevents duplicate upload and preserves manual sync lifecycle |
| Manual sync | Explicit operator action to send a package to a configured target | Defaults to dry-run or file export unless configured |
| Cloud intake | GitHub-side validation of uploaded metadata packages | Rejects schema-invalid or unsafe payloads |
| Aggregator | Workflow logic that groups run events into patterns | Produces summaries, issues, and eval candidates |
| Aggregation summary | Machine-readable grouped outcome report | Used by maintainers and candidate-generation tooling |
| Eval candidate package | Machine-readable plus human-readable candidate regression case | Candidate only; requires review before becoming an eval |
| Improvement candidate | Report finding, issue, eval candidate, or patch proposal | Candidate only; not an accepted control-law change |
| Release gate | Human/reviewed PR, eval pass, tag, and pinned install/update path | Prevents uncontrolled self-modification |
| Version identity | Skill pack commit/tag, skill name, skill version, and optional adapter version | Required for attributing failures to versions |
| Maintainer/reviewer | Human or independent reviewer who accepts or rejects improvement candidates | Owns control-law change decisions |

### Relationships

- A run event conforms to the event schema and may reference failure taxonomy entries.
- The recording skill invokes the local logger but never invokes manual sync.
- The local logger writes to the local event store; it does not redact or upload by itself.
- The redactor reads local events and produces an exportable sync package.
- The sync ledger records package ids, event ids, destination identity hashes, dry-run/export/upload state, and sent status.
- Manual sync transmits only an allowed sync package to cloud intake and must consult the sync ledger before re-sending.
- Cloud intake validates packages before aggregation.
- The aggregator produces machine-readable aggregation summaries, reports, issues, and eval candidates as improvement candidates.
- Improvement candidates enter the release gate; they do not directly modify skills.
- Version identity is attached to every run event so aggregation can distinguish old failures from current regressions.

### Information / State Flow

1. A cybernetic run reaches a meaningful event point: skill invocation, routing decision, artifact creation, blocked status, human feedback, or runtime outcome.
2. The recording skill or local script normalizes safe metadata into a run event.
3. The local logger validates the event shape and appends it to JSONL storage.
4. Optional redaction/export reads local JSONL and produces a metadata-only sync package, with content fields and content summaries/excerpts disabled unless explicitly configured.
5. The sync package enters pending state with a deterministic package id or event-id set.
6. Manual sync sends the inspected package to a configured GitHub destination or writes a dry-run/export file, then records sent state only for confirmed real sends.
7. GitHub aggregation validates incoming package shape, groups failures by taxonomy/version, and produces a machine-readable summary artifact plus reviewable human-readable report material.
8. Aggregation may create an issue or eval-candidate artifact for recurring patterns.
9. Maintainers review candidates through ordinary repository change control before any skill file, release, or machine update changes.

### Boundaries

Inside scope:

- `observability/` schemas, taxonomy, examples, docs, and report/eval candidate templates.
- `scripts/` local logger, validator, redactor, and manual sync helper.
- `.agents/skills/recording-cybernetic-run-outcomes/` skill, template, and evals.
- Workflow-ready `.github/` workflow and issue template scaffolding for aggregation and candidate creation, inert unless manually triggered or configured.
- Tests/fixtures showing metadata-only defaults, redaction behavior, schema validation, and dry-run sync behavior.

Outside scope:

- Automatic edits to installed skills or repository skill files.
- Automatic release publishing.
- Automatic multi-machine update.
- Default upload of raw prompts, content summaries/excerpts, code, logs, artifact bodies, credentials, real paths, real repo names, or customer data.
- Network operations from ordinary skill execution.
- A full dashboard product.
- Domain-adapter-specific telemetry as part of the core MVP.

### Alternative Concepts Considered

| Option | Accepted / Rejected | Rationale |
|---|---|---|
| Skills upload events directly | Rejected | It mixes ordinary skill execution with network and token risk. |
| Sync every raw artifact body for full diagnosis | Rejected | It violates metadata-only default and privacy invariants. |
| One failure creates one GitHub issue | Rejected | It creates noisy, low-value process feedback. |
| Cloud workflow opens candidate issues only after aggregation | Accepted | It preserves observability value while limiting issue noise. |
| Cloud workflow directly commits skill fixes | Rejected | It lets the control system modify its own control law. |
| Versioned local event schema plus taxonomy | Accepted | It makes multi-machine evidence attributable and comparable. |

### Conceptual Invariants

- Local observation is allowed; automatic self-modification is not.
- Metadata-only is the default collection and sync mode.
- Content upload requires explicit opt-in and redaction.
- Manual sync is separate from local recording.
- Manual sync must preserve pending/sent lifecycle and idempotency; duplicate sends require an explicit operator action.
- Cloud outputs are candidates, not accepted changes.
- Release and update behavior stays pinned, reviewed, and versioned.
- Machine identity is pseudonymous, locally generated, and not derived from hostname by default.
- Sensor/evidence records must not become objectives that override privacy or release boundaries.

## Detailed Design

### Components / Mechanisms

| Component / Mechanism | Responsibility | Inputs | Outputs |
|---|---|---|---|
| `observability/schemas/run-event.schema.json` | Define run-event shape, required fields, allowed event kinds, privacy mode, and version metadata | Requirements and event model | JSON schema |
| `observability/taxonomies/failure-taxonomy.yaml` | Define process-failure categories and stable codes | Requirements failure taxonomy | YAML taxonomy |
| `observability/examples/metadata-only-event.json` | Provide a safe sample event | Event schema | Sample metadata-only event |
| `observability/README.md` | Document local-first behavior, privacy defaults, manual sync, cloud aggregation, and release gates | Requirements/design | Maintainer docs |
| `scripts/record_run_event.py` | Append schema-shaped events to local JSONL | CLI args or JSON input | Local JSONL event |
| `scripts/validate_run_events.py` | Validate event files using repository-owned schema constraints | JSON/JSONL files | Pass/fail diagnostics |
| `scripts/redact_run_event.py` | Redact or reject unsafe fields before export | Event file/package | Redacted JSON/JSONL |
| `scripts/sync_run_events_to_github.py` | Dry-run/export by default; optionally upload when explicitly configured; maintain pending/sent idempotency | Redacted package and config | Dry-run summary, export package, or upload result |
| `scripts/aggregate_run_events.py` | Validate redacted packages, group by taxonomy/version, and emit candidate summaries | Redacted packages | Machine-readable summary and eval-candidate data |
| `.agents/skills/recording-cybernetic-run-outcomes/SKILL.md` | Instruct agents how to record local run outcomes without upload | Current artifacts/outcome | Local event write instructions |
| `.agents/skills/recording-cybernetic-run-outcomes/assets/run-outcome-template.md` | Human-readable run summary source for events | Run outcome details | Structured summary |
| `.agents/skills/recording-cybernetic-run-outcomes/evals/evals.json` | Regression cases for privacy and non-upload behavior | Skill behavior prompts | Eval cases |
| `.github/workflows/aggregate-cybernetic-outcomes.yml` | Validate and aggregate uploaded metadata packages when manually supplied | Workflow input/artifact | Machine-readable summary artifact and candidate outputs |
| `.github/ISSUE_TEMPLATE/cybernetic-improvement-pattern.md` | Standardize aggregate-pattern issue reports | Aggregation output | Maintainer-reviewable issue body |

### Interfaces / Contracts

- Run-event contract:
  - event type is one of `skill_invoked`, `route_decided`, `artifact_created`, `blocked`, `human_feedback`, or `runtime_outcome`;
  - each event includes event id, timestamp, pseudonymous locally generated machine id, skill-pack version or commit, privacy mode, and source skill when applicable;
  - machine id is not derived from hostname by default;
  - no raw prompt, content summary/excerpt, artifact body, credential, code excerpt, real path, or real repository name is required or allowed by default.
- Logger contract:
  - accepts CLI fields and/or one JSON object;
  - validates required metadata before append;
  - writes JSONL locally;
  - does not perform network operations.
- Redaction contract:
  - strips or hashes disallowed fields in metadata-only mode;
  - rejects content fields and content summaries/excerpts unless an explicit opt-in mode is provided;
  - reports redaction actions.
- Sync contract:
  - defaults to dry-run/export;
  - refuses real upload without explicit destination and token/config;
  - sends only redacted metadata packages;
  - records pending and sent state using event ids, package ids, destination identity hashes, timestamp, and response id when available;
  - prevents duplicate real sends for the same package/destination unless explicitly forced;
  - reports the target, event counts, taxonomy counts, idempotency state, and blocked reasons.
- Cloud aggregation contract:
  - validates schema before aggregation;
  - groups by taxonomy, skill, version, and outcome;
  - emits machine-readable aggregation summaries and eval-candidate data;
  - creates reports/issues/eval candidates only as reviewable candidates.
- Release contract:
  - no candidate can become an installed skill change without PR/review/eval/release and pinned installation/update.

### State Model / Lifecycle

| State | Meaning | Allowed transition |
|---|---|---|
| Observed | A meaningful cybernetic run event exists in local context | Normalize to run event |
| Recorded | Event is appended to local JSONL | Validate, redact/export, or remain local |
| Pending export | Event/package selected for manual sync | Redact or reject |
| Redacted | Package contains only allowed fields for the chosen mode | Dry-run/export/upload |
| Pending send | Redacted package is ready for a configured destination | Dry-run, export, send, or cancel |
| Sent | Package was explicitly sent to a destination and recorded in sent ledger | Cloud intake validation or duplicate-send refusal |
| Aggregated | Cloud grouped events into patterns | Report, issue candidate, eval candidate |
| Candidate reviewed | Maintainer/reviewer evaluated candidate | PR/eval/release or reject |
| Released | Reviewed skill/eval/docs changes are tagged and versioned | Machines may install pinned release |

### Error / Failure / Exception Model

- Schema-invalid events are rejected before append or recorded as local validation failures without upload.
- Missing version identity blocks sync readiness because aggregation cannot attribute behavior.
- Missing event id, package id, destination identity, pending state, or sent ledger data blocks real sync readiness.
- Missing token, repo, or destination blocks real upload but not dry-run/export.
- Duplicate package/destination sends are refused unless the operator explicitly forces resend and the progress/evidence record states why.
- Unsafe fields in metadata-only mode, including content summaries/excerpts, are removed or cause export refusal.
- Issue creation failures produce a report artifact rather than retrying unboundedly.
- Cloud aggregation failures do not affect local recording.
- Any candidate that would edit skills, publish a release, or update machines automatically is rejected by design.

### Evidence / Sensor Model

- Schema validation passes for safe sample events.
- Logger writes JSONL locally with no network requirement.
- Redactor removes or rejects raw prompt, content summary/excerpt, artifact body, credential, real path, and real repo fields by default.
- Sync dry-run reports event counts, pending/sent state, and refuses real upload without explicit configuration.
- Duplicate-send fixtures prove idempotency behavior.
- Aggregation workflow or script validates sample packages and produces a machine-readable summary artifact plus eval-candidate data.
- Recording skill evals assert no upload and no self-modification.
- Documentation states metadata-only defaults, opt-in content rules, manual sync, cloud candidate boundaries, and release gates.

### Output Contract Design

| Output element | Design |
|---|---|
| Audience | Maintainers, future Codex agents, reviewers, and optional GitHub aggregation workflow. |
| Purpose | Execute implementation safely, preserve privacy/release invariants, validate metadata, aggregate recurring failures, and create reviewable improvement/eval candidates. |
| Medium / destination | Repository artifacts under `observability/`, `scripts/`, `.agents/skills/recording-cybernetic-run-outcomes/`, workflow-ready `.github/`, tests/fixtures, and runtime progress under `docs/cybernetics/progress/2026-06-01-cybernetic-observability-meta-control.md`. |
| Required structure | Machine-readable schema, taxonomy, sample metadata-only event, local scripts, recording skill, evals, documentation, workflow/issue template scaffold, machine-readable aggregation summary/eval-candidate outputs, and final implementation report with verification evidence. |
| Detail-level split | Runtime final report is standard detail: concise summary, changed files, verification commands/results, privacy/release invariant evidence, and residual risks. Repository docs provide detailed operator guidance. |
| Evidence-reference rules | Every final claim must cite a file path, command result, test/fixture, dry-run result, or generated artifact. |
| Machine-readable shape | Required for run events, schema, taxonomy, sync package, aggregation summary, and eval candidate files. |
| Acceptance condition | A maintainer can inspect local recording, redaction, dry-run sync, aggregation candidate flow, and release boundaries without needing runtime to invent data policy or output shape. |

### Compatibility / Migration / Integration

- Existing cybernetic skills do not need immediate modification to adopt recording; the recording skill and scripts can be invoked manually first.
- Local state path defaults must not depend on repository checkout path.
- Repository examples and tests must use anonymized fixture paths and pseudonymous machine ids.
- Pseudonymous machine ids are locally generated and not hostname-derived by default.
- GitHub workflow must be inert unless configured or manually triggered.
- Multi-machine adoption should use release tags or pinned commits, not automatic `main` updates.

### Design Decisions

| Decision | Rationale | Risk | Reversible? |
|---|---|---|---|
| Use metadata-only as default mode | Preserves privacy and keeps default collection safe | Less diagnostic detail initially | Yes |
| Keep recording and sync separate | Prevents ordinary skill execution from needing tokens/network | More operator steps | Yes |
| Add a recording skill but keep cloud sync as scripts/CI | Lets agents produce standard local events without network authority | Requires explicit sync operation | Yes |
| Use aggregate-pattern issues | Reduces issue noise and improves process signal | Slower feedback for one-off failures | Yes |
| Treat cloud outputs as candidates | Prevents self-modifying control laws | Requires human review effort | No for safety boundary |
| Include version identity in every event | Makes regressions attributable across machines | Some local setup needed | Yes |

## Design-to-Goal Mapping

| Design element | Goal implication |
|---|---|
| Metadata-only default | Goal must forbid default upload of raw content and require tests/fixtures for default redaction behavior. |
| Recording/sync separation | Goal must forbid network behavior in ordinary skill execution and local logger. |
| Run-event schema and taxonomy | Goal must require machine-readable schema/taxonomy artifacts and validation evidence. |
| Manual sync | Goal must require dry-run/export behavior and real-upload refusal without explicit config. |
| Sync ledger and idempotency | Goal must require pending/sent state and duplicate-send prevention. |
| Cloud aggregation candidates | Goal must require candidate reports/issues/evals only, not accepted changes. |
| Machine-readable aggregation outputs | Goal must require machine-readable summary and eval-candidate artifacts. |
| Release gate | Goal must forbid auto skill modification, auto release, and auto machine update. |
| Output Contract Design | Goal must preserve final output shape and forbid runtime substitution. |

## Design-to-Execution Mapping

| Design element | Execution-policy implication |
|---|---|
| Schema and taxonomy | Implement early because logger, redactor, sync, workflow, skill evals, and docs depend on these contracts. |
| Logger/redactor/sync scripts | Use focused tests for metadata-only behavior, unsafe-field rejection, dry-run sync, pending/sent state, and duplicate-send refusal. |
| Recording skill | Implement after script contracts exist so skill instructions can reference concrete local interfaces. |
| GitHub aggregation | Require a non-live fixture aggregation dry-run; defer live GitHub Actions/issue creation to optional configured environments. |
| Release gate | Include explicit stop conditions for any implementation path that enables auto modification/release/update. |
| Output Contract Design | Execution policy must collect evidence paths, command results, fixture outputs, and generated candidate artifacts for the final report. |

## Open Design Questions

- None.

## Design Review Requirements

Review must check:

- semantic fidelity to the requirements analysis;
- internal consistency of objects, relationships, flows, and boundaries;
- privacy and release-gate invariants;
- local recording versus network sync separation;
- evidence/sensor adequacy;
- output-contract adequacy;
- boundary correctness;
- design invariants versus tactical flexibility;
- suitability as source input for goal and execution policy.
