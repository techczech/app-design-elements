---
title: Settings window — locked candidate (A with C's inspector and B's recent changes)
date: 2026-10-19
status: locked candidate, awaiting Dominik's lock
mockup: settings-window-locked-mockup.html
screenshots: screenshots/frame-01.png … frame-16.png
source round: the earlier three-direction design round
rules: ../../references/settings.md, ../../references/layout-and-visual.md
---

# Settings window: locked candidate

Dominik picked "A, with C's inspector and B's recent changes" and, for moving settings between Macs, "Export and import a settings file by hand". This is that combination in one window.

## What came from each direction

- **From A (the frame):** the sidebar with the search field at the top. Shared sections come first under "All apps" (General, Appearance, Shortcuts, Accounts and keys), then the app's own sections under the app's name, then Changes and About pinned at the bottom. The selected section shows as grouped cards with solid header bars.
- **From C (the inspector):** a fixed right-hand column, 240 px of the 790 px to the right of the sidebar (about 70/30). For the selected setting it shows the name and where it lives, what it does, default, current value, who changed it last, the history of that one setting, "Reset to <default>", and the agent commands (`writeflex settings set <key> <value>`, `… reset <key>`) with copy buttons. Secrets show that agents can see whether a key is saved but never its value.
- **From B (recent changes):** when no setting is selected, the inspector column shows Recent changes: the last five changes, each with old → new, who (You / agent name / app update / Import) and when, a Reset on each, and "All changes (n)" at the foot. The window opens on General with nothing selected, so the opening screen always shows them.

## Where export and import sit

- **General › Settings file** card, the last card on the opening section: one row, "Move settings to another Mac", with **Export settings…** and **Import settings…** buttons.
- **App menu**, directly under Settings… ⌘,: **Export Settings…** and **Import Settings…** (frame 11).
- Export opens the macOS save sheet with `WriteFlex Settings 2026-10-19.json` in Documents. Below the fields: what is included (settings changed from default and shortcuts), and that account keys are not exported and stay in Keychain on this Mac.
- Import opens a preview sheet once a file is picked: which Mac and app version exported it, each setting that will change with this Mac's value → the file's value, one setting skipped (a folder that is not on this Mac), how many already match, and that keys are not in the file. Buttons: Cancel / Import 6 settings.
- After the import, Changes shows the batch as its own card headed "Import from WriteFlex Settings 2026-10-17.json", with **Undo import** for the whole batch in the header and Reset on each entry. Each entry is tagged "Import". The inspector shows the batch: when it was imported, which Mac exported it, counts, the skipped setting, Undo import, and the agent commands.

## Frames

| Key | Frame | File |
|---|---|---|
| 1 | Window, default (General, search focused, recent changes in the inspector) | frame-01.png |
| 2 | Search "font": three matches in two sections, one selected and inspected | frame-02.png |
| 3 | Search, no results: Search commands in Shortcuts / Clear search | frame-03.png |
| 4 | Every row type (Read aloud): toggle, choice, text, number, path, chord, secret, segmented; changed rows with Reset; validation error; disabled rows with reasons | frame-04.png |
| 5 | Row just changed by an agent (Claude Code, Checkpoint on close), link to its Changes entry, "1 new" on Changes | frame-05.png |
| 6 | Changes: grouped Today / Yesterday / Earlier, filter by who, Reset per entry, one entry that is itself a reset | frame-06.png |
| 7 | Shortcuts: search, one row capturing, one conflict with Swap / Replace / Cancel, Reset one / Reset all | frame-07.png |
| 8 | Accounts and keys: connected, not connected with a key being added (masked, saved in Keychain), problem with recovery | frame-08.png |
| 9 | About: version and build, copy, update status, Reset all settings… confirm naming the count | frame-09.png |
| 0 | Same window, TalkWeaver: Presenting, Publishing, Recording in the shared frame | frame-10.png |
| Q | App menu open: Settings… ⌘, plus Export Settings… / Import Settings… | frame-11.png |
| W | Changes, empty: "No changes yet" | frame-12.png |
| E | Export: save sheet | frame-13.png |
| R | Import: preview sheet | frame-14.png |
| T | After import: Changes with the import batch, Undo import, Reset per entry | frame-15.png |
| Y | Import, wrong file: a TalkWeaver file picked in WriteFlex | frame-16.png |

← and → step through all sixteen.

## Decisions

- Inspector as a fixed right-hand column, not a popover or a slide-in: it keeps A's sidebar and section pane unchanged, follows the 70/30 rule with the depth on the left, and never covers the row being changed.
- Recent changes go in the inspector when nothing is selected, not at the top of General: General is a shared section every app fills, and putting the list in a column that already exists keeps it on every section's opening view without pushing settings down.
- On Changes the inspector shows the selected entry's setting, not recent changes, so the same list never appears twice on one screen.
- Window drawn at 1000 × 690 rather than round 1's 860 × 600, because a third column at 860 would squeeze the setting rows below a readable width.
- Export and import live in General and in the App menu, not in About or the File menu: General is where the window opens, File is for documents, and the App menu is where macOS apps put app-wide actions next to Settings….
- The import preview has no per-setting checkboxes: every imported change can be reset on its own in Changes, which keeps the sheet to one decision.
- Settings that cannot apply on this Mac (a folder that does not exist here) are skipped and listed as skipped, rather than imported broken.
- The file name appears once, on the import batch header, and each entry carries a short "Import" tag, so the long name is not repeated six times.
- Import gets its own who colour (teal) beside You (blue), agents (purple) and app updates (grey), and its own filter in Changes.
- A wrong-file import (another app's settings) is drawn as a frame, because the states rule asks for the refused state.
- WriteFlex's own sections follow the real Settings window (Assistant, Editor, Reading Room, Read aloud, Sounds, Library, Diary, Saving & history). Account & Model is split: sign-in and keys go to the shared Accounts and keys; Model, reasoning level and Agent permissions go to the WriteFlex section Assistant.

## Assumptions

- The agent command line gains `settings import <file>` and `settings undo-import`, matching the window's Import and Undo import. The settings rules list only list / get / set / reset / changes.
- The settings file records which Mac and app version exported it, so the preview can say so.
- "Interface text size" in Appearance is not in WriteFlex today. It is there to show a search match outside Editor.
