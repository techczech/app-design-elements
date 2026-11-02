# Surfaces: where a feature opens

Every feature that adds interface states its surface type before visual design. A design without one is not ready to lock.

## The four types

| Type | Use it when | Examples |
|---|---|---|
| **Modal** | A short task that ends in a choice or a pick. You are not working anywhere else until it closes. | Slide insert, share, confirm, pickers, command palette |
| **Float** | A small companion you keep beside your work while you carry on editing. It holds things; it is not a place you work in. It can move, dock or collapse. | Slide Scratchpad |
| **Docked panel** | A tool for the current document that acts at the cursor or selection. It shares the main window and leaves the editor usable. | Image drawer, research panel, inspector |
| **Window** | A work area of its own: it spans documents, runs many steps, or is worth keeping open side by side with the main window. It has its own state and survives switching document. | Studio, Publications, Settings |

## Choosing

Ask in this order and stop at the first yes.

1. Does it end in seconds with a choice, and does nothing else make sense until then? **Modal.**
2. Does it act on the current document at the cursor? **Docked panel.**
3. Does it work across documents, or would the person want it beside the main window for minutes? **Window.**
4. Otherwise it is a small holding place used during editing: **Float.**

## Rules

- A modal never holds long work and never hides something the person needs to read in order to answer.
- A modal does not open from a background event. Automatic checks use a status mark.
- A float never covers text being edited by default. It can be moved, docked or collapsed, and it remembers its place.
- A window is never a modal in disguise: it blocks nothing and has no backdrop.
- A window remembers its size and position, reopens rather than duplicates, and is reachable from the palette.
- Where an app has a shared tools window, a new work area is a view in it. It gets a window of its own only if people need it beside another view, or it is output such as a presentation.
- The same kind of task gets the same type across apps. Settings is always a window.

## Other surfaces

- **Workspace mode:** replaces the main workspace for the same document, such as a slide browser. Treated as part of the main window. Use it when the task needs the whole space and leaves the document open.
- **Output windows:** presentation and audience windows are outputs, outside this choice.
