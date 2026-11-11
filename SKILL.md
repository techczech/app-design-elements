---
name: app-design-elements
description: "Use before designing, building, reviewing or retrofitting any app surface, and as the checklist at every release; the elements shared by all of Dominik's desktop apps."
---

# App Design Elements

If `references/local.md` exists, read it: it holds the estate's decision records, reference implementations and per-app adoption status, and overrides this file where they differ.

## What this is

One set of elements, built the same way in every app, so that a person who knows one app already knows how to drive the next. Commands, keys, menus, settings, help and agent access are not designed per app; each app fills the same frame with its own content.

Three properties make it a system rather than a style guide:

- **One registry, many readers.** Every command is registered once. The palette, the menu bar, the cheat sheet, the shortcut settings and the agent's operation list are all generated from that registry, so none of them can drift from the others.
- **Same gesture, same meaning, every app.** Reserved chords, menu layout and settings shape are identical across apps. Divergence is allowed only where an app's domain demands it, and is written down.
- **The agent is a user.** Anything the app can do with content, an agent can do through the same typed operations the UI calls; settings are readable and changeable by agents through the same changelog the user sees.

## The elements

| # | Element | Rule in one line | Reference |
|---|---|---|---|
| 1 | Command registry | Every command: id, name in the user's words, visible purpose group, core/supplementary role, default chord or none, availability, run function. A keydown handler that is not a registered command is a defect. | `references/commands-and-keyboard.md` |
| 2 | Command palette `⌘⇧P` | The complete command surface, visibly grouped by purpose with core actions first for broad intent, each command showing its current chord; `⌘⇧,` rebinds the highlighted command in place. | same |
| 3 | Reserved chords | `⌘⇧P` palette · `⌘⇧K` switcher · `⌘K` contextual actions · `⌘P` inspector · `⌘F`/`⌘⇧F` find/search everything · `⌘,` settings · `⌘/` cheat sheet. Never repurposed; an absent surface leaves its chord unbound. | same |
| 4 | Keyboard parity and rebinding | Every click target has a key path; every chord is rebindable; overrides are the truth. | same |
| 5 | Cheat sheet `⌘/` | Generated from the registry with effective chords; works while typing. | same |
| 6 | macOS menu bar | Generated from the registry; every command except `noMenu` repeat keys (with reason); shows effective chords; fixed frame: App (Settings…), Edit, View, app menus, Window, Help. | same |
| 7 | Contextual actions `⌘K` | What can be done to the current selection, here. Also the contextual help surface. | same |
| 8 | Switcher `⌘⇧K`, inspector `⌘P` | Only when the app's locked journeys need them. | same |
| 9 | Find and search | `⌘F` in the current document, `⌘⇧F` across everything. Default-on; omission needs a recorded reason. | same |
| 10 | Settings | Own window; one schema drives sections, search, per-setting reset, changelog; Shortcuts page; Accounts and keys encrypted; version from the running build. Present from the first release. | `references/settings.md` |
| 11 | Agent access | Content-verb law: every content operation is a typed headless verb the UI and the agent both call. Settings have a command-line read/change path through the same changelog. | `references/agent-access.md` |
| 12 | Onboarding | Temporary: a Get started button with a lifecycle that removes itself; an example project teaching commands as task chapters; a How this app works section. | `references/onboarding-and-help.md` |
| 13 | Help | After onboarding, help is contextual (`⌘K`, `⌘/`, Help menu), not a catalogue; no resident explainer copy in the interface. | same |
| 14 | Layout and visual | Protect native window controls; protect content height with adaptive chrome and at most two top bars; align toolbar controls and menu columns systematically. Application, not website; follows the system theme, light when there is no signal; bounded sections; scan axes and 70/30; negative space left; real icons; designed buttons; searchable, sortable lists. | `references/layout-and-visual.md` |
| 15 | States and errors | Empty, loading, refused, mid-operation, finished and error states are designed; errors are human-readable with a recovery action. | same |
| 16 | Wording | Plain literal sentences: what you do and what you get; one spelling convention per app; no internal jargon or ids as chrome. | same |
| 17 | Update notices | Tell and link, never install: a daily check (on by default) of a small feed on the app's site that sends nothing but the request; a status-bar mark with Download / Not now / Skip this version; Check for Updates… in the app menu, palette and Settings; What's new as a status-bar mark after an update; store copies never check; previews hear public versions only. | `references/update-notices.md` |
| 18 | App logo | A designed app icon and logo from the first release, in the estate family set by TalkWeaver and WriteFlex; never the Electron/Tauri default. Generated with Codex image generation as drawn options, picked by the owner in DTC; the pick ships as `.icns`/PNG set plus SVG/PNG master in the repo. | `design/2026-10-21-app-logos/` (theme brief) |
| 19 | Built-in agent skill | Every app with a CLI ships its skill inside the app, offers it in onboarding and Settings to each agent it finds, and refreshes installed copies after every update. The same skill is published separately at each release. Any feature exposed to agents updates the skill in the same change, enforced by a test. Skill version equals app version. | `references/agent-skill.md` |
| 20 | Surface type | Every feature states modal, float, docked panel or window before visual design: short choice is a modal; acting at the cursor is docked; a work area across documents or kept side by side is a window; a small holding place during editing is a float. | `references/surfaces.md` |
| 21 | Web platform basics in the renderer | Electron apps: motion and JS smooth scroll only when `prefers-reduced-motion` is not reduce; visible `:focus-visible`, forced-colors fallbacks, rem font sizes; user-typed or imported text via `textContent`, imported HTML sanitised. | `references/layout-and-visual.md` |

## Research (every app with documents)

Every app whose documents are talks, pieces or similar carries:
- A `research/` folder beside each document: one Markdown file per captured unit (frontmatter: title, kind, prompt, sources, created, project, by), artefacts beside it. Filed with `scout capture`.
- Palette command "Capture to research…" (sheet: title, kind, question, text prefilled from selection or clipboard) and, where the app has files, "Reveal research folder".
- The folder name `research` (any case) is reserved: never a document, category or outline; create, rename, clone and move to it are refused.
- Agent verb `research.capture` (built in TalkWeaver 0.42.0-alpha.3 and WriteFlex 0.26.0-alpha.9). Planned with the panel, not built: `research.list`, `research.whereUsed`, `research.search`.
- Research panel (locked 2026-10-20, not built): docked right panel `⌘⇧R` plus quick picker (keyboard route); insert at cursor, make slide (TalkWeaver), used-in, search scopes this talk or piece / all research / everything. TalkWeaver builds first, WriteFlex after. Design: `design/2026-10-20-research-panel/` (`design-notes.md` Lock section, `research-journeys.md`).

## How to use it

- **New app:** every element from the first release. Elements 1–7, 9, 10, 11 (content verbs), 14–16 and 20 are unconditional. 8 depends on the journeys. 12–13 apply when the app has a first run. 17 applies to every app that people other than its developer install. 18 is unconditional: ask for the logo when the app is set up (owner, 2026-10-21: "we should also ask for a logo for any new app"). 19 applies to every app with a CLI.
- **Design round:** each direction states its surface type (element 20) and is drawn inside this frame. A direction that moves Settings into a sheet, invents a different palette chord or drops the menu bar is out of bounds unless the owner reopens the rule.
- **Existing app:** adopt an element fully the next time its surface is being worked on (no partial adoption, no silent drift). The owner may order a retrofit sweep; see `references/local.md` for status per app.
- **Desktop platforms:** declare the primary and supported platforms, then apply `references/cross-platform-desktop.md`. Keep Mac and Windows verification separate; a primary-platform pass cannot stand in for the other. Load this contract before using Impeccable on desktop apps.
- **Command discovery:** apply `references/command-purpose-and-priority.md` to registry, palette, menus and toolbar groups. Every command has a visible purpose; broad-purpose search prioritises the task over its adjustments.
- **Layout review:** apply the three anti-pattern checks in `references/layout-and-visual.md` to every window and mode. Record source findings separately from native visual acceptance; include minimum-size geometry and content-height evidence.
- **Release check:** walk the table. Record each element as met, not applicable (with reason) or failing. A failing unconditional element blocks "done". For element 17, each release also checks that the version's What's new notes ship in the app, that the feed is updated only after the release is published, and that the feed check script passes.

## Tests every app carries

1. Every reserved chord resolves to its surface or is unbound.
2. Every cheat-sheet row and every menu item shows its command's effective chord.
3. Every command is in the palette, in the bindable set, and in the menu bar or `noMenu` with a reason.
4. Zero chord collisions.
5. Every settings key in the schema appears in the window, is found by search, resets to its default, and writes a changelog entry; the command-line path writes the same entry.
6. Every content command maps to a verb.
7. Update notices (element 17): the feed validator, version comparison, no request in a store copy or protected mode, every Check for Updates… answer, and the bare request; list in `references/update-notices.md`.
8. Built-in agent skill (element 19): every agent-exposed verb is described in the hand-written skill; the install, refresh and refusal cases on a disposable home folder; the release checks; list in `references/agent-skill.md`.
