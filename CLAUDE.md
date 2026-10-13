# CLAUDE.md

Behavioral rules for working in this repo. This file is **identical in every repo**
and deliberately makes **no claims about any codebase** — so it cannot go stale.
Everything specific to this project lives in `docs/PROJECT.md`. All repo docs live in
`docs/`; only `README.md` and `CLAUDE.md` stay at the root.

Bias: caution over speed on non-trivial work. On genuinely trivial tasks, use judgment.

## 1. Session start

Before the first edit:

- Read `docs/PROJECT.md`. It is the only file that describes this repo's current state.
- Read the two or three files closest to the task — not the tree.
- Check whether a test already covers this area.

Architecture rationale, past traps, and planned work live in linked docs. Read them
when the task touches that area, not by default.

## 2. Before you write

- **Grep first.** Before adding any function, type, or helper, search for one that
  already does it. Reaching for training data instead of the existing codebase is the
  most common cause of duplicate implementations.
- Read the exports, the immediate callers, and the shared utilities you're touching.
- If you can't tell *why* existing code is shaped the way it is, ask. Structure that
  looks pointless usually isn't.

## 3. While you write

- **Simplest thing that solves the stated problem.** No speculative features, no
  abstractions for single-use code, no configurability nobody asked for, no error
  handling for states that can't occur.
- **Surgical diffs.** Every changed line traces to the request. Don't improve adjacent
  code, don't reformat, don't refactor what isn't broken. Notice dead code → mention
  it, don't delete it.
- Clean up only the orphans *your* change created — imports and helpers your edit made
  unused. Nothing pre-existing.
- **Local convention beats personal taste.** If a convention seems harmful, say so;
  don't quietly fork it.

## 4. Verification

- Turn the task into a verifiable goal before starting. "Add validation" → "write tests
  for invalid input, then make them pass." "Fix the bug" → "write a failing test that
  reproduces it, then make it pass."
- For multi-step work, state the plan as `step → how it's verified`.
- **Tests encode intent, not behavior.** A test that still passes when the business rule
  changes is not a test. Assert why the behavior matters, not that the function returned
  something.
- **Fail loud.** "Done" is false if anything was skipped. "Tests pass" is false if any
  were skipped, xfailed, or never ran. Report what actually happened, with the output.
- Never describe as verified anything you did not run.

## 5. When things conflict

- **Surface conflicts, don't average them.** If two patterns in the codebase
  contradict, pick one (more recent, better tested), say why, and flag the other for
  cleanup. Never blend them.
- **Flag uncertainty before writing, not after.** "This touches the shared auth guard,
  I want to confirm the blast radius" is worth more than a confident wrong diff.
- **Judgment calls to the model, deterministic ones to code.** Classification, drafting,
  summarizing, extraction — fine. Routing, retries, status-code handling, and
  transforms belong in code. If code can answer, code answers.

## 6. Where constraints and docs live

- Hard constraints live in `docs/PROJECT.md` § Constraints. Each is either backed by a named
  conformance test or tagged `[unverifiable]` with a reason. **An untagged, untested
  constraint is a bug in docs/PROJECT.md** — flag it when you notice one.
- When you change something `docs/PROJECT.md` asserts, update it in the same
  change. A doc slightly behind the code does more damage than one that's obviously
  wrong, because it gets trusted.
- Documenting a pattern: if it takes more than two sentences, point at the canonical
  file instead. Pattern-matching a real file beats following a written spec of it.
- Something that cost real debugging time → add it to `docs/GOTCHAS.md` as
  symptom → root cause → guard.
- Completed work moves out of `docs/BACKLOG.md` to `docs/archive/`. Finished history that
  stays in a read-every-session doc is a tax on every future session.

## 7. Ending a session

- **Never end a session with a dirty tree.** Commit the work, or state plainly why it
  can't be committed yet. Uncommitted work doesn't survive the session; the reasoning
  behind it definitely doesn't.
- **Work in progress belongs on a branch, never on the default branch.** A WIP commit
  on a branch costs nothing and is trivially amended or squashed later.
- Don't commit something you'd describe as broken just to satisfy the rule. If the tree
  can't go green, say what's unfinished and what the next step is — that's the honest
  version of the same instruction.
- `docs/TOKEN_DRAIN.md` is regenerated and staged by the pre-commit hook. It's derived data:
  never edit it by hand, and don't treat its contents as an input to any decision.

## 8. These rules are working if

- Diffs contain no lines unrelated to the request.
- Duplicate implementations stop appearing.
- Clarifying questions arrive before the code, not after the review.
- "Done" survives a check, every time.
- Sessions end with a clean tree and no orphaned reasoning.

If you catch yourself violating one of these, say so rather than quietly continuing.
