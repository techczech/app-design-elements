# Commands, keyboard and menus (elements 1–9)

Summary for design and review. The deep reference — modifier families, collision ladder, failure signatures, verification — is the `keyboard-and-commands` skill; load it before changing any chord, command or menu.

## Registry

- Each command: `id`, user-facing `name` (the user's words, grouped by what they are doing), `defaultChord` or explicit none, `when`/availability, `run`, `menu` placement (menu, group, order) or `noMenu` with a reason, and a class (content / view / settings / chrome) for agent access.
- Readers generated from it: palette, cheat sheet, Settings › Shortcuts, menu bar, agent operation list. Nothing hand-copies a chord.
- Shipping a command keyless is fine; shipping it unfindable is not.

## Palette `⌘⇧P`

- Complete command surface, not a search over a subset.
- Shows each command's effective chord.
- `⌘⇧,` rebinds the highlighted command in place.

## Reserved chords

| Chord | Surface | Tier |
|---|---|---|
| `⌘⇧P` | Command palette | always |
| `⌘K` | Contextual actions on the selection | always |
| `⌘,` | Settings | always |
| `⌘/` | Cheat sheet, works while typing | always |
| `⌘⇧,` | Rebind highlighted palette command | always |
| `⌘F` / `⌘⇧F` | Find in document / search everything | default-on |
| `⌘⇧K` | Navigation switcher | when journeys need it |
| `⌘P` | Preview / inspector | when journeys need it |

`⌘K` is deliberately not the web's switcher or insert-link. Link moves to `⌥⌘K` (displaced action keeps its letter, gains a modifier).

## macOS menu bar

- Generated from the registry. Every command except small repeat/movement keys marked `noMenu` with a reason.
- Menu items display the effective chord (overrides included); rebuild on rebind; display-only accelerators so dispatch stays with the registry.
- Fixed frame: **App** (About, Settings… `⌘,`, Quit) · **Edit** (standard roles) · **View** · app menus named by task · **Window** · **Help** (cheat sheet `⌘/`, Get started, How this app works).
- Unavailable commands appear disabled, not missing.
- Swift: same rule through `.commands` generated from the command table.
