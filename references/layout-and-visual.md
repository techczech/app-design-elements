# Layout, visual, states and wording (elements 14–16)

## Layout

- **Application, not website:** panels, splitters, toolbars, panel-local scrolling, tool density. No hero sections or page rhythm.
- **Light is the identity; dark is a settings option.**
- **Bounded sections:** panels separated by real contrast steps (stage → surface → row) and solid section header bars, not hairlines inside a narrow luminance band. The primary panel gets visible emphasis.
- **Two scan axes:** left→right is the reading axis (depth, may run to two lines); top→bottom is the scanning axis (short rows, strong rhythm). A scannable list is narrow enough that a row reads without a horizontal journey; never title far left and status 700px away at the right edge.
- **70/30 default** for dashboards and mixed surfaces: ~70% for what earns depth, ~30% for what needs attention only sometimes. Primary work goes where the eye should settle (left); a TOC or rail goes left because the eye leaves it for the read on the right.
- **Negative space on the left**, never a trailing void on the right.

## Controls

- Real icons from an established set (lucide), never letters or model-drawn glyphs.
- Buttons are designed controls: icon + label at proper scale and hierarchy.
- Lists are searchable and sortable; trees and outlines collapsible; inputs carry their affordances (search glyph, clear button).
- No duplicated information on one surface.

## States and errors

- Every surface is designed in each state it can be in: present, empty, loading, refused, mid-operation, finished, error — including the state where the thing is absent.
- Errors are human-readable with a recovery action; never raw exception text, model ids or config values as chrome.

## Wording

- Plain literal sentences with concrete nouns and verbs: what you do and what you get. No slogan contrasts ("not A but B", "X is Y; here Z is W"), no punchy fragments. Comparisons with other products are fine when they state facts about both.
- One spelling convention per app, applied everywhere.
- Command names are the user's words for the task, not the subsystem's name.

## Design rounds

- Multi-option rounds carry a large identity badge (letter in a green rectangle, top-left) so options can be named when opened out of order; confirm a pick by name as well as letter.
