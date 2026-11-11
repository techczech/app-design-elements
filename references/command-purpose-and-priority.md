---
title: Visible command purpose groups and core-first discovery
created: 2026-11-03
provenance: Owner request for every command to have a visible purpose group and core versus supplementary priority; read-aloud example
---

# Visible command purpose groups and core-first discovery

## Rule

Every registered command has a user-facing purpose group and a role within that group: **core** or **supplementary**. A purpose names what the person is trying to do, such as Read aloud, Navigate a document, Format text or Share a document. A subsystem name or an unstructured Other group is not an adequate purpose.

A group must be visible where commands are discovered. The palette shows named group headings in both browse and search results; menus use meaningful submenus or labelled sections; toolbars show coherent task clusters through placement, spacing and appropriate labels. The same purpose is recognisable across surfaces, without forcing identical layouts or an extra toolbar row.

The registry is the source of truth. Group identity/label/order, core/supplementary role, within-role order and search aliases are maintained with command metadata, alongside availability and effective platform shortcuts. These are semantic requirements; existing schema field names can be reused. Do not keep an independent grouping or priority table in each UI. Give each command one canonical purpose; secondary search aliases can connect it to other user vocabulary.

## Primary task before adjustments

Core commands start, continue, pause, finish or otherwise perform the group's main task. Supplementary commands adjust or navigate that task. Define the roles deliberately per group; do not label everything core to avoid making a decision. Actions such as Stop may be core when a task is active.

For a broad query naming a purpose, show its relevant core commands before supplementary commands. Alphabetical order, registration order, recency or fuzzy-score accidents must not put an adjustment ahead of starting the task. Recency may order otherwise comparable commands within a role; it does not silently redefine that role.

### Read-aloud example

| Context/query | Expected visible group and order |
|---|---|
| Idle; `read aloud` | Read aloud: **Start reading aloud** first; then supplementary actions such as Skip forward and Increase reading speed, with honest availability. |
| Reading; `read aloud` | Read aloud: applicable core actions such as **Pause reading aloud** and **Stop reading aloud** first; then supplementary navigation/speed actions. |
| Paused; `read aloud` | Read aloud: **Resume reading aloud** and applicable Stop action before adjustments. |
| Explicit `increase reading speed` | The directly requested speed action is the leading actionable match within its visible Read aloud group; a generic Start action must not displace it. |
| Explicit `skip forward` | The requested Skip forward command is easy to reach. If unavailable while idle, explain why and do not substitute a different action on Enter. |

Names are examples, not a command to rename established app commands. Broad purpose intent and a specific action intent are different: first honour a specific requested action; for broad/equivalent matches prefer core actions. Group relevance orders groups; core/supplementary role and stable order arrange comparable matches within them. Preserve the useful matched supplementary results rather than hiding them.

## Discovery, state and keyboard behaviour

- Show clear purpose headings; do not require users to infer a group from repeated prefixes. Headings have accessible labels and are not selectable commands.
- Keep groups and within-group order stable while the query and task state are unchanged. Preserve the highlighted command by identity when availability updates. Do not move focus onto another command because a result re-sorts.
- The first actionable broad-purpose result should perform the main task for the current state. Unavailable commands remain discoverable with a reason, and Enter must never execute them or silently execute a fallback.
- Keep destructive or irreversible actions behind their established confirmation. Being core does not make an unrelated broad query permission to select a dangerous default.
- Supplementary commands retain search, keyboard and menu access. Search aliases include the group's purpose so someone can find an adjustment without knowing its exact implementation name.
- Palette headings may need a taller popover, but they do not create another permanent row above app content. Long groups scroll within the palette. Toolbar grouping stays inside the existing height budget.
- Apply the same semantics on Mac and Windows; show each platform's effective shortcut and normal keyboard behaviour.

## Review and implementation acceptance

1. Every registry command resolves to a named purpose and an intentional core/supplementary role. No orphaned commands or silent catch-all bucket.
2. Browse and broad-purpose search visibly group results; Read aloud puts the applicable primary task before skip and speed adjustments.
3. Specific speed/skip searches return the intended command promptly without a generic core command winning solely through priority.
4. Idle, active, paused, unavailable and no-results states preserve truthful availability and safe Enter behaviour.
5. Keyboard movement skips headings, keeps the highlighted command stable and announces purpose/context accessibly. Effective shortcuts match menus and the cheat sheet on both platforms.
6. Menu and toolbar representations use the registry semantics without adding permanent rows or hiding supplementary commands from all discovery paths.

Verify ranking with representative intent/state scenarios and real palette keyboard behaviour when implemented. Metadata-only tests do not establish that people can see the groups. This reference defines the shared pattern; it does not assert that existing apps or shared packages already implement it.
