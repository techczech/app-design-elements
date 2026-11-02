# Update notices (element 17)

Status: locked 2026-10-20 on the first app to adopt it (worked example below). Applies to every app that people other than its developer install. An app used only by its developer, rebuilt from source, records the element as not applicable with that reason.

## What it is

The app tells its users that a newer version exists, links them to the download, and after an update shows what changed. It does not download or install anything itself.

## Decided

- **Tell and link; do not install.** The app reads a small release feed, compares versions on the computer and, when a newer version exists, offers a link to the download page in the browser. The user installs as they did the first time. Installing inside the app (electron-updater, Sparkle, Tauri's updater) is out of scope until an app's installers are signed on every platform it ships, and then needs its own decision: an unsigned installer fetched by the app is checked only against a hash published beside it.
- **On by default, once a day.** A setting `updates.checkForNewVersions` (toggle, default on) in a Settings section named **About and updates**, which also shows the running build's version and where the copy came from. The first check runs a couple of minutes after launch, not during start-up, then every 24 hours while the app runs; a launch within 24 hours of the last successful check does not check.
- **Check for Updates… command.** A registry command, in the palette, in the macOS app menu under About (the standard place), in Help on Windows and Linux, and as a button beside the switch in Settings. No default chord; rebindable. It always checks, even with daily checking off. Its answers, each drawn:
  - **Up to date:** "You have the newest version." with the version and when it was checked.
  - **A new version:** "<App> <version> is available." with Download from <site> and What's new in <version>. A deliberate check shows a skipped version too, with Stop skipping.
  - **Could not check:** "Could not check for updates." with the reason in plain words (site unreachable; answered with something other than a version list), the last successful check and Try again.
  - **Store copy:** "Updates come from the <store>." with Open in <store>.
  From the menu or palette the answer is a short note in the main window; from Settings it shows in the card.
- **The automatic notice is quiet.** A mark in the status bar beside the version ("<version> is available"). Clicking it shows the version, a few lines about it, and **Download from <site>**, **Not now** (hidden until the next daily check) and **Skip this version** (that exact version is never marked again; a later one is). An automatic check never opens a modal, toast, badge or sound, and a failed automatic check shows nothing outside Settings.
- **What's new after an update: a status-bar mark only.** From the first launch of a version newer than the last one run on this computer, the status bar reads "Updated to <version> · What's new". Clicking it opens the notes. Nothing opens by itself. The mark goes when clicked or after seven days of use. Not shown on a first install or after a downgrade. The notes ship inside the app (no network) and are also in Help › What's new in <App> and the palette.
- **Never interrupt the main use.** Where the app has a mode in which a notice would intrude (presenting, recording, a live session, a full-screen task), no check runs and nothing is shown while it lasts; a check that falls due waits until it ends.
- **Store rule.** A copy installed from an app store (Microsoft Store, Mac App Store) is updated by the store, and store policies bar an app from offering its own updates. That copy makes no request to the feed at all, has no daily setting and no mark, and its About section says the store installs new versions. Check for Updates… stays and gives the store answer. What's new still works.
- **Previews hear public versions only.** A pre-release build (`1.4.0-preview.3`) reads the same public feed. In semantic-version order it is older than `1.4.0`, so it is told when the real release ships. There is no preview channel.
- **Development runs never check** (unpackaged builds).

## What a check sends (privacy)

- One GET to the feed address. No version, no identifier, no query string, no cookies (a session with no storage), and a fixed User-Agent of the app's name: Electron's default User-Agent carries the app version, so it is replaced.
- The comparison happens on the computer.
- The feed host sees the computer's internet address, as any website would. Settings says exactly this, in plain words, under the switch: what is read, what is sent, and that the site sees the address.
- Use the system proxy; time out after about 10 seconds; read at most a small fixed size.

## The release feed contract

Each app publishes one static file on its own website, written at release time, for example `https://<site>/updates.json`. Not the GitHub releases API: unauthenticated calls are limited to 60 an hour per IP address, which fails everyone behind one university or company address, and the release body is not written for the app.

```json
{
  "schema": 1,
  "latest": {
    "version": "1.4.0",
    "released": "2026-11-12",
    "summary": ["One plain sentence.", "Another.", "A third."],
    "notes": "https://<site>/whats-new#1.4.0",
    "download": {
      "mac": "https://<site>/download#mac",
      "windows": "https://<site>/download#windows"
    }
  }
}
```

- **Validation, all or nothing:** `schema` is 1; `version` is a release number without a pre-release part; `released` is a date; `summary` is one to three plain-text lines of at most 120 characters, shown as text, never HTML or Markdown; every link starts with the app's own `https://<site>/`. Anything else is rejected whole and reported only in Settings ("answered, but not with a version list"), which also covers a captive login page answering instead.
- **State** (app state, not settings): last successful check, last result, skipped version, snoozed-until, last version run on this computer. An app adopting this after earlier releases treats an existing configuration with no "last version run" as an update, so its first What's new is not lost.
- **Release order:** publish the release and its downloads first, then update the feed, so Download never leads nowhere. A check script compares the live feed with the latest published release and fails on a mismatch or an off-site link; run it as the last release step. A build check refuses a release whose What's new notes file (one short file per version, shipped in the app) is missing.

## Tests

1. The feed validator rejects each malformed case (wrong schema, pre-release version, HTML in summary, off-site link, oversize body, non-JSON) and accepts the example.
2. Version comparison: newer, equal, older, skipped, snoozed, pre-release running against its own release.
3. No request in a store copy, an unpackaged run, or while the app's protected mode is active; the postponed check runs when it ends.
4. Check for Updates… produces each of its four answers.
5. The request carries no version, cookie or query string, and the fixed User-Agent.
6. What's new mark: shown after an update, not after a first install or a downgrade; gone when clicked.

## Worked example: TalkWeaver (locked 2026-10-20)

Feed `https://talkweaver.app/updates.json`; Settings › About and updates added at the foot of the section list; status-bar mark beside `v0.41.0`; Check for Updates… in the TalkWeaver app menu, Help on Windows, the palette and Settings; no check while a presenter window, audience window, live session or recording is open; the Microsoft Store copy (`process.windowsStore`) never contacts the site; notes in `resources/whats-new/<version>.md`. Eleven drawn frames and seven journeys: `docs/design/2026-10-20-update-notices/` in the TalkWeaver repository; spec `docs/plans/update-notices/spec-update-notices.md`.
