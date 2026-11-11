---
title: Mac and Windows desktop design and review contract
created: 2026-11-03
provenance: Owner request for Mac-first quality with Windows compatibility; inspected Impeccable, Electron, Microsoft and cross-platform skill references
---

# Mac and Windows desktop design and review

Electron ships its own Chromium, so any feature shipped in that Chromium is fine: no cross-browser fallbacks or polyfills.

## Platform contract

Declare the supported desktop platforms and the primary experience before reviewing a surface. A primary platform may receive more visual refinement, but a supported secondary platform must retain its core tasks, native window controls, readable content and keyboard access. Keep the existing framework and product identity unless a migration or redesign is explicitly requested.

Share command semantics, purpose groups, data and design tokens where appropriate. Adapt window chrome, native menus, shortcut defaults and labels, file dialogs, fonts and input behaviour to the platform. Do not copy a Mac traffic-light spacer onto Windows or draw Mac window buttons inside a Windows window. Never infer Windows acceptance from a Mac screenshot or a user-agent override.

## Minimum review on each supported platform

| Surface | macOS check | Windows check |
|---|---|---|
| Native controls | Clear the actual left-side traffic-light footprint, including focus mode and full-screen transitions. | Clear the actual caption-button area; check minimise, maximise/restore and close, restored/maximised windows and supported Snap behaviour. |
| Custom title bar | Native buttons, usable drag space and app controls have independent hit targets. | System caption controls and drag/resize regions work; interactive content is outside drag regions. Preserve system-menu access. |
| Commands and menus | Native menu roles and effective Mac shortcuts remain available. | Commands remain reachable through a Windows application menu or equivalent command surface and the palette. Shortcuts use actual Windows bindings and labels. |
| Text editing | Check native editing, selection, composition and the app's reserved chords. | Check native editing, selection, composition and Windows/AltGr collisions; do not mechanically translate every Mac modifier family. |
| Layout | Count top bars and remaining content height; check minimum sizes and long names. | Repeat with Windows fonts, scrollbar widths and display scaling, including 100%, 150% and 200% where supported. |
| Focus and states | Check keyboard traversal, disabled states, popovers, inactive windows and supported appearance/accessibility settings. | Check the same paths with visible focus, Narrator where applicable, Contrast themes and reduced motion. |
| Core tasks | Exercise the primary workflow and recovery with disposable data. | Exercise the same workflow, including native open/save and clipboard/file interactions touched by the change. |

These are checks, not a new promise that every app supports every OS feature. Record a reason for a genuinely inapplicable feature. Record unavailable runtime verification as not run, with the missing platform or host named. Source checks, rendered content checks, native interaction and packaging remain separate results. A Windows build compiling is not proof that caption controls, menus or keyboard input work.

## Implementation principles

- Prefer host-provided native title bars and controls where they meet the app's needs. Custom chrome must use the actual host geometry and keep its reservation independent of optional content.
- Electron: inspect the running version's `titleBarStyle`, `titleBarOverlay`, traffic-light placement and Window Controls Overlay support. Use supported title-bar area geometry rather than a fixed cross-platform guess. Interactive descendants must be excluded from drag regions.
- Use the command registry's effective platform binding for dispatch and all displayed shortcuts. `CommandOrControl` is useful for shared Electron defaults, but distinct Mac Control/Command families and Windows AltGr require deliberate mapping. Preserve existing user overrides and native text editing.
- Keep purpose headings, core/supplementary roles and command availability shared. The menu arrangement and shortcut typography can follow the OS.
- Use fallbacks for unsupported materials and effects. Readability, focus and state distinctions must survive their absence. Do not turn a material preference into a framework migration.

## Using Impeccable

Load app-design-elements and this contract before Impeccable on a desktop app. App work surfaces use its **Operate** mode; documentation uses **Read**. Preserve the current design on a refinement request.

Use `audit` for located technical defects, `critique` for visual and workflow judgement, and `distill` for unnecessary UI. Start with a bounded window, task or component. The upstream iOS/Android native route does not cover desktop platform acceptance. Electron renderer inspection can supply useful evidence, while native chrome still requires the real host window. On macOS Tauri, record source-only checks when a rendered detector path is unavailable.

Keep the estate's command registry, grouped-command rules, container pattern and two-top-bar rule authoritative. Follow the current harness's permission, delegation, browser and process-preservation rules. Installing this skill does not authorise hooks, a redesign, a release or an app install. Do not run an upstream self-update over a tracked skill import.

For each app, report Mac and Windows results separately: source revision/build, window and mode, dimensions/scaling, evidence type, failures and checks not run. Preserve genuine failures even if the other platform passes.

## Evidence-led desktop review

- Before suggesting changes, identify the working task paths, command names, layout density and platform behaviours to preserve. Prefer a local fix for a local defect; record a wider redesign separately when it is actually needed.
- Each finding names the affected platform/window/state, the trigger, observed evidence, user impact and the smallest useful correction. Label source inference, screenshot observation and exercised runtime behaviour separately. Missing evidence remains unknown.
- When comparing before and after, match the window, dimensions, display scaling, theme, data and interaction state. Reproduce the original trigger after a fix; a different state cannot clear the finding.
- For lists, tables and toolbars in scope, use representative empty, single-item, typical and large-data cases, plus long names, multi-selection and relevant failure/offline states. Use disposable or authorised data. Add cases because the task needs them, not to build a permanent test programme by default.
- Choose density for the actual work: reading, scanning, comparison or editing. Preserve useful content height without shrinking text or targets below comfortable use. Identify which pane scrolls and check nested scrolling only where it affects the task.

These are independently maintained review criteria. Community packs supply ideas, not authority over the app's existing design, framework, update policy or workflow.
