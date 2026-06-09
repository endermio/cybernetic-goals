---
name: clarifying-cybernetic-tasks
description: 'Use when older prompts invoke cybernetic clarification terminology; prefer analyzing-cybernetic-requirements for formed task requirements analysis.'
---

# Clarifying Cybernetic Tasks

Deprecated alias for `$analyzing-cybernetic-requirements`.

When invoked, perform the requirements-analysis workflow from:

```text
.agents/skills/analyzing-cybernetic-requirements/SKILL.md
```

Use the new artifact path:

```text
docs/cybernetics/requirements/YYYY-MM-DD-<slug>.md
```

Do not create files under `docs/cybernetics/clarifications/`.

Compatibility terms:

- "clarification brief" means "requirements analysis brief".
- "Clarification Status" means "Requirements Analysis Status".
- "Confirmed Decisions From Human" means "Confirmed Requirement Decisions".

The limit is unchanged: this alias may analyze requirements, rubrics, safe defaults, blocking decisions, and checks, but it must not resolve solution design, write goals, write plans, review approved work chains, compile runtime `/goal`, or execute target work.
