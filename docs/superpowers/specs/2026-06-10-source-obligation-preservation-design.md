# Original Request Preservation Design

## Purpose

Prevent the control pipeline from translating a user's required action into a weaker internal target.

The recent failure mode was:

- user required empirical curve measurement and dominance decisions;
- requirements translated that into defining scan rules and a framework document;
- review, runtime, and verifier then correctly completed the weaker internal target.

This design adds an original-request layer before `required_outcomes`. The goal is not keyword linting. The goal is a completion check: each downstream outcome and evidence item must explain which part of the user's original request it completes and what proof shows that part is complete.

The first protected boundary is the translation from the approved user request into `source_requirements`. If that first translation is weaker than the user's request, the rest of the chain can still preserve the wrong target. Review and guard therefore start with:

```text
approved user request text -> source_requirements
```

Only after that check passes should the pipeline validate:

```text
source_requirements -> required_outcomes -> required_evidence -> runtime.required_steps -> verifier
```

## Scope

This implementation covers original-request preservation across:

- `analyzing-cybernetic-requirements`;
- `requirements.control.json` examples and validation;
- `reviewing-cybernetic-control-structures`;
- `control_chain_guard.py` and `control_json_runtime.py`;
- `verify_runtime_progress.py`;
- regression tests/evals for the historical `/api/v2` and complexity-curve failures.

This implementation does not cover global skill installation or `.agents` deployment drift. That is a separate release/distribution problem.

## Core Model

Add `approved_control.source_requirements` to `requirements.control.json`.

Each source requirement records one must-do item from the approved user request:

```json
{
  "id": "SR-measure-scale-curves",
  "source": {
    "kind": "user_message",
    "quote": "测 E、S、A、M、Q、K、Se、Nout、Cckpt 增长时的曲线"
  },
  "required_action": "measure scale curves for the named variables",
  "requirement_type": "produce_empirical_measurement",
  "required_evidence_strength": "measured_curve_data",
  "target_objects": ["E", "S", "A", "M", "Q", "K", "Se", "Nout", "Cckpt"],
  "completion_checks": [
    "Measured data exists for each named variable.",
    "Each curve records run parameters, measured metrics, and the timing boundary.",
    "The artifact distinguishes measured results from planned scans or rubric definitions."
  ],
  "blocks_goal_achieved_if_missing": true
}
```

`required_outcomes[*]` must link to source requirements:

```json
{
  "id": "O-measured-scale-curves",
  "statement": "Produce measured scale curves for E, S, A, M, Q, K, Se, Nout, and Cckpt.",
  "source_requirements": ["SR-measure-scale-curves"],
  "completion_claim": "Completes the request by producing actual measured curve data for the named variables, not just scan definitions.",
  "completed_target_objects": ["E", "S", "A", "M", "Q", "K", "Se", "Nout", "Cckpt"],
  "blocks_goal_achieved_if_missing": true
}
```

`required_evidence[*]` continues to live under `required_outcomes[*]`. The existing required fields such as `evidence_id`, `kind`, and `description` remain required. This design extends that object with source-request fields:

```json
{
  "evidence_id": "E-measured-scale-curves-json",
  "kind": "json_file",
  "description": "Measured scale curve data for the named variables.",
  "evidence_strength": "measured_curve_data",
  "satisfies_source_requirements": ["SR-measure-scale-curves"],
  "evidence_claim": "The file contains measured curves for the named variables with recorded runs and metrics.",
  "completed_target_objects": ["E", "S", "A", "M", "Q", "K", "Se", "Nout", "Cckpt"]
}
```

The target object fields are plain-language matching aids. They prevent same-strength but wrong-target substitutions, such as a compatibility test for future v2 exposure being used to complete an approved request for implemented `/api/v2` routes.

## No Downgrade Rule

The pipeline must not accept weaker translations of source requirements.

Allowed:

- equal-strength coverage;
- stronger coverage that still preserves the approved target and authority.

Not allowed:

- measurement becoming framework definition;
- implementation becoming readiness or compatibility;
- decision becoming decision rule only;
- root-cause diagnosis becoming a list of possible causes;
- current-run required work becoming future work.

This is not a keyword rule. Words such as "define", "plan", "rule", or "readiness" are not automatically invalid. They are invalid only when they are used as substitutes for a source requirement that asks for actual measurement, implementation, decision, repair, or diagnosis.

If a weaker target is desired, it must be a new user-approved requirements object. The current run must not auto-generate a scope-reduction path.

## Evidence Strength

Use a small evidence-strength vocabulary for structural checks:

- `behavior_exists`
- `measured_curve_data`
- `benchmark_result`
- `analysis_report`
- `framework_document`
- `review_report`
- `command_result`
- `code_change`
- `test_result`

Use a small requirement-type vocabulary:

- `implement_behavior`
- `produce_empirical_measurement`
- `analyze_existing_evidence`
- `define_framework_or_plan`
- `write_documentation`
- `verify_or_review`
- `diagnose_root_cause`
- `decide_or_classify`

The guard enforces obvious structural mismatches, for example:

- `framework_document` alone cannot satisfy `produce_empirical_measurement`;
- `review_report` cannot satisfy `implement_behavior`;
- `analysis_report` alone cannot satisfy `benchmark_result` when the source requirement requires new benchmark evidence.

Semantic equivalence is not decided by this vocabulary alone. Review must still check the plain-language completion explanation.

Minimum allowed evidence strengths:

| Requirement type | Minimum acceptable evidence strength |
| --- | --- |
| `implement_behavior` | `behavior_exists`, `code_change` plus `test_result`, or `command_result` that exercises the implemented behavior |
| `produce_empirical_measurement` | `measured_curve_data` or `benchmark_result` |
| `analyze_existing_evidence` | `analysis_report` tied to the cited source evidence |
| `define_framework_or_plan` | `framework_document` or `analysis_report` |
| `write_documentation` | `framework_document` or `analysis_report` |
| `verify_or_review` | `review_report`, `test_result`, or `command_result` |
| `diagnose_root_cause` | `analysis_report` tied to inspected evidence and a stated causal conclusion |
| `decide_or_classify` | `analysis_report` with an explicit decision/classification result and the evidence it used |

Multiple evidence items may jointly satisfy a source requirement only when the source requirement's `completion_checks` are all covered. For example, `code_change` plus `test_result` may satisfy `implement_behavior`; `framework_document` plus `analysis_report` still does not satisfy `produce_empirical_measurement` unless measured data is present.

## Review Requirements

Add a required review check:

```text
source-requirement-preservation
```

This is a new required check. It does not replace `intent-preservation`, `obligation-preservation`, or `required-outcome-coverage`; it adds the missing first boundary and source-request coverage checks. The implementation must add it to review examples, required review check sets, amendment review requirements, and corresponding tests.

The review must first compare:

```text
approved user request text -> source_requirements
```

Then it must compare:

```text
source_requirements -> required_outcomes -> required_evidence -> runtime.required_steps -> verifier
```

For each blocking source requirement, review must answer:

- What did the user ask to be done?
- Does the source requirement preserve that request without weakening it?
- Which required outcome completes that request?
- Which evidence proves that request was completed?
- Do the named target objects still match?
- Are the completion checks inspectable rather than self-attesting?
- Is any downstream artifact only preparing, explaining, defining, or scheduling the work instead of actually doing the requested work?
- Is the coverage equal or stronger than the original request?

If the answer is not defensible, the review returns `needs_revision` to requirements or the earliest downstream artifact that introduced the weakening.

## Guard And Runtime Validation

`control_chain_guard.py` and `control_json_runtime.py` must validate:

- `approved_control.source_requirements` is present for newly generated official JSON control runs using `requirements.control.schema_version >= 1.1.0`;
- each blocking source requirement has a unique id and required fields;
- each blocking source requirement has at least one source quote or source reference, a requirement type, a required evidence strength, and at least one completion check;
- every blocking source requirement is covered by at least one blocking `required_outcome`;
- every blocking `required_outcome` links to known source requirements;
- every linked required outcome states a completion claim and completed target objects when the source requirement has target objects;
- required evidence that claims a source requirement uses an allowed `evidence_strength`;
- required evidence that claims a source requirement states an evidence claim and completed target objects when the source requirement has target objects;
- runtime required steps preserve source requirement coverage through their satisfied outcomes;
- verifier required outcomes cover all blocking outcomes that carry blocking source requirements.

These checks are structural. They prevent missing links and obviously weaker evidence, but they do not replace review's plain-language judgment about whether the original request is actually completed.

## Verifier Behavior

`verify_runtime_progress.py` must reject final completion when:

- a blocking source requirement has no completed evidence;
- completed evidence only satisfies a required outcome but not the linked source requirement;
- evidence strength is weaker than the source requirement's required strength;
- an unresolved amendment says current strategy cannot complete a source requirement.

The final report should include completed and missing source requirements alongside completed required outcomes.

Verifier completion algorithm:

1. Read the current generation from `run.control.json`.
2. Read completed mainline progress events for the current generation.
3. Collect completed `evidence_id` values from those events.
4. For each `required_outcomes[*].required_evidence[*]` whose `evidence_id` was completed, collect its `satisfies_source_requirements`.
5. Count a source requirement as completed only when its completion checks are covered by completed evidence with acceptable evidence strength.
6. Reject `goal_achieved` if any blocking source requirement remains incomplete.

## Runtime Amendment Interaction

If runtime observes that the current strategy can only produce weaker evidence, it must propose an amendment instead of claiming completion.

Example:

```text
The current strategy can define scan rules, but cannot produce measured curves.
```

This must become:

```text
control.amendment.proposed
```

Amendment proposal events must include:

```json
{
  "affected_source_requirements": ["SR-measure-scale-curves"]
}
```

The amendment may revise design, plan, runtime steps, instrumentation, or verifier configuration if source requirements, required outcomes, authority, and semantic base remain unchanged. It may not change the source requirement into a weaker target.

## Regression Coverage

Add fixtures/evals for:

1. `/api/v2 implementation` translated to future v2 compatibility or old-path readiness: must fail.
2. `measure scale curves` translated to scan matrix/framework document only: must fail.
3. User quote asks for measurement, but `source_requirements` itself says framework definition: must fail before downstream outcome checks.
4. User quote asks for `/api/v2` implementation, but `source_requirements` itself says future compatibility: must fail before downstream outcome checks.
5. `define a framework` translated to framework plus a small smoke measurement: may pass as stronger coverage when authority allows it.
6. User explicitly asks only for a plan/framework: framework evidence passes and is not misclassified as too weak.
7. A semantically weak rewrite without obvious keywords still fails, such as "API surface is compatible with future v2 exposure" replacing route implementation.

## Acceptance Criteria

- New requirements examples include source requirements and source-linked outcomes/evidence.
- Review examples include `source-requirement-preservation`.
- Guard rejects missing source requirement coverage.
- Guard rejects weaker evidence-strength substitutions.
- Verifier rejects final completion when source requirements are not completed.
- Negative regression tests fail before the fix because the bad run is accepted; after the fix they pass by asserting the bad run is rejected.
- No keyword-only lint is introduced.
- Existing pure documentation tasks still pass when their source requirements are documentation or framework-definition requirements.
