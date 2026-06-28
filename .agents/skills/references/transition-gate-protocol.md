# Transition Gate Protocol

Use this for every control step that can approve, block, hand off, or route to
another action. A transition gate is a router, not a worker: it reports the next
required action and the agent performs that action outside the script.

Required JSON fields:

```json
{
  "gate_protocol": "transition-gate/v1",
  "gate_id": "short-stable-name",
  "ok": false,
  "next_action": "RunCounterexampleGate",
  "terminal": false,
  "rerun_required": true,
  "approval_allowed": false,
  "handoff_allowed": false,
  "may_ask_user": false,
  "user_action_required": false,
  "agent_must_continue": true,
  "requires_independent_review": true,
  "errors": []
}
```

Rules:

- If `terminal` is false, execute `next_action` and run the same gate again.
- `terminal` does not mean success. It can also mean a wait or stop state, such
  as waiting for a new amendment proposal or human decision. Do not rerun the
  same gate until the missing external artifact or decision exists.
- If `approval_allowed` is false, do not ask the user to approve that stage.
- If `handoff_allowed` is false, do not move to the next control stage.
- If `may_ask_user` is false, do not ask the user to authorize internal review,
  safe read-only collection, repair, or other agent-owned work.
- If `agent_must_continue` is true, execute `next_action` in the current turn
  and run the same gate again. Do not stop with a status report unless the
  action reaches `AskUserForInformation`, `HumanApprovalRequired`, or another
  terminal stop state.
- If `user_action_required` is true, ask only for the requested user-owned
  information, approval, or decision.
- If `requires_independent_review` is true, the next action must use an
  independent reviewer; self-review is not enough.
- Validators and schema checks are structural gates. Counterexample review is
  the quality gate.

Information sufficiency gates:

`requirements-information-sufficiency` gates run inside requirements analysis
before design, goal writing, execution policy, review, or runtime compilation.
They decide whether enough pre-design facts have been derived from the approved
source requirements and required outcomes.

| `next_action` | `terminal` | `rerun_required` | `approval_allowed` | `handoff_allowed` | `user_action_required` | `agent_must_continue` | `requires_independent_review` | Meaning |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RunInformationCounterexampleReview` | false | true | false | false | false | true | true | Start an independent reviewer to challenge whether required pre-design facts are complete. Do not ask the user to authorize this internal review. |
| `RunInformationGathering` | false | true | false | false | false | true | false | Collect safe read-only facts, such as source reads, docs, local no-side-effect probes, or existing logs. |
| `AskUserForInformation` | false | true | false | false | true | false | false | Ask only for the missing credentials, files, business decisions, external access, or probes that could affect an environment, then rerun the gate. |
| `RepairRequirementsInformationState` | false | true | false | false | false | true | false | Fix malformed or inconsistent information-sufficiency state and rerun the same gate. |
| `ReviseRequirements` | false | true | false | false | false | true | false | Newly discovered facts changed target meaning, authority, completion criteria, or forbidden actions; return to requirements semantics before approval. |
| `ReadyForUserApproval` | true | false | true | false | true | false | false | Information sufficiency is satisfied or explicitly not required, but the requirements have not yet been approved by the user. |
| `ReadyForPreGoalHandoff` | true | false | false | true | false | false | false | Information sufficiency is satisfied or explicitly not required and approved requirements may move to pre-goal handoff. |
| `RequirementsInformationBlocked` | true | false | false | false | false | false | false | A design-blocking fact cannot currently be collected inside the approved requirements-analysis authority. |
| `RunInformationSufficiencyCheck` | false | true | false | false | false | true | false | A downstream pre-goal stage encountered missing or invalid information sufficiency state; route back to the requirements information loop. |

If any design-blocking fact is `needs_counterexample_review`,
`needs_information_gathering`, `needs_user_input`,
`needs_requirements_revision`, or `blocked`, `approval_allowed` and
`handoff_allowed` must both be false.

Compatibility:

- Legacy scripts may also emit `next_allowed_action`; it must equal
  `next_action`.
- Legacy scripts may also emit `requires_user_authorization`; it must match
  `may_ask_user`.
- Scripts should emit `user_action_required` and `agent_must_continue`. If an
  older script omits them, derive them from `may_ask_user` and `terminal`;
  internal next actions still must not be reported as user authorization waits.
