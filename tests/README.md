# tests/

`test_conformance.py` checks the repo's rules, not its features. Every hard
constraint in `docs/PROJECT.md` § Constraints has one test here, named in that table.
A rule written only in prose gets skimmed; a rule written as a test blocks the commit.

**When they run:** on every commit (`.githooks/pre-commit`) and in CI, which
`--no-verify` can't skip.

**What they need:** only pytest. They read the source as text and never import it, so
they run on any machine that has the checkout, with no hardware, network or project
dependencies.

**Two kinds:**

- **Project-specific** (top of the file): one per `docs/PROJECT.md` row.
- **Generic** (bottom): the same in every repo. No credential files tracked, TLS
  verification never disabled, `CLAUDE.md` identical to the shared template,
  `docs/PROJECT.md` naming no dead paths, and every constraint naming a test that exists.

**When one fails:** the assertion message says why the rule exists and how to fix it.
If the rule itself is wrong, change the `docs/PROJECT.md` row and the test in the same
commit. A finding you can't fix yet is marked `xfail(strict=True)`, so the marker has
to come off once it's fixed.

Feature tests (unit tests, fixtures) live next to the code they test, not here.

## In this repo

| Test | Rule |
|---|---|
| `test_no_em_dashes` | C1: no em dashes in anything shipped or documented |
| `test_colour_pairs_meet_wcag_aa` | C2: every text and status pairing passes AA in both themes |
| `test_font_weights_render_as_written` | C3: variable Archivo, every weight inside its range |
