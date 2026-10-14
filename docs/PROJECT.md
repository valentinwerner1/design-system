# PROJECT.md: design-system

Shared visual language for Valentin's sites and apps (valentinwerner.com, upgrade-me,
loquol, hindsight): tokens, base styles and components as plain CSS, plus a theme script
and a reference page. No build step; apps vendor a copy with `scripts/sync.sh`.

Behavioral rules: `CLAUDE.md` (repo root). Beside this file in `docs/`: design and
rationale in `ARCHITECTURE.md`, how to design with it in `GUIDELINES.md`, planned work in
`BACKLOG.md`.

**Status:** all design decisions made; tokens, components, patterns and guidelines exist.
No app has adopted it yet. The fonts are fetched and committed in `fonts/`.

## Constraints

Each is backed by a conformance test in `tests/test_conformance.py` or tagged
`[unverifiable]` with the reason. ⛔ = currently failing; see `BACKLOG.md`.

| # | Constraint | Check |
|---|---|---|
| C1 | No em dashes in `css/`, `js/`, `reference/`, `docs/`, `scripts/` or `README.md` | `test_no_em_dashes` |
| C2 | Greys and links pass WCAG AA (4.5:1) on every surface in both themes; status colours pass 4.5:1 and data colours 3:1 in dark. Light mode keeps the dark colour set as a recorded exception, floor 1.6:1 | `test_colour_pairs_meet_wcag_aa` |
| C3 | Archivo is declared as a variable weight range, and every font-weight used in `css/` falls inside it | `test_font_weights_render_as_written` |

## Canonical files

| Concern | File |
|---|---|
| Colour, type, space, radius, motion values | `css/tokens.css` |
| A component with all its states | `.btn` in `css/components.css` |
| Theme switching without a flash | `js/theme.js` |
| How everything looks together | `reference/index.html` |
| What goes on a screen, and the no-gos | `docs/GUIDELINES.md` |

## Layout

```
css/fonts.css        @font-face for the self-hosted variable fonts
css/tokens.css       every value, dark default + light overrides
css/base.css         element defaults: type, links, selection, focus, reduced motion
css/components.css   buttons, nav, tabs, cards, rows, status, notices, forms, progress, charts
js/theme.js          saved theme before first paint, toggleTheme(), [data-reveal]
reference/           foundations, components and assembled patterns
docs/archive/        the comparison rounds behind the decisions
scripts/sync.sh      vendor into an app as ds.css + theme.js + fonts/
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
