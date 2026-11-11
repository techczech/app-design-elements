# Layout, visual, states and wording (elements 14–16)

## Rule one: protect the vertical space

The owner's first rule, set 2026-11-02 after repeated failures: vertical space is the scarcest thing on a screen, and the content is what earns it.

- **At most two bars at the top of any window, ever:** title or tab bar plus one toolbar. A third row of tabs, filters, breadcrumbs, banners or status lines is a defect, not a layout choice.
- **Before adding a row, combine or move:** put filters, scope and view switches into the one toolbar (segmented control, popover, menu), status into the status bar or the sidebar, explanations into `⌘K` help, rare actions into a menu. A new control finds a place in an existing bar or it does not ship.
- **No stacked notices:** one notice slot, collapsible, never pushing content down permanently; a state that persists is shown in place (a badge, a mark in the sidebar), not as a banner.
- **No resident explainer lines** above content. A sentence that has to stay on screen to make the screen usable means the screen is wrong.
- **Count it in every review:** each screen contract and each mockup states the rows above the content and the height they take; more than two fails review.

## Anti-patterns to avoid

These three checks apply to every window and mode, including Settings, tools, previews, empty states and distraction-free views. Each anti-pattern has a replacement pattern and observable acceptance criteria. Review them whenever a surface changes and at release.

| Anti-pattern | Use instead | Review failure |
|---|---|---|
| App controls occupy the native window-control area. | Reserve the platform window controls and navigation before laying out app controls. | Any overlap, obscured target or ambiguous click in any supported window state. |
| Permanent chrome takes height from content. | Keep at most two top bars and adapt their contents to available space and the current task. | A third top row, wrapped toolbar, persistent setup banner or disappearing content area. |
| Every button or menu item has its own geometry. | Use shared control sizes, alignment rules and menu columns. | Sibling icons, labels, shortcuts or chevrons shift between items or states. |

### Protect native window controls and navigation

**Avoid:** placing an exit, back, sidebar, tab or other app control at the top-left without accounting for the Mac close, minimise and full-screen buttons. Hiding a toolbar must not remove the only reserved space. Raising a z-index cannot resolve competing native and app hit targets.

**Use instead:** let the window shell own the native-control exclusion area. Prefer native title-bar layout when suitable. A custom title bar reserves the actual window-control footprint plus spacing; its dimensions must match the host window configuration. Keep window navigation beside that reserved area, in a stable position. Reserve enough room for every supported platform's controls; do not copy a Mac inset onto Windows or browser views.

- Keep the reservation outside optional toolbars and sidebars. Focus and distraction-free modes retain it while the native controls are present; place their exit control in a safe area.
- Keep interactive controls outside drag regions. Leave a usable drag area without intercepting buttons, inputs, menus or keyboard focus.
- Handle normal, maximised and full-screen states explicitly, including native controls that reappear when the pointer reaches the top. Check entering and leaving these states.
- **Acceptance:** at default and minimum supported window sizes, native controls and app navigation remain visible and independently clickable. Check pointer hover, focus mode, sidebar changes and a long document title. A browser-only screenshot cannot pass native Mac geometry.

### Protect content height with adaptive chrome

**Avoid:** adding one permanent row per feature, wrapping a crowded toolbar into another row, or showing an optional service's setup sentence throughout unrelated work. A narrow window must not become a stack of controls above a sliver of content.

**Use instead:** allocate the title/tab bar and one toolbar first. Declare which controls are always needed, needed for the current selection or task, or occasional. Adapt within those bars: shorten secondary labels, shrink a search field within a usable limit, collapse optional groups into an overflow menu, and move detailed status to a popover, sidebar or status bar. Preserve the primary task and its navigation.

- Define the collapse order per surface. Content names can truncate with a route to their full text; controls must retain accessible names and keyboard access when labels disappear.
- Keep persistent conditions as compact status marks. Show setup instructions when setup is requested, and actionable failures when they matter. A quiet state may be compact; a blocking error must remain discoverable with its recovery action.
- Contextual controls appear for a meaningful task or selection and use existing space. Keep group order stable, keep focused controls mounted or deliberately restore focus, and avoid layout movement on hover.
- Keep content able to grow and scroll independently of chrome. Do not fix the layout by shrinking text, removing hit area or placing controls over the content.
- **Acceptance:** record the number of rows and their combined height in pixels above the primary content, plus the content height left at the minimum supported window height. Check default, narrow and short windows; long names; disconnected, loading and error states; selection and focus modes. No toolbar wraps into an extra row. Content remains usable and status details remain reachable.

### Align toolbar controls and menu items systematically

**Avoid:** mixing ad hoc button heights, icon sizes, padding, baseline offsets and corner shapes among peers. A status pill floating above neighbouring controls is still an alignment defect even if each item looks acceptable alone. Tabs may have their own geometry; this is an explicit component rule.

**Use instead:** define shared tokens for toolbar height, control height, icon box, label line height, padding, inter-item gap and group gap. Build button variants from the same primitive. Align peer controls on a common centreline and their labels on a common text baseline; use optical corrections only as shared icon rules. Status marks use the same alignment frame, even where their visual treatment differs.

- Use a consistent icon slot, label slot, optional shortcut slot and chevron slot. Icon-only buttons have the same hit-area convention as labelled peers and an accessible name.
- Menus use stable columns: check/state, icon where used, label, shortcut and submenu chevron. A missing icon or shortcut leaves its column intact. Right-align shortcuts; separators and group spacing follow one rule.
- Use the command registry for names, availability and effective shortcuts across toolbars, palettes and menus. Group actions by the task they serve and keep their order stable; record domain-specific exceptions.
- **Acceptance:** inspect mixed icon-only and labelled controls, status marks, long labels, disabled and active states. In menus, compare checked and unchecked rows, rows with and without icons or shortcuts, and submenu rows. No neighbour shifts when a state mark appears. Check keyboard focus and popovers as well as the closed toolbar.

## Containers express purpose

A container establishes a meaningful relationship between content or controls. Start by naming that relationship: a navigation pane, a document, properties of the selection, a task's commands, a discrete object or a temporary decision. Then choose the lightest grouping that makes the relationship visible.

- Use alignment, spacing and a concise heading before adding a box. Use a semantic background or divider when it clarifies a real pane boundary. Distinct panes still need the contrast required by the Layout rule below; removing decorative wrappers must not erase hierarchy.
- Use a card or framed group when it represents a discrete selectable/movable object, an independent operation, or a relationship that would otherwise be unclear. A transient popover, sheet or float has its own legitimate boundary.
- Avoid a rounded shell inside the app window, a card around every sidebar section, a table inside multiple decorative wrappers, or a separate pill around every toolbar action. Do not apply a blanket ban to meaningful cards or native grouped controls.
- For each visible border, fill, shadow and wrapper, state what its boundary communicates. If removing it preserves both meaning and usable hierarchy, prefer the simpler composition. Keep content space, focus and readable state distinctions intact.
- Command groups must be visible by purpose, with core actions before adjustments where intent is broad. A group can be expressed by labelled sections or task clusters; it does not need another card or top bar. See `command-purpose-and-priority.md`.
- **Acceptance:** inspect the whole window on each supported platform. Identify its main content, navigation, command groups and optional inspector at a glance. Every enclosure has a semantic job; repeated decoration neither consumes useful content space nor hides the grouping.

## Layout

- **Application, not website:** panels, splitters, toolbars, panel-local scrolling, tool density. No hero sections or page rhythm.
- **Theme follows the system; light is the fallback.** Follow the system light/dark setting. With no stored user choice and no system signal, default to light, never dark. Offer System / Light / Dark where the surface has settings, and set `color-scheme` to the active theme. Same rule as `web-design-elements` (apps and websites match; archive sites stay light only).
- **Bounded sections:** panels separated by real contrast steps (stage → surface → row) and solid section header bars, not hairlines inside a narrow luminance band. The primary panel gets visible emphasis.
- **Two scan axes:** left→right is the reading axis (depth, may run to two lines); top→bottom is the scanning axis (short rows, strong rhythm). A scannable list is narrow enough that a row reads without a horizontal journey; never title far left and status 700px away at the right edge.
- **70/30 default** for dashboards and mixed surfaces: ~70% for what earns depth, ~30% for what needs attention only sometimes. Primary work goes where the eye should settle (left); a TOC or rail goes left because the eye leaves it for the read on the right.
- **Negative space on the left**, never a trailing void on the right.
- **Density follows the task:** reading needs a different rhythm from scanning a long table or comparing records. Preserve useful existing density, then verify empty, typical and large-data states with long labels. Check each pane's scroll ownership; do not recover content height by making text or hit areas unusably small.

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

## Web platform basics in the renderer

An Electron renderer is a web page, so the web basics apply. Rules and code live in `web-design-elements` (`references/motion-and-focus.md`, `references/safe-rendering-and-storage.md`); read them, do not copy them here.

- **Motion:** animation and JS-driven smooth scrolling run only when `prefers-reduced-motion` is not `reduce`.
- **Accessibility floor:** a visible `:focus-visible` style, `forced-colors` fallbacks where tint carries meaning, font sizes in `rem`.
- **Safe rendering:** render user-typed or imported text with `textContent`; sanitise imported HTML. In Electron an injection can reach IPC and the filesystem, so this matters more than on the web. Storage is optional and wrapped in try/catch.
