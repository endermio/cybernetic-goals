# Source Obligation Preservation Design

## Purpose

Prevent the control pipeline from translating a user's required action into a weaker internal target.

The recent failure mode was:

- user required empirical curve measurement and dominance decisions;
- requirements translated that into defining scan rules and a framework document;
- review, runtime, and verifier then correctly completed the weaker internal target.

This design adds a source-level obligation layer before `required_outcomes`. The goal is not keyword linting. The goal is a truth-making check: each downstream outcome and evidence item must explain how it makes the original user obligation true.

## Scope

This implementation covers source obligation preservation across:

- `analyzing-cybernetic-requirements`;
- `requirements.control.json` examples and validation;
- `reviewing-cybernetic-control-structures`;
- `control_chain_guard.py` and `control_json_runtime.py`;
- `verify_runtime_progress.py`;
- regression tests/evals for the historical `/api/v2` and complexity-curve failures.

This implementation does not cover global skill installation or `.agents` deployment drift. That is a separate release/distribution problem.

## Core Model

Add `approved_control.source_obligations` to `requirements.control.json`.

Each source obligation records an approved user-level obligation:

```json
{
  "id": "SO-measure-scale-curves",
  "source": {
    "kind": "user_message",
    "quote": "测 E、S、A、M、Q、K、Se、Nout、Cckpt 增长时的曲线"
  },
  "required_action": "measure scale curves for the named variables",
  "obligation_type": "produce_empirical_measurement",
  "required_evidence_strength": "measured_curve_data",
  "blocks_goal_achieved_if_missing": true
}
```

`required_outcomes[*]` must link to source obligations:

```json
{
  "id": "O-measured-scale-curves",
  "statement": "Produce measured scale curves for E, S, A, M, Q, K, Se, Nout, and Cckpt.",
  "source_obligations": ["SO-measure-scale-curves"],
  "makes_true": "The named variables have actual measured curve data, not just scan definitions.",
  "blocks_goal_achieved_if_missing": true
}
```

`required_evidence[*]` must also describe the source obligation it proves:

```json
{
  "evidence_id": "E-measured-scale-curves-json",
  "kind": "json_file",
  "evidence_strength": "measured_curve_data",
  "satisfies_source_obligations": ["SO-measure-scale-curves"],
  "proves_true": "The file contains measured curves for the named variables with recorded runs and metrics."
}
```

## No Downgrade Rule

The pipeline must not accept weaker translations of source obligations.

Allowed:

- equal-strength coverage;
- stronger coverage that still preserves the approved target and authority.

Not allowed:

- measurement becoming framework definition;
- implementation becoming readiness or compatibility;
- decision becoming decision rule only;
- root-cause diagnosis becoming a list of possible causes;
- current-run required work becoming future work.

This is not a keyword rule. Words such as "define", "plan", "rule", or "readiness" are not automatically invalid. They are invalid only when they are used as substitutes for an obligation that requires actual measurement, implementation, decision, repair, or diagnosis.

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

Use a small obligation-type vocabulary:

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
- `analysis_report` alone cannot satisfy `benchmark_result` when the source obligation requires new benchmark evidence.

Semantic equivalence is not decided by this vocabulary alone. Review must still check the truth-making explanation.

## Review Requirements

Add a required review check:

```text
source-obligation-preservation
```

The review must compare:

```text
source_obligations -> required_outcomes -> required_evidence -> runtime.required_steps -> verifier
```

For each blocking source obligation, review must answer:

- What state must become true?
- Which required outcome makes that state true?
- Which evidence proves it true?
- Is any downstream artifact only preparing, explaining, defining, or scheduling the work instead of making it true?
- Is the coverage equal or stronger than the original obligation?

If the answer is not defensible, the review returns `needs_revision` to requirements or the earliest downstream artifact that introduced the weakening.

## Guard And Runtime Validation

`control_chain_guard.py` and `control_json_runtime.py` must validate:

- `approved_control.source_obligations` is present for official Level 3/4 runs;
- each blocking source obligation has a unique id and required fields;
- every blocking source obligation is covered by at least one blocking `required_outcome`;
- every blocking `required_outcome` links to known source obligations;
- required evidence that claims a source obligation uses an allowed `evidence_strength`;
- runtime required steps preserve source obligation coverage through their satisfied outcomes;
- verifier required outcomes cover all blocking outcomes that carry blocking source obligations.

These checks are structural. They prevent missing links and obviously weaker evidence, but they do not replace review's semantic truth-making judgment.

## Verifier Behavior

`verify_runtime_progress.py` must reject final completion when:

- a blocking source obligation has no completed evidence;
- completed evidence only satisfies a required outcome but not the linked source obligation;
- evidence strength is weaker than the source obligation's required strength;
- an unresolved amendment says current strategy cannot make a source obligation true.

The final report should include completed and missing source obligations alongside completed required outcomes.

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

The amendment may revise design, plan, runtime steps, instrumentation, or verifier configuration if source obligations, required outcomes, authority, and semantic base remain unchanged. It may not change the source obligation into a weaker target.

## Regression Coverage

Add fixtures/evals for:

1. `/api/v2 implementation` translated to future v2 compatibility or old-path readiness: must fail.
2. `measure scale curves` translated to scan matrix/framework document only: must fail.
3. `define a framework` translated to framework plus a small smoke measurement: may pass as stronger coverage when authority allows it.
4. User explicitly asks only for a plan/framework: framework evidence passes and is not misclassified as too weak.
5. A semantically weak rewrite without obvious keywords still fails, such as "API surface is compatible with future v2 exposure" replacing route implementation.

## Acceptance Criteria

- New requirements examples include source obligations and source-linked outcomes/evidence.
- Review examples include `source-obligation-preservation`.
- Guard rejects missing source obligation coverage.
- Guard rejects weaker evidence-strength substitutions.
- Verifier rejects final completion when source obligations are not completed.
- Historical regression fixtures reproduce the two known failures and fail before the fix, pass after the fix.
- No keyword-only lint is introduced.
- Existing pure documentation tasks still pass when their source obligations are documentation or framework-definition obligations.
