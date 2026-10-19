# Settings (element 10)

Status: rules and the shared visual design are locked (2026-10-19).

## Decided

- **Every app has Settings from its first release.** Minimum: version read from the running build, a Shortcuts page covering every command, the app's real preferences.
- **Own window**, the macOS convention. Opened by `⌘,`, by App menu › Settings…, and by the palette. Not a sheet or panel over the main window. One instance; reopening focuses it.
- **One schema.** Each setting declared once: `key`, `label` (user's words), `section`, `type` (toggle, choice, text, number, path, chord, secret), `default`, validation, optional help line. The window, search, reset and changelog are generated from the schema; no hand-built form fields beside it.
- **Search** across labels, help lines and section names; results show the section they belong to.
- **Changed from default is visible** on each setting, with a per-setting Reset.
- **Settings changelog** (the Changes section): every change records old → new, when, and who (you / agent / app migration), each entry with Reset. Reset itself is recorded.
- **Shortcuts page:** every registry command, searchable, its effective chord, rebind in place, conflicts shown, reset one or all.
- **Accounts and keys:** connection status, add / replace / remove; the secret value is never displayed and never stored in a plain config file (macOS Keychain or the platform's encrypted store).
- **About / version:** the version of the running build, not a constant typed in the UI.
- **Agent path:** a command-line interface `<app> settings list | get <key> | set <key> <value> | reset <key> | changes`, with `--json`, writing through the same store and changelog. An open Settings window updates live when a setting changes from outside.
- **Moving settings between Macs:** by hand — Export settings… writes one file; Import settings… previews old → new, then applies; imported changes enter Changes attributed to the file, with Undo import. Account keys are never exported. No synced folder.
- **Storage:** one settings file in the app's user-data folder plus the changelog; the keymap overrides live in the same store, not browser storage.

## Typical sections

General · Appearance (light default, dark option) · app-specific sections · Shortcuts · Accounts and keys · Changes · About. App sections are named by what the user is doing, not by subsystem.

## Locked design (2026-10-19)

Mockup: `design/2026-10-19-settings-locked/settings-window-locked-mockup.html` (16 frames; notes in `design-notes.md` beside it). Build to it.

- **Frame:** sidebar (search; shared sections; the app's own sections under its name; Changes and About pinned at the bottom) + one section as grouped cards + a fixed right inspector, 70/30. Window about 1000×690.
- **Inspector:** nothing selected → recent changes (who, when, Reset, link to all changes). Setting selected → what it does, default, current, changed by, history of this setting, Reset, the agent command. On Changes → the selected entry's setting.
- **Agent change:** row highlighted with "Changed by <agent> just now" and a link to its Changes entry; Changes badge shows new entries.
- **Changes:** newest first, filter by setting, filters All / You / Agents / App updates / Imports; each entry old → new, who, when, Reset; reset entries are themselves listed.
- **Settings file:** card at the bottom of General (Export settings…, Import settings…) and App menu items under Settings…. Export file records app version and Mac; never account keys. Import shows a preview sheet (count, old → new, skipped settings with reason, "already match" count), one Import button, no per-row checkboxes; refused state for a wrong file. Imported entries form one batch in Changes with Undo import; each entry resets on its own.
- **Agent path additions:** `settings import <file>`, `settings undo-import --last`, `settings export <file>`.
