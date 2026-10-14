# Backlog

## Open decisions

- **Control borders vs contrast:** field borders (`--line-2`) are about 1.6:1 on the page.
  WCAG asks 3:1 for the boundary of an input. Raising it makes fields heavier, which works
  against the quiet look. Decide with a visual comparison.

## Next

- Adopt in upgrade-me first (names already match), then the homepage.
- Fix the homepage mock: 8 em dashes, middle dots, the two failing greys
  (`#6f695f`, `#736c62`), and the 760ms reveals down to the settle timings.
- loquol: move from cool blue-black and azure to the shared base; speakers use `--data-*`.
- When each app adopts the system: dates and durations to the formats table in
  `GUIDELINES.md` (loquol's `DD/MM/YY`, upgrade-me's locale dates), placeholders to real
  examples, middle dots out.
- Markdown (GUIDELINES.md section 6): upgrade-me renders with plain CommonMark, so module
  tables arrive as pipes; enable table, strikethrough and task lists. loquol renders the AI
  summary with its notes-editor converter (bullets and bold only); give read-only AI text a
  full GFM render into `.md`.
- hindsight: keeps its own colours (recorded exception), but its streak becomes a record
  ("best run"), not something you can lose.

## Later

- Components still missing: dialog (as a real overlay), menu/dropdown, toast, tooltip,
  toggle switch, skeleton loader.
- Line charts and single-number tiles in the chart section.
- Icon set: a small shared set in the round-cap line style, plus logo construction rules
  for the per-app marks.
- Social card / OG image template.
- Export tokens for non-web consumers (hindsight's GNOME extension stylesheet).

## Proposed constraints (not agreed yet)

- No raw hex colours outside `css/tokens.css`.
- The two light-theme blocks in `css/tokens.css` stay identical.
- No emoji in `css/`, `js/` or `reference/`.
