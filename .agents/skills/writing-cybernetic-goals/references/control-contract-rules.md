# Control Contract Rules

A goal contract is not a runtime command. It is a frozen statement of:

- target state
- constraints
- sensors
- stop conditions
- evidence requirements

When Design Gate is required, the goal contract is downstream of the solution design. It should preserve design invariants and boundary decisions without redoing the design or freezing tactical details as semantics.

For complex implementation work, do not let the runtime `/goal` write its own plan. The goal contract must be paired with an approved execution policy and an approved control review before execution.

## Bad runtime goal pattern

```text
/goal First write a plan, then implement it...
```

## Good runtime goal pattern

```text
/goal Execute the approved execution policy in [PLAN] under the control contract in [GOAL], confirmed requirements in [REQUIREMENTS], and required solution design in [DESIGN]...
```
