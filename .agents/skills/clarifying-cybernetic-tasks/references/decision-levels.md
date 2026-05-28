# Decision Levels

## Level 1: Blocking Human Decision

Ask the human. Do not proceed to solution design or final goal creation without an answer or explicit approval of defaults.

Examples:

- whether Actor A observes Object B directly or through an intermediary summary
- whether Concept X is an alias of Concept Y or an independent entity
- whether Role A can observe all groups or only authorized groups
- whether deferred/offline handling is inside scope
- whether observer-visible identifier semantics are single-format or multi-format
- whether authorization scope is local, group-level, organization-level, or hybrid

## Level 2: Default Assumption

Do not ask by default. Record the assumption and allow override.

Examples:

- partial results are surfaced with failed source markers
- multiple source results are sorted by a confirmed ordering rule
- unreachable sources are surfaced as observer-visible warnings
- existing excluded capabilities remain out of scope unless reopened

## Level 3: Deferred Design / Planning / Execution Detail

Do not ask during requirements analysis. Defer to solution design, goal writing, execution-policy writing, or execution.

Examples:

- exact timeout values
- retry count
- interface names
- sensor artifact names
- structure index names
- helper mechanism names
- evidence artifact names
