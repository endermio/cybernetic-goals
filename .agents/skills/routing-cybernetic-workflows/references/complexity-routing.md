# Control Entry Reference

Route by unresolved control decisions, not by scary keywords or process weight.

## Main Question

Would runtime need to invent or revise any of these?

- requirement meaning
- solution structure or design model
- goal or success criteria
- authorization or visibility meaning
- external contract meaning
- evidence checks
- execution strategy
- phase checks
- stop or completion conditions

If yes, choose `controlled_run`.

If no, choose `ordinary_direct_work` or `bounded_runtime`.

## Existing Control Structure

If approved artifacts or explicit user decisions already fix meaning and the
task is a bounded correction, do not create a new controlled run.

Examples for `bounded_runtime`:

- Fix a misleading observer display inside an already approved work chain.
- Update an evidence assertion after a confirmed observer-label change.
- Write a bounded audit when rubric and output shape are explicit.

Examples for `controlled_run`:

- Define a controlled relationship for the first time.
- Decide direct observation vs intermediary reporting.
- Create a new authorization or visibility model.
- Execute multi-subsystem work without approved requirements and strategy.

Risk examples:

- Production-impacting, irreversible, credentialed, regulated, or customer-data
  work adds `human_gate` or `live_gate`.
