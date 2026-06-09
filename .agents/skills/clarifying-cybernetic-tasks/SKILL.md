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

Use the current official control path:

```text
docs/cybernetics/runs/<slug>/requirements.control.json
```

Do not create legacy Markdown clarification or requirements files. Historical Markdown is non-authoritative background only.

Compatibility terms:

- "clarification brief" means historical terminology for requirements analysis; official persistence is `requirements.control.json`.
- "Clarification Status" means "Requirements Analysis Status".
- "Confirmed Decisions From Human" means "Confirmed Requirement Decisions".

The limit is unchanged: this alias may analyze requirements, rubrics, safe defaults, blocking decisions, and checks, but it must not resolve solution design, write goals, write plans, review approved work chains, compile runtime `/goal`, or execute target work.
