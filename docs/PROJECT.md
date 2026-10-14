# PROJECT.md: design-system

Shared visual language for Valentin's sites and apps (valentinwerner.com, upgrade-me,
loquol, hindsight): tokens, base styles and components as plain CSS, plus a theme script
and a reference page. No build step; apps vendor a copy with `scripts/sync.sh`.

Behavioral rules: `CLAUDE.md` (repo root). How to design with the system:
`GUIDELINES.md` (repo root). Beside this file in `docs/`: design and rationale in
`ARCHITECTURE.md`, planned work in `BACKLOG.md`, traps that cost debugging time in
`GOTCHAS.md`.

**Recorded exception to `CLAUDE.md` § "all repo docs live in `docs/`":** `GUIDELINES.md`
sits at the root because it is a deliverable of this repo, like `css/`, not a document
about it (decided 2026-10-14).

**Status:** all design decisions made; tokens, components, patterns and guidelines exist,
including the app elements decided in the 2026-10-14 review. No app has adopted it yet.
The fonts are fetched and committed in `fonts/`.

Agents reach this repo through the `design-system` skill in the skillset repo, which
points at `GUIDELINES.md`, `reference/` and `scripts/sync.sh` by path. Renaming any of
them breaks the skill; update it in the same change.

## Constraints

Each is backed by a conformance test in `tests/test_conformance.py` or tagged
`[unverifiable]` with the reason. ⛔ = currently failing; see `BACKLOG.md`.

| # | Constraint | Check |
|---|---|---|
| C1 | No em dashes in `css/`, `js/`, `reference/`, `docs/`, `scripts/`, `README.md` or `GUIDELINES.md` | `test_no_em_dashes` |
| C2 | Greys and links pass WCAG AA (4.5:1) on every surface in both themes; status colours pass 4.5:1 and data colours 3:1 in dark. Light mode keeps the dark colour set as a recorded exception, floor 1.6:1 | `test_colour_pairs_meet_wcag_aa` |
| C3 | Archivo is declared as a variable weight range, and every font-weight used in `css/` falls inside it | `test_font_weights_render_as_written` |
| C4 | Every control that sits in a bar (buttons, dropdowns, segments, fields, sort, steppers) takes its height from `--control-h` and nothing gives one a fixed height | `test_controls_in_a_bar_share_one_height` |
| C5 | No hex colour in `css/` outside `tokens.css` (masks exempt: they only read transparency) | `test_no_raw_hex_outside_tokens` |
| C6 | No middle dot in `css/`, `js/`, `reference/`, `README.md` or `GUIDELINES.md` | `test_no_middle_dots` |
| C7 | Arrows and ticks (`→ ↗ ← ✓`) only inside a mono element or a CSS rule that sets the mono font | `test_arrows_are_set_in_mono` |
| C8 | Every element a GFM markdown renderer can emit (tables, task lists, strikethrough, code included) has a style, globally or under `.md` | `test_markdown_output_is_fully_styled` |

## Canonical files

| Concern | File |
|---|---|
| Colour, type, space, radius, motion values | `css/tokens.css` |
| A component with all its states | `.btn` in `css/components.css` |
| Theme switching without a flash | `js/theme.js` |
| How everything looks together | `reference/index.html` |
| Every app element and why it looks that way | `reference/elements.html` |
| What goes on a screen, and the no-gos | `GUIDELINES.md` |

## Layout

```
css/fonts.css        @font-face for the self-hosted variable fonts
css/tokens.css       every value, dark default + light overrides
css/base.css         element defaults: type, links, selection, focus, reduced motion
css/components.css   buttons, nav, cards, rows, status, forms, charts, then the app elements:
                     app bar, menu, filter and sort bars, dialog, toast, table, settings,
                     tooltips, tour, state page, front door
js/theme.js          saved theme before first paint, toggleTheme(), [data-reveal]
js/components.js     toast(), menu keys and pickers, toggles, table sort and filters, steppers
reference/index.html     foundations, components and assembled patterns
reference/elements.html  every app element, with the reason beside it
docs/archive/        the comparison rounds and the 2026-10-14 review behind the decisions
scripts/sync.sh      vendor into an app as ds.css + theme.js + components.js + fonts/
scripts/fetch-fonts.sh  download the woff2 files into fonts/
```

## Environment

Any OS with Python 3 and git. Nothing to install for the CSS itself.

```
scripts/fetch-fonts.sh                          # once
python3 -m http.server 8765                     # then open http://localhost:8765/reference/
scripts/sync.sh ../upgrade-me/upgrade_me/web/static/ds
uvx --from pytest pytest -q tests
```

Opening `reference/index.html` straight from disk breaks the relative stylesheet links
in some previewers; serve the repo instead.
