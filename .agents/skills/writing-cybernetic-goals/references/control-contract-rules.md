# Control Contract Rules

A goal contract is not a runtime command. It is a frozen statement of:

- intended result
- constraints
- evidence checks
- stop conditions
- evidence requirements

When required design is required, the goal contract is downstream of the solution design. It should preserve design invariants and boundary decisions without redoing the design or freezing tactical details as meaning.

For complex controlled work, do not let the runtime `/goal` write its own policy. The goal contract must be paired with an approved execution policy and an approved control review before execution.

## Bad runtime goal pattern

```text
/goal First write a plan, then execute it...
```

## Good runtime goal pattern

```text
/goal Execute the runtime goal contract at docs/cybernetics/runtime-goals/YYYY-MM-DD-slug.goal.md. Read it first and follow it exactly. If any referenced artifact is missing, not approved, or inconsistent, stop and report the smallest required human decision.
```

The runtime goal contract artifact references the approved requirements,
required design, goal, execution policy, and control review. The user-entered
`/goal` stays pointer-only and length-bounded.
