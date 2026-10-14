# Backlog

## Open decisions

- **Control borders vs contrast:** field borders (`--line-2`) are about 1.6:1 on the page.
  WCAG asks 3:1 for the boundary of an input. Raising it makes fields heavier, which works
  against the quiet look. Decide with a visual comparison. Related: settings fields now
  have no box at all (focus shows a yellow underline); decide whether that is enough.
- **Native `<select>`:** `GUIDELINES.md` says `.menu` for every dropdown, but
  `css/components.css` still styles `.select` (a native select). Remove it, or keep it as
  the no-JS fallback and say so.
- **Light mode for the homepage and hindsight's dashboard** (review ⚑B18): both are dark
  only today. hindsight's colours are exempt; light mode is a separate question.
- **Feature names in running text** (review ⚑B19): "Your games", "The one thing" keep a
  capital mid-sentence in hindsight. Quote them, bold them, or lower-case them.

## Next

- **A skill for frontend work, built on this design system:** loads `GUIDELINES.md`, the
  tokens and `reference/elements.html`, and helps build or review UI in any of the apps
  (pick the right component, apply the rules, run the no-go list and the "before you ship"
  checklist). Decide where it lives (the skillset repo) and how it stays in sync with this
  repo.
- **Pre-commit hook can't run the tests:** it looks for pytest in `.venv` or the system
  Python, but here pytest only runs through `uvx`, so every commit prints "conformance NOT
  checked". Add a `uvx --from pytest pytest` fallback (the hook comes from the
  repo-governance skill, so fix it there too). See `docs/GOTCHAS.md`.
- Adopt in upgrade-me first (names already match), then the homepage.
- Fix the homepage mock: 8 em dashes, middle dots, the two failing greys
  (`#6f695f`, `#736c62`), the 760ms reveals down to the settle timings, and its motion
  (review ⚑B14): drop the mouse-wheel hijack and the endless scroll-cue nudge, keep the
  snap at `proximity` at most.
- loquol: move from cool blue-black and azure to the shared base; speakers use `--data-*`.
- When each app adopts the system: dates and durations to the formats table in
  `GUIDELINES.md` (loquol's `DD/MM/YY`, upgrade-me's locale dates), placeholders to real
  examples, middle dots out, em dashes out of user-facing strings (loquol: "Meeting ended
  ... still recording", "No sessions yet ...", "No notes yet ..."; hindsight's `<title>`),
  empty states rewritten as invitations (review ⚑B11).
- Markdown (`GUIDELINES.md` section 6): upgrade-me renders with plain CommonMark, so module
  tables arrive as pipes; enable table, strikethrough and task lists. loquol renders the AI
  summary with its notes-editor converter (bullets and bold only); give read-only AI text a
  full GFM render into `.md`.
- hindsight: keeps its own colours (recorded exception), but its streak becomes a record
  ("best run"), not something you can lose.
- Every app hosted through Cloudflare gets an offline page built on `.state-page`.

## Later

- Components still missing: skeleton loader; document tabs with overflow (loquol's session
  tabs); audio player and scrubber; inline edit (click, Enter commits, Esc cancels);
  right-click context menu in the `.menu` look; outline beside a stage, collapsible on a
  phone (upgrade-me topic player); video embed with a credit line; selection bar for
  multi-select actions; window chrome for frameless desktop apps (loquol).
- Line charts and single-number tiles in the chart section.
- Icon set: a small shared set in the round-cap line style, plus logo construction rules
  for the per-app marks and favicons that follow the theme.
- `fmt.js`: relative date, date, duration and plural, following the formats table.
- Breakpoints as named values: the apps use 640, 760, 860, 940 and 960; pick three.
- Print styles for what gets printed (CV, summaries).
- A microcopy library: error, empty, undo, confirm and offline strings, with bad and good
  examples.
- A shared keyboard map beyond Ctrl+F / Ctrl+K / Esc (zoom, `?` for help) and the
  notification budget (at most 2 a week, threshold-based) as system rules.
- Social card / OG image template.
- Export tokens for non-web consumers (hindsight's GNOME extension stylesheet, pywebview
  window colours).
- Small: the `.arrow` hover nudge moves right, which is wrong for a back arrow (`←`). The
  17B front door demo uses an empty checkerboard as a placeholder for a real position.

## Proposed constraints (not agreed yet)

- The two light-theme blocks in `css/tokens.css` stay identical.
- No emoji in `css/`, `js/` or `reference/`.
