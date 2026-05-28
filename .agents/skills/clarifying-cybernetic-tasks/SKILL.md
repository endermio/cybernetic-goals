---
name: clarifying-cybernetic-tasks
description: 'Deprecated compatibility alias for analyzing-cybernetic-requirements. Use only for older prompts that invoke clarification terminology. Route to $analyzing-cybernetic-requirements and create requirements analysis briefs under docs/cybernetics/requirements/. Do not create solution designs, goal contracts, execution policies, control reviews, runtime /goal commands, or implementation code.'
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

The boundary is unchanged: this alias may analyze requirements, rubrics, safe defaults, blocking decisions, and gates, but it must not resolve solution design, write goals, write plans, review control structures, compile runtime `/goal`, or implement code.
