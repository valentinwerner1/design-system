# Gotchas

Things that cost real debugging time. Symptom, root cause, guard.

## Arrows and ticks look different on every machine

- **Symptom:** `→ ↗ ← ✓` render in a different font from the text around them, and differ
  between Linux and Windows.
- **Root cause:** Archivo has none of them, so the browser borrows them from a system font.
  Google Fonts' JetBrains Mono doesn't help either: every subset it serves drops them.
- **Guard:** `scripts/fetch-fonts.sh` takes the full JetBrains Mono file from JetBrains' own
  repo, pinned to a commit; `.arrow` and `.go` set the mono font; test C7
  (`test_arrows_are_set_in_mono`) fails on an arrow outside a mono element.

## Markdown tables arrive as pipes

- **Symptom:** a table written by an agent shows as `| a | b |` text.
- **Root cause:** markdown-it's `"commonmark"` preset has no tables; they are a GitHub
  extension.
- **Guard:** the renderer configuration in `GUIDELINES.md` section 6 enables tables,
  strikethrough and task lists; test C8 (`test_markdown_output_is_fully_styled`) fails if
  `.md` leaves any element the renderer can emit unstyled.

## The pre-commit hook never runs the tests

- **Symptom:** every commit prints "no pytest found, conformance NOT checked", and a commit
  went in with a failing test (`b76e0c8`).
- **Root cause:** the hook looks for pytest in `.venv` or the system Python; here pytest
  only runs through `uvx`.
- **Guard:** until the hook has a `uvx` fallback (in `BACKLOG.md`), run
  `uvx --from pytest pytest -q tests` by hand before every commit.

## The reference page shows old CSS after an edit

- **Symptom:** after editing `css/` or `js/`, the browser shows the previous version, even
  after a reload.
- **Root cause:** `python3 -m http.server` sends no cache headers, so the browser caches the
  files heuristically.
- **Guard:** hard reload (Ctrl+Shift+R), or add a query string to the page URL and
  refetch the stylesheets.

## `gap` on a `.stack` does nothing

- **Symptom:** `style="gap: ..."` on a `.stack` element has no effect.
- **Root cause:** `.stack` spaces its children with margins (`.stack > * + *`), not flex or
  grid gap.
- **Guard:** use `display: grid; gap: ...` when the spacing must differ from `--space-4`.

## Numbers in a table turn yellow

- **Symptom:** table cells with class `num` render in the accent colour.
- **Root cause:** `.num` is the yellow mono numbering style in `css/components.css`.
- **Guard:** numeric table cells use `.numeric`.
