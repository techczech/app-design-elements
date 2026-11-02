# Layout, visual, states and wording (elements 14–16)

## Rule one: protect the vertical space

The owner's first rule, set 2026-11-02 after repeated failures: vertical space is the scarcest thing on a screen, and the content is what earns it.

- **At most two bars at the top of any window, ever:** title or tab bar plus one toolbar. A third row of tabs, filters, breadcrumbs, banners or status lines is a defect, not a layout choice.
- **Before adding a row, combine or move:** put filters, scope and view switches into the one toolbar (segmented control, popover, menu), status into the status bar or the sidebar, explanations into `⌘K` help, rare actions into a menu. A new control finds a place in an existing bar or it does not ship.
- **No stacked notices:** one notice slot, collapsible, never pushing content down permanently; a state that persists is shown in place (a badge, a mark in the sidebar), not as a banner.
- **No resident explainer lines** above content. A sentence that has to stay on screen to make the screen usable means the screen is wrong.
- **Count it in every review:** each screen contract and each mockup states the rows above the content and the height they take; more than two fails review.

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
