# Agent access (element 11)

## The content-verb law

If the app can do it with content, the agent can do it. An app feature operating on content that the agent cannot operate is the same defect class as a click target without a keyboard route.

- Every content operation is a **typed, headless verb**: one implementation, the UI is one caller, the agent another.
- The command registry classifies every command: content / view / settings / chrome. Every content command maps to a verb, enforced by the app's own tests. Chrome exclusions carry a declared reason (`ui-navigation`, `presentation`, `duplicate-of`).
- **Posture floor per verb:** reversible → direct, recorded, undoable; substantive rewrite → proposal (diff, accept/reject); destructive or externally irreversible → approval plus an execution journal. The request's intent may raise the gate ("suggest…" returns a proposal), never lower it.
- Every feature design includes a verb table: verb, typed inputs, posture floor, context contribution. An agent journey is written only when the agent is a primary user of the feature.

## Settings

- Read and change through a command-line path (`<app> settings …`, `--json`), through the same store and the same changelog, marked as agent changes.
- A CLI is not a back door: it goes through the same validation and recording as the UI.

## Discoverability

The agent's operation list is generated from the registry and the verb inventory, like the palette, so an agent can discover what the app can do without reading its code.
