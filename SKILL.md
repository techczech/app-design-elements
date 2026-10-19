---
name: app-design-elements
description: "The shared elements every desktop app in this estate carries: command registry, palette, keyboard, macOS menu bar, settings, agent access, onboarding, help, layout and wording rules — one unified approach across apps. Use before designing, building, reviewing or retrofitting any app surface, and as the checklist at every release."
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
| 1 | Command registry | Every command: id, name in the user's words, default chord or none, availability, run function. A keydown handler that is not a registered command is a defect. | `references/commands-and-keyboard.md` |
| 2 | Command palette `⌘⇧P` | The complete command surface, each command showing its current chord; `⌘⇧,` rebinds the highlighted command in place. | same |
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
| 14 | Layout and visual | Application, not website; light is the identity, dark an option; bounded sections; scan axes and 70/30; negative space left; real icons; designed buttons; searchable, sortable lists. | `references/layout-and-visual.md` |
| 15 | States and errors | Empty, loading, refused, mid-operation, finished and error states are designed; errors are human-readable with a recovery action. | same |
| 16 | Wording | Plain literal sentences: what you do and what you get; one spelling convention per app; no internal jargon or ids as chrome. | same |

## How to use it

- **New app:** every element from the first release. Elements 1–7, 9, 10, 11 (content verbs) and 14–16 are unconditional. 8 depends on the journeys. 12–13 apply when the app has a first run.
- **Design round:** each direction is drawn inside this frame. A direction that moves Settings into a sheet, invents a different palette chord or drops the menu bar is out of bounds unless the owner reopens the rule.
- **Existing app:** adopt an element fully the next time its surface is being worked on (no partial adoption, no silent drift). The owner may order a retrofit sweep; see `references/local.md` for status per app.
- **Release check:** walk the table. Record each element as met, not applicable (with reason) or failing. A failing unconditional element blocks "done".

## Tests every app carries

1. Every reserved chord resolves to its surface or is unbound.
2. Every cheat-sheet row and every menu item shows its command's effective chord.
3. Every command is in the palette, in the bindable set, and in the menu bar or `noMenu` with a reason.
4. Zero chord collisions.
5. Every settings key in the schema appears in the window, is found by search, resets to its default, and writes a changelog entry; the command-line path writes the same entry.
6. Every content command maps to a verb.
