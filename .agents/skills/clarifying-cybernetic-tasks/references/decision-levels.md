# Decision Levels

## Level 1: Blocking Human Decision

Ask the human. Do not proceed to final goal creation without an answer or explicit approval of defaults.

Examples:

- real-time pull vs local summary vs push-based reporting
- enterprise equals corp_id vs independent enterprise entity
- regulator can query all parks vs only authorized parks
- whether offline filing workflow is in scope
- whether user-visible hash concept is base58-only or dual-format
- whether permission scope is node-level, tenant-level, organization-level, or hybrid

## Level 2: Default Assumption

Do not ask by default. Record the assumption and allow override.

Examples:

- fan-out query returns partial results and marks failed nodes
- multiple node results are globally sorted by time descending
- UI shows failure badges or warnings for unreachable nodes
- existing excluded features remain out of scope unless reopened

## Level 3: Deferred Execution / Planning Detail

Do not ask during clarification. Defer to goal writing, planning, or implementation.

Examples:

- exact timeout values
- retry count
- endpoint names
- test file names
- schema index names
- helper function names
- screenshot file names
