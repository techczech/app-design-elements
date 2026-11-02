# Built-in agent skill (element 19)

Owner rule, 2026-10-30: every app with a CLI ships its agent skill inside the app. The person is never asked to find or install a skill by hand. The app offers it to each agent it finds, and every app update brings the matching skill. The same skill is also available separately (owner, 2026-10-30: "ship these and make them available separately and package as well").

## What ships

- Home: `resources/agent-skill/<app>/` in the app repo, packed with `extraResources`. This is the one source; never hand-edit a copy elsewhere.
- Contents: `SKILL.md` plus `references/`. `references/commands.md` is generated at build from the verb inventory (element 11), so the skill cannot drift from the CLI.
- Build stamps `metadata.app-version` into `SKILL.md`. Skill and app version are always equal.
- Works on a stranger's machine: no absolute paths, no private stores, no owner-only tools, no internal handlers. Owner-only additions live in a separate skill under another name.
- Skill and CLI are one install. Connecting an agent also installs the CLI on the path, using the existing marker-guarded installer; the person never meets them as two steps.

## Available separately

- Every release also publishes the skill on its own, for agents the app cannot reach and for people who do not install the app. Same content, same version.
- Release step: copy the app's skill into the skills repo as a generated copy, with `PROVENANCE.md` naming the app, version and commit; then `tools/publish.py --push`. No release is finished until the published version equals the app version.
- A separately installed copy carries `metadata.app` and `metadata.app-version` but no marker. Settings shows it as "installed separately, version N". Plain folder: offer Replace. Symlink: never touch; it updates from the skills repo.

## Agent features must update the skill

Owner rule, 2026-10-30: any new feature exposed to agents must update the skill.

- A verb, CLI command or flag added, changed or removed is not finished until the skill describes it. This is part of the feature, in the same change, not a release chore.
- Hand-written `SKILL.md` or `references/` name every agent-exposed verb, excluding the generated `commands.md`. A verb left out on purpose is listed in `resources/agent-skill/not-in-skill.txt` with a reason.
- Test, in the normal suite: compare the verb inventory with the hand-written skill; fail naming each missing or stale verb. The failure blocks landing, so generating `commands.md` alone does not pass.
- The verb table in every feature design (element 11) gains a line: what the skill will say. A PR review reads the skill change with the code.

## Agents and folders

| Agent | Found by | Skill folder |
|---|---|---|
| Claude Code | `claude` binary, or the config folder | `$CLAUDE_CONFIG_DIR/skills`, else `~/.claude/skills` |
| Codex | `codex` binary, Codex app, or `~/.codex` | `~/.agents/skills` |
| Gemini CLI | `gemini` binary | `~/.gemini/skills`; skip if it already reads the `~/.agents/skills` copy |
| Antigravity | app in `/Applications` | `~/.gemini/antigravity/skills` |
| T3 Code | app in `/Applications` | none of its own: it runs Claude Code and Codex, so name it in the offer and connect those |

- Agent folders move. Keep this table as data in one module, and re-check it against each agent's docs at every release.
- A GUI app gets a thin `PATH`. Check `/opt/homebrew/bin`, `/usr/local/bin`, `~/.local/bin` as well.
- Resolve real paths and write each real folder once: two agents, or a symlinked config folder, can share one.

## The offer

- First run: one step in onboarding (element 12). Later: a Settings row, "Give your agents skills to use <App>", always present.
- List only agents found, one line each with a tick box, all ticked. If none are found, skip the step; Settings says none were found.
- Owner's wording, 2026-10-30. Title: "Give your agents skills to use <App>". Text: "This will install a skill that tells your agent how to do things with <App>. You will be able to ask your agent to <features the skill enables>." The feature list is per app, in the person's terms. Buttons: Install skill, Not now.
- Folder names and paths stay out of the main text; a "What this does" disclosure names the folders it will write.
- Not now is final for that agent. An agent found later gets one offer, once.
- Settings shows each agent: installed at version N, not installed, installed separately, or kept with a reason. It offers Install and Remove.

## Writes (write path: full review cycle)

- No file lock: Node on macOS has no lock released on crash, and three review rounds broke every recoverable one (TalkWeaver, 2026-10-31). Keep state where concurrent writers cannot clash instead.
- Marker file `.app-skill.json` in the installed folder: app id, version, hash of each file. The app owns a folder only if the marker is present and matches.
- Write to a temporary folder beside the target, then rename. Write nothing outside the skill's own folder; create the agent's `skills` folder only when that agent was found.
- Never write through a symlink. A symlink, or a folder without the marker, is someone else's: leave it, show "already has its own version".
- A file edited since install (hash mismatch): keep it, show "you have changed this copy", offer Replace.
- Remove deletes only a folder the app owns, unedited. It leaves the agent's `skills` folder.
- A store or sandboxed copy that cannot write shows the skill's location and a Copy button.
- Rename the target aside first, then re-inspect what actually moved (marker, hashes, no link, version) before deleting it; if it is not what was allowed, put it back and report kept. Confirm the parent is the same real directory (device and inode) before any path-based delete; if not, delete nothing and name the leftover.
- A replacing write refuses an absent target; only an install creates. A newer copy is never overwritten except by Replace in Settings, including when a newer copy lands mid-write.
- Commands use a no-overwrite hard link, never a replacing rename.
- State in its own folder under user data: consent in `agents/<id>.json`, written only by the person's actions; results in `agents/<id>.result.json`, the only agent file refresh writes; `app.json` for onboarded and last version; `history.jsonl`, one complete line per append. Files replaced by temp then rename. Unknown ids never reach a path. Corrupt reads as absent. Status reads truth from disk. A refused or failed write is a state in Settings, never a startup failure.

## Refresh on update

- At launch, when the running version differs from the stored one, rewrite every folder the person installed, without asking. Never add an agent they did not choose.
- A lower version never overwrites a higher one, so a preview and a release can share a machine. Replace in Settings overrides this.
- Update notices (element 17) still only tell and link; the refresh is what runs after the new version first opens. What's new mentions it only if the agent gained something the person would notice.

## Agent route

`<app> agent status|install|remove [--agent <id>] --json`, same module as the UI, same history file. `status` lists found agents, versions and states. No settings bypass: `install` from the CLI covers only agents named in the call.

## Tests

Reference implementation: TalkWeaver `src/main/agent-skill/`, portable to any Electron app. Disposable `HOME`: first connect; refresh after a version change; lower version refused; symlinked folder untouched; unmarked folder untouched; edited file kept; remove leaves everything else; two agents sharing one real folder written once; read-only folder reported, app still starts. Release check: `metadata.app-version` equals the app version; the published copy has the same version; every command named in `SKILL.md` exists in the CLI; no absolute path or private store name in the packed skill.
