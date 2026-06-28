# Detailed Rules Snapshot


# Analyzing Cybernetic Requirements

## Overview

Turn a formed task or task candidate into requirements control JSON before it becomes a solution design, Codex `/goal`, execution policy, or target-work change.

This skill is a pre-goal control loop:

```text
formed task -> AI context scan -> requirement meaning -> rubric/output/check analysis -> human decisions/defaults -> goal-ready requirements brief
```

Requirements analysis is broader than asking clarifying questions. Clarifying questions are one tool inside this skill. The output is not just answers to questions; it is the analyzed approved target, constraints, evaluation function, and required checks.

Official persistent control facts are JSON only. Historical Markdown may be read as non-authoritative background, but do not create or compile Markdown as official guard, compiler, runtime, or long-term dual-path control input.

Output:

- a short requirements analysis confirmation in chat, or
- `docs/cybernetics/runs/<slug>/requirements.control.json`.

Use the approved requirements control JSON shape for the run directory. Do not use Markdown templates as official control input.

## What This Skill Owns

This skill owns requirements analysis for formed tasks and task candidates.
Use `$framing-cybernetic-intent` first when the approved target is still pre-task
intent: confusion, dissatisfaction, risk sense, failed experience, method
preference, or process distrust.

Owned analysis:

- extract human purpose;
- identify requirement objects, actors, terms, limits, and non-goals;
- classify success, failure, completion, completion, usability, readiness, or pass/fail meaning;
- identify the final output audience, purpose, medium, required structure level, detail level, evidence-reference needs, machine-readable needs, destination path, and acceptance condition;
- identify how we know the user's purpose was met: who can observe purpose realization, what outcome realizes the human purpose, what feedback can judge it, and what internal checks can or cannot prove;
- identify where the result must show up when intended result must be realized across a controlled object: intended result, required result places, required action, old behavior check, and result-placement status;
- identify the work covered and allowed actions limit for full-route or multi-batch work: work covered in this run, what the agent may do, forbidden actions, unauthorized-action handling, and explicitly out-of-scope items;
- identify the path that makes the result true for implementation work: one actor-centered path from initial state to the what counts as done;
- identify how this should be answered for tasks where merely running a plausible path would not answer the question, including what is not enough;
- prepare the What the User Approved compact control commitment for `controlled_run` JSON pre-goal work: Human purpose, Input role binding, Primary object, Requested transformation, Non-goals, how we know the user's purpose was met, where the result must show up, What counts as done, Evidence needed to call it done, If it is not done, what should be reported, Required answer path, How this should be answered, What is not enough, Work covered in this run, What the agent may do, Forbidden live / irreversible actions, Required handling for unauthorized actions, Explicitly out-of-scope items, Agent delegation preference, Agent workflow preference, Parallel execution authority, Maximum parallel agents, Final answer format, Why this process is needed, and Known assumptions;
- identify constraints, rules that cannot change, assumptions, and stop conditions;
- decide whether Meaning, Rubric, Output Contract, Design, Goal, Execution Plan, Review, or Risk checks are required;
- ask high-value human questions;
- record obvious defaults without blocking progress;
- recommend the appropriate handoff for design check: direct `$designing-cybernetic-solutions` for bounded/manual chains, or `$orchestrating-cybernetic-pregoal` for `controlled_run` JSON pre-goal work.

Routed elsewhere:

- solution structure, interfaces, object structures, mechanism architecture, flows, report structures, output schemas, and lifecycle models go to `$designing-cybernetic-solutions`;
- goal control JSON goes to `$writing-cybernetic-goals`;
- execution policies go to `$writing-cybernetic-execution-policies`;
- whole-chain review goes to `$reviewing-cybernetic-control-structures`;
- runtime `/goal` compilation goes to `$compiling-cybernetic-runtime-goals`;
- target work starts only after an approved runtime `/goal`.

Requirement object lists are not solution designs. They name what the human is talking about; they do not prescribe mechanisms, interfaces, lifecycle, state flow, or execution batches.

## Preserve Requested Scope

Do not reduce, simplify, postpone, or replace the requested behavior merely because execution seems complex, risky, unstable, or hard.

Execution complexity may be recorded as execution risk, planning concern, evidence concern, or future realization challenge. It must not become the recommended default unless the human explicitly asks for a lower-risk scope.

## Preserve Original Request Items

For `controlled_run` JSON control work, extract `source_requirements` before writing `required_outcomes`. A source requirement is one must-do item from the approved user request. It must include the user's quote or source reference, required action, requirement type, required evidence strength, target objects when applicable, completion checks, and whether missing it blocks `goal_achieved`.

Do not weaken the user's request while extracting source requirements. If the user asks to measure, implement, decide, repair, or diagnose, the source requirement must preserve that action. A framework, plan, readiness result, compatibility result, or decision rule may support the work, but it cannot replace the requested action unless the user gives a new approval for the weaker target.

The compact approval summary must show each source requirement in plain language: original quote/reference, required action, evidence needed, and completion checks.

## Counterexample Gate Contract

For `controlled_run`, requirements analysis must define
`counterexample_gate_contract` before orchestration. Do not leave quality-control
scope for design, plan, review, or runtime to invent.

The contract must state:

- `quality_standard`: what an independent reviewer must try to disprove;
- `required_checked_transformations`: every decomposition or terminal-claim
  position the gate must challenge;
- `minimum_reviewer`: allowed independent reviewer kinds and whether
  `reviewer.evidence_ref` is required;
- `reject_if`: semantic failure conditions that block approval.

Each blocking `required_outcome` must also define a per-outcome
`counterexample_gate`:

- `completion_standard`: what has to be true for that outcome alone;
- `required_checked_transformations`: checks that challenge that outcome's
  completion claim;
- `required_evidence_ids`: evidence IDs from that outcome's `required_evidence`;
- `reject_if`: semantic failure conditions for that outcome.

The default checked transformations are the minimum, not the maximum:

```text
source_requirements->required_outcomes
required_outcomes->required_steps
required_steps->work_packages
required_steps->runtime_steps
pre_runtime_compile
blocked_or_goal_achieved
```

Add task-specific transformations when the user's request needs them. Later
review may require stronger evidence, but must not weaken, replace, or invent a
different quality contract.

## Information Sufficiency Check

Before controlled-run design or planning, requirements analysis must determine
whether there are facts that must be known first. These are not solution-design
choices; they are facts without which the design or plan could be invalid.

Information collection is part of requirements analysis. Do not ask for final
requirements approval while design-blocking facts still need review,
collection, user input, or requirements revision.
Do not ask for final requirements approval until the information sufficiency
state is `satisfied` or `not_required`.

When such facts exist, record `approved_control.information_sufficiency_check`
in `requirements.control.json` and use `schema_version: 1.2.0`. Each fact must
include:

- a stable `fact_id`;
- the fact statement;
- `derived_from.source_requirements` and/or `derived_from.required_outcomes`;
- `why_needed`;
- `acceptable_evidence`;
- `current_status`;
- `evidence_ref`;
- whether missing it blocks design or plan.

Do not ask design, plan, or runtime to invent this standard later. They may
gather evidence, report a blocker, or propose a reviewed amendment, but they
may not redefine what information was required before design.

Do not reduce this to an agent-filled `required_observations` checklist. A fact
is valid only when it is derived from approved source requirements/outcomes and
has acceptable evidence criteria.

`information_sufficiency_check.counterexample_review` must be independent and
must try to find missing facts that would invalidate design or plan. It must
record reviewer provenance, checked facts, checked transformations, evidence
reference, and findings. If a blocking fact is missing, unknown, weakly
evidenced, or not independently reviewed, orchestration must stop before design
or plan and route through the requirements information loop.

Use these states inside requirements analysis:

- `needs_counterexample_review`: run the independent review before approval.
- `needs_information_gathering`: gather safe read-only facts, examples, probes,
  or source/documentation observations before approval.
- `needs_user_input`: stop and ask for the missing credential, artifact,
  external access, or business decision.
- `needs_requirements_revision`: newly gathered facts change the requested
  outcome, completion standard, authority, or forbidden actions; revise the
  requirements and return to user approval.
- `satisfied` or `not_required`: the only states that can pass handoff.

Use the loop helper before asking for approval or handoff:

```bash
python3 .agents/skills/analyzing-cybernetic-requirements/scripts/requirements_information_loop.py \
  --run-dir docs/cybernetics/runs/YYYY-MM-DD-<slug> --json
```

Follow its `next_action`:

- `RunInformationCounterexampleReview`: start an internal independent reviewer;
  do not ask the user whether this review may run.
- `RunInformationGathering`: perform the listed safe read-only source/doc/probe
  actions and write their evidence.
- `AskUserForInformation`: ask only for the listed credential, external access,
  artifact, or business decision.
- `ReviseRequirements`: update requirements meaning before approval because new
  facts changed the requested result, done standard, authority, or forbidden
  actions.
- `ReadyForUserApproval`: show the approval commitment.

The helper is a transition gate, not an executor. Follow
`../references/transition-gate-protocol.md`: when `terminal` is false, perform
the returned `next_action`, update requirements/evidence as needed, and run the
same helper again before approval or handoff.

Safe collection may read source, inspect local documentation, and run
no-side-effect local probes or minimal examples. Ask the user before using
credentials, touching external systems, accessing real DEV/N1/N2 services, or
running anything that could change state.

Before asking for approval, expose these facts in plain language as
"Information needed before design": fact, why it matters, acceptable evidence,
current status, owner/source, and blocker if missing. If the independent
counterexample review has not actually run and passed, say that explicitly and
keep the requirements at pending/needs-revision. Do not mark top-level
requirements approved while writing `counterexample_review.status` as
`required_before_*`, `pending`, `planned`, or any future-work phrase.

## Ask Only High-Value Human Questions

Ask the human a question only if all are true:

1. The answer materially changes any What the User Approved compact control commitment field, including how we know the user's purpose was met, beneficiary/observer, sufficient evidence level, feedback-unavailable handling, where the result must show up, intended result, required result places, required action, old behavior check, preserved/excluded places, what counts as done, required answer path, how this should be answered, what is not enough, work covered in this run, what the agent may do, forbidden actions, unauthorized-action handling, explicit out-of-scope items, runtime delegation preference, agent workflow preference, parallel execution authority, or maximum parallel agents; or changes requirement meaning, evaluation rubric, output contract, visibility limit, authorization model, external contract meaning, observer-visible behavior, downstream consumption, acceptance condition, or control limits.
2. There are at least two plausible business choices.
3. The correct answer cannot be safely inferred from the user request, existing source artifacts, or common requirement conventions.
4. A wrong default would be costly to reverse or would cause serious misalignment.

Do not ask the human about routine execution tactics, obvious resilience behavior, execution mechanics, or design details that belong in `$designing-cybernetic-solutions`.

Use `references/decision-levels.md` for decision classification.

## What the User Approved Rule

For `controlled_run` JSON pre-goal orchestration, `Requirements Analysis Status: Complete` is not sufficient to start downstream orchestration.

The requirements analysis must also include:

```text
What the User Approved: Approved
```

unless the user explicitly approves the compact control commitment in the current message.

If the current user message approves the compact control commitment, update the requirements analysis `What the User Approved` section first, quoting or referencing that approval, then continue. Do not rely on in-memory approval to pass orchestration or runtime guards.

Human answers to clarification questions are inputs, not approval. Do not infer approval from the user merely answering questions.

Before handoff to `$orchestrating-cybernetic-pregoal`, present a compact control commitment for approval. The commitment must include:

- Human purpose;
- Input role binding;
- Primary object;
- Requested transformation;
- Non-goals;
- How we know the user's purpose was met;
- Where the result must show up;
- What counts as done;
- Evidence needed to call it done;
- If it is not done, what should be reported;
- Required answer path;
- How this should be answered;
- What is not enough;
- Work covered in this run;
- What the agent may do;
- Forbidden live / irreversible actions;
- Required handling for unauthorized actions;
- Explicitly out-of-scope items;
- Agent delegation preference;
- Agent workflow preference;
- Parallel execution authority;
- Maximum parallel agents;
- Final answer format;
- Why this process is needed;
- Known assumptions.

If the commitment is `Pending`, `Rejected`, or `Needs Revision`, keep the workflow at requirements analysis and ask the user to approve or revise the compact commitment. Do not route the user into design review, plan review, or artifact-by-artifact approval as a substitute for approved target approval.

## final-answer-format check

Output shape is part of the controlled requirement when the final artifact will be used for a decision, handoff, audit, record, downstream action, or machine consumption.

Requirements analysis must identify:

- audience;
- purpose;
- medium;
- required structure;
- detail level;
- evidence-reference needs;
- machine-readable needs;
- destination path;
- acceptance condition.

Mark `final-answer-format check: required` when:

- the output will be consumed by another actor, reviewer, downstream agent, script, or external stakeholder;
- the task is audit, evaluation, reporting, classification, handoff, or persistent record work;
- the output must be persisted as an artifact;
- the output needs a table, schema, matrix, evidence index, structured report, or artifact bundle;
- multiple audiences need different summaries;
- a wrong output shape would make the task unusable or change how execution should proceed.

Mark `final-answer-format check: satisfied` when the output contract is explicit enough to write the goal.

Mark `final-answer-format check: not applicable` when:

- the user asks a simple question;
- a direct prompt or local correction only needs a short final note;
- the output shape is obvious, low-risk, and does not affect execution or acceptance.

Do not ask output-format questions by default for simple tasks. Use safe defaults:

- chat summary for simple direct tasks;
- markdown file for persistent approved files;
- evidence table for audit or evaluation tasks;
- final report with summary, evidence, and unresolved items for runtime tasks.

Ask the human only when the output contract changes execution or acceptance and no safe default exists.

Requirements analysis may record that structured output is needed. It must not design complex report schemas, field sets, matrix layouts, or artifact bundles; defer those to `$designing-cybernetic-solutions` when structure synthesis is required.

## Evaluation Function Check

For audit, evaluation, readiness, completion, completeness, usability, safety, stability, coverage, correctness, or status-classification tasks, treat the rubric as requirement meaning.

Evaluation conditions include terms such as:

```text
闭环, 完成, 可用, 通过, 达标, 就绪, 用户视角, 质量好, 稳定, 安全, 合理, 充分, 覆盖, 一致, 正确, 可交付, 生产可用, 验收通过
```

Do not treat these as self-explanatory. Requirements analysis must identify the error function:

- status meanings or pass/fail categories;
- evidence levels or evidence strength;
- the minimum evidence needed for the strongest positive status;
- downgrade rules for partial, weak, missing, stale, or indirect evidence;
- handling for external credentials, production-only dependencies, third-party services, or currently unobservable behavior;
- whether confidence or evidence grade must be reported.

For rubric-only analysis, ask a short set of high-value questions focused on the evaluation function. If the user asks to proceed by default, use a conservative rubric:

```text
Strongest positive status requires direct workflow evidence or a successfully run runtime check.
Partial status means work products or unrun evidence checks exist, but direct path evidence is missing.
Negative status means only placeholders/plans exist, or no usable entrypoint exists.
Unknown/unverifiable status means external credentials, production-only environment, third-party service, or current environment prevents observation.
```

## How We Know The User's Purpose Was Met

When a task exists to realize a human purpose, evidence must be selected and
interpreted by how well it observes purpose realization, not by how easy it is
to execute.

Requirements analysis must identify:

- Human purpose: what the human wants to change or understand;
- Beneficiary / observer: who can observe whether the purpose is realized;
- Purpose-realizing outcome: the observable change when the purpose is realized;
- Feedback needed: evidence that can judge purpose realization;
- Internal checks role: what internal checks can and cannot prove;
- Sufficient evidence level: `internal`, `integration`, `purpose-limit`, or `operational`;
- If feedback unavailable: honest status and the smallest next observation.

Internal evidence checks may support progress, diagnosis, and risk reduction, but they
must not be treated as purpose-achievement evidence unless the human purpose
itself is internal-state correctness.

## Where The Result Must Show Up

When a task changes or realizes intended result across a controlled object,
requirements analysis must identify where that intended result must appear and how
old behavior will be checked.

Requirements analysis must define:

- Intended result: the state or meaning change to realize;
- Required result places: the behavior, interface, record, report, policy,
  compatibility point, or other place that must carry the intended result;
- Required action: change, inspect, preserve, exclude, or discover;
- Old behavior check: how old state, unknown places, exclusions,
  preserved behavior, and remaining mismatches will be accounted for;
- Result placement status: `adequate`, `partial`, `missing`,
  `unavailable`, or `not applicable with justification`.

result-placement is distinct from How We Know The User Purpose Was Met.
Result-placement calibrates intended-result claims. User-purpose evidence
calibrates whether the human purpose was met.

## Design Check Limit

This skill identifies whether design check is required. It does not resolve it.

Mark `design check: required` when:

- multiple reasonable solution structures exist;
- controlled objects, actors, roles, or relationships are not explicit enough for goal writing;
- system/process/organizational limits are unclear;
- information flow, state flow, evidence flow, or decision flow is unclear;
- interfaces, contracts, procedures, reports, events, or user interactions are unclear;
- a new abstraction must be introduced;
- an old concept must be replaced without letting old realization details define the requirement;
- several subsystems or roles must coordinate around one model;
- runtime execution would otherwise invent objects, limits, evidence checks, or flow.

When design check is required, record the missing solution-model questions. Do not answer those questions inside the requirements analysis unless they are already confirmed human meaning.

For `ordinary_direct_work`, `bounded_runtime`, or manual downstream chains, recommend `$designing-cybernetic-solutions` before goal writing when design is required.

For `controlled_run` JSON pre-goal work, pass design check to `$orchestrating-cybernetic-pregoal` and state that the orchestrator must invoke or request `$designing-cybernetic-solutions` before goal writing. Do not output a standalone `$designing-cybernetic-solutions` command as a separate pre-orchestration next step.

## Process

1. Inspect just enough context to avoid generic questions.
2. Restate the human purpose in task language.
3. Extract confirmed requirement meaning, terms, objects, limits, constraints, and non-goals.
4. Build a requirements control map: objective, controlled object, candidate evidence checks, actuators, constraints, disturbances, stop conditions.
5. If the task is evaluative, identify the rubric/error function and classify missing rubric elements as decisions.
6. Identify how we know the user's purpose was met and whether internal checks are sufficient or only supporting evidence.
7. Identify where the result must show up when intended-result realization spans places.
8. Identify output-contract needs and whether a safe default is sufficient.
9. For `controlled_run` JSON pre-goal work, build or update the What the User Approved compact control commitment.
10. If the commitment includes How this should be answered or What is not enough, record the plain-language requirement in `requirements.control.json` and leave execution-shape synthesis to design; do not map it to a predefined internal category.
11. Identify required checks: Meaning, Rubric, Output Contract, Design, Goal, Execution Plan, Review, Risk.
12. Classify uncertainty as blocking human decision, safe default assumption, or deferred design/planning/execution detail.
13. Ask 3-7 high-value questions, preferably no more than 5.
14. Create or update `requirements.control.json`.
15. If the human answers, update `Confirmed Requirement Decisions`, `Requirements Analysis Status`, and the What the User Approved record without treating answers as approval.
16. Do not create a solution design, goal, plan, review, runtime `/goal`, or target-work artifacts.
17. If analysis is complete and the brief path deterministically identifies a date/slug, output the approval request or queue-friendly next commands as described below.

## Queue-Friendly Next Commands

When requirements analysis is complete, choose the next command from the intended workflow.

If requirements analysis is complete but What the User Approved is not Approved for `controlled_run` JSON pre-goal work, do not output the orchestration command or predicted `/goal`.

Instead, output only the compact approval request:

```text
What the User Approved is Pending. Please approve or revise the compact control commitment before orchestration.
```

For `controlled_run` JSON pre-goal work, when `What the User Approved: Approved` is recorded and the run directory is deterministic, output:

1. A pre-goal orchestration command using the concrete run directory.
2. The predicted `runtime.control.json` path and pointer-only `/goal` shape for the same slug.

When available, generate both with:

```bash
python3 .agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py \
  --run-dir docs/cybernetics/runs/YYYY-MM-DD-<slug>
```

Use the script output instead of hand-writing predicted runtime commands when the script supports JSON run directories. The script checks `Requirements Analysis Status: Complete`, `What the User Approved: Approved`, required answer-path data, deterministic path shape, design check, and same-slug control paths.

If `predict_pregoal_handoff.py` blocks on `information_sufficiency_check`,
schema version, missing evidence, or an unapproved counterexample review, do
not hand-write an orchestration command. Run `requirements_information_loop.py`
and follow its next action.

If `design check: required`, still output the predicted runtime contract path and pointer-only `/goal` shape. State that `$orchestrating-cybernetic-pregoal` must invoke or request `$designing-cybernetic-solutions` before goal writing, and make the predicted downstream artifact paths include the expected solution design path. design check dispatch note must not replace the predicted pointer-only `/goal`. Do not output `$designing-cybernetic-solutions` as a standalone command before orchestration for `controlled_run` JSON pre-goal work.

The predicted pointer-only `/goal` is not the final approved runtime command. Label it as predicted or queue-friendly, and make it point to `runtime.control.json` that the pre-goal compiler must create after downstream artifacts are approved.

Derive expected paths from:

```text
docs/cybernetics/runs/YYYY-MM-DD-<slug>/
```

Use that run directory for:

```text
requirements.control.json
design.control.json
goal.control.json
plan.control.json
review.control.json
runtime.control.json
progress.jsonl
runtime-status.json
final-report.json
evidence/
```

The predicted pointer-only `/goal` shape must include this precondition:

```text
If any referenced artifact is missing, not approved, or inconsistent, stop and report the smallest required human decision.
```

Predicted commands and handoff prompts are response-only. Do not write them into the requirements analysis artifact.

For `bounded_runtime` work with `rubric check: required`, do not output the pre-goal orchestration command by default after rubric-only analysis. Output the next bounded goal-writing command instead:

```text
$writing-cybernetic-goals 使用 docs/cybernetics/runs/YYYY-MM-DD-slug/requirements.control.json 中确认的评价口径，为这个 bounded_runtime 有界审计/评估任务创建 goal.control.json 和 runtime.control.json，并在完成后给出指向 runtime.control.json 的短 /goal，不要默认建议 execution policy。
```

## Requirements Analysis Status

The brief must include:

```text
Status: `Incomplete` or `Complete`
```

Mark `Complete` only when:

- all blocking human decisions are resolved;
- confirmed requirement decisions are recorded;
- remaining assumptions are low-risk and explicit;
- the next step can safely create solution design control JSON or goal control JSON.

For `controlled_run` JSON pre-goal work, `Complete` only means requirement meaning are sufficiently analyzed. Downstream orchestration still requires `What the User Approved: Approved`.

## Output Format

Output examples in this section are response-only. Do not write `$skill ...` commands, runtime `/goal` prompts, or conversational next-step prompts into the requirements analysis artifact.

If a brief was created or updated:

Return a compact chat summary with:

- requirements analysis path;
- requirement status;
- blocking human decisions, if any;
- default assumptions;
- required checks;
- What the User Approved status for `controlled_run` JSON pre-goal work;
- response-only next action.

If all blocking decisions are resolved for JSON pre-goal work:

If `What the User Approved` is not `Approved`, output only:

```markdown
Requirements analysis is complete, but What the User Approved is pending.

Updated requirements control JSON:
`docs/cybernetics/runs/YYYY-MM-DD-slug/requirements.control.json`

Approve or revise the compact control commitment in the brief before orchestration.
```

If `What the User Approved: Approved`, output the predictor invocation and paste its response-only queue suggestions:

````markdown
Requirements analysis is complete.

Updated requirements control JSON:
`docs/cybernetics/runs/YYYY-MM-DD-slug/requirements.control.json`

Generated queue-friendly handoff:

```bash
python3 .agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py \
  --run-dir docs/cybernetics/runs/YYYY-MM-DD-slug
```
````

For `bounded_runtime` work with `rubric check: required`, summarize the confirmed rubric and output the bounded goal-writing handoff described in `Queue-Friendly Next Commands`.

## Validation Checklist

- [ ] Requirement meaning are separated from solution design and execution-policy writing.
- [ ] Evaluation conditions are treated as rubric/error-function meaning.
- [ ] Evaluation tasks define or ask for status meanings, evidence strength, strongest-positive threshold, downgrade rules, and external/unobservable handling.
- [ ] design check is recorded as required, satisfied, or not applicable when solution structure matters.
- [ ] The response did not downscope because execution is hard.
- [ ] Uncertainty is classified into blocking decisions, default assumptions, deferred design, and deferred planning/execution.
- [ ] Obvious defaults are not asked as blocking questions.
- [ ] There are no more than 7 questions.
- [ ] The brief includes `Requirements Analysis Status`.
- [ ] `controlled_run` JSON pre-goal work includes `What the User Approved`.
- [ ] If How this should be answered or What is not enough is recorded, `requirements.control.json` records the plain-language requirement without internal classification keys.
- [ ] Human answers to clarification questions are not treated as approval.
- [ ] Any required `information_sufficiency_check` uses schema_version 1.2.0,
      has run-local evidence, and passed independent counterexample review
      before handoff.
- [ ] Information collection was completed inside requirements analysis, or
      the artifact is explicitly `needs_information_gathering`,
      `needs_user_input`, `needs_counterexample_review`,
      `needs_requirements_revision`, or `blocked` and no handoff was output.
- [ ] Missing or weak information facts were shown to the user as
      design-blocking facts, not hidden in approved JSON.
- [ ] If What the User Approved is not `Approved`, the response asks for approval or revision and does not output the orchestration command or predicted `/goal`.
- [ ] No solution design, goal, plan, review, or approved runtime `/goal` was created.
- [ ] `bounded_runtime` work with `rubric check: required` routes to `$writing-cybernetic-goals`, not JSON pre-goal orchestration by default.
- [ ] When the predictor script is available, controlled-run queue-friendly commands are generated with `.agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py`.
- [ ] Any predicted queue-friendly `/goal` is clearly labeled as predicted and includes the missing/not-approved/inconsistent artifact precondition.
- [ ] For `controlled_run` JSON pre-goal work, `design check: required` is passed to `$orchestrating-cybernetic-pregoal`; requirements analysis does not output standalone `$designing-cybernetic-solutions` before orchestration.
