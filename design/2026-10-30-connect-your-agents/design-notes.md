---
title: Connect your agents (onboarding step, Settings card, later offer)
date: 2026-10-30
status: locked, owner approved 2026-10-30 with the title and wording in references/agent-skill.md
mockup: connect-your-agents-mockup.html
spec: references/agent-skill.md (The offer, Writes, Refresh on update)
---

Seven stacked frames, light theme, Settings look from `2026-10-19-settings-locked`. Screenshots in `screenshots/frame-01.png` to `frame-07.png` (open the HTML with `#f1` to `#f7` to see one frame alone).

1. **Onboarding, three agents found.** Claude Code, Codex and Antigravity listed with ticked boxes. A grey line says T3 Code uses Claude Code and Codex and comes along with them. Buttons Connect (primary) and Not now. "What this does" is closed. The words skill, folder and path stay out of the main text.
2. **Disclosure open.** Names the three folders written and the command-line tool `talkweaver`. Says connected copies are updated with each app update and can be removed in Settings, under Agents.
3. **Finished.** Lists the connected agents, gives a sentence to try ("Ask Codex to make a ten-slide talk on how bees find flowers."), button Done.
4. **WriteFlex, one agent.** Same layout as frame 1. Only the wording changes: "Codex will be able to draft, edit and review your documents."
5. **Settings card.** Rows: Claude Code connected, version 0.42.0, Disconnect; Codex connected, Disconnect; Antigravity not connected, Connect; Gemini CLI "Already has its own version", no action; one row "You have changed this copy" with Replace.
6. **Later offer.** A mark in the status bar beside the version, opened to a small notice: "TalkWeaver found Codex. Connect it?" with Connect and Not now. Shown once per agent.
7. **None found.** Settings card with an empty state that says nothing was found and that a later install will be offered.

Assumptions:
- The folder names (`~/.claude/skills/...`, `~/.agents/skills/...`, `~/.gemini/antigravity/skills/...`) follow `references/agent-skill.md`; the builder re-checks them against each agent's docs.
- The changed-copy row names no agent in the brief; the mockup labels it "Another agent".
- The Settings pane is called "Agents", under a "Connections" group, as a stand-in for the real sidebar.
- In frames 1, 3, 4 and 6 no skill, folder or path wording appears; frame 5 uses "copy" and "version" only.
