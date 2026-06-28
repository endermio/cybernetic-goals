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
- If `requires_independent_review` is true, the next action must use an
  independent reviewer; self-review is not enough.
- Validators and schema checks are structural gates. Counterexample review is
  the quality gate.

Compatibility:

- Legacy scripts may also emit `next_allowed_action`; it must equal
  `next_action`.
- Legacy scripts may also emit `requires_user_authorization`; it must match
  `may_ask_user`.
