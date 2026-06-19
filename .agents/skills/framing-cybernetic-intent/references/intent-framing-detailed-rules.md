# Intent Framing Detailed Rules

Use this file only when the hot path is not enough to bind roles or decide
whether persistence is justified.

## Trigger Examples

Common pre-task signals:

- confusion: "I do not know what is wrong";
- dissatisfaction: "This workflow feels wrong";
- risk sense: "This may explode context";
- observed symptoms: "The agent keeps writing plans";
- failure experience: "Last time this did not converge";
- method preference: "Use the whole cybernetic workflow";
- process distrust: "I do not trust the current pipeline";
- completed findings: "I already finished the investigation; turn these
  findings into a repair plan";
- feasibility framing: "Use the current system as baseline, but investigate
  future implementation limits".

## Role Binding Details

Classify input into:

- Human purpose;
- Method preference;
- Source material;
- Declared current state;
- Requested transformation;
- Primary object;
- Reference object;
- Non-goals;
- Uncertainty to reduce.

Ask one concise role-binding question only when roles conflict or the primary
object is ambiguous, for example:

```text
Do you want these findings verified, or turned into a repair/convergence task?
```

```text
Does "capability limit" mean current system state, or future technical implementation limit?
```

## Default Output Shape

```text
Shared Intent Understanding
- Human situation:
- Input role binding:
  - Source material:
  - Declared current state:
  - Requested transformation:
  - Primary object:
  - Reference object:
  - Method preference:
  - Non-goals:
- Apparent purpose:
- Method vs purpose distinction:
- Symptoms or failure experience:
- Risk or uncertainty to reduce:
- What not to assume yet:
- Current best next move:
```

Allowed next moves include continuing intent framing, making a judgment,
designing a small experiment, performing bounded inspection, handing off to
workflow routing or requirements analysis, or stopping because purpose is not
stable.

## Persistence

Default to no file write.

Write an intent brief only when one of these is true:

- the intent frame will affect long-lived approved files;
- the same unresolved intent is likely to recur;
- the user asks to record the framing;
- future routing or requirements analysis needs a stable record of shared
  intent.

When persistence is justified, use
`docs/cybernetics/intents/YYYY-MM-DD-<slug>.md` and
`assets/intent-frame-template.md`.
