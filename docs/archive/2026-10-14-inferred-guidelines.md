# What makes an app yours: inferred guidelines

**Archived 2026-10-14; the review is done.** The proposed files became `css/components.css`
(plus `css/base.css` and `--control-h` in `css/tokens.css`), `js/components.js` and
`reference/elements.html`; the rules went into `docs/GUIDELINES.md`. Original text follows.

**For review, 2026-10-14. Not committed.** Inferred from the code, CSS comments, docs and
commit history of upgrade-me, loquol and hindsight, plus the homepage mock, cache-tax and
claude-skins. Every rule cites where it came from. Generic best practice is left out
unless your apps already do it in a recognisable way.

How to read it:

- **Part A** is the rule list, grouped. Each rule is a candidate for `GUIDELINES.md`.
- **Part B** is every inconsistency I found, flagged **⚑**, most important first, each
  with a recommendation. These need your decision.
- **Part C** is what a complete system still lacks.
- **Part D** lists the 22 proposed reference elements, live at `reference/proposed.html`
  (code in `css/proposed.css` and `js/proposed.js`, not shipped by `sync.sh` yet).
- **Part E** is the short list of decisions I need from you, in order.

Sources are abbreviated: **UM** upgrade-me, **LQ** loquol, **HS** hindsight, **HP** the
homepage mock, **DS** this repo. "commit:" quotes a commit subject.

---

## Part A: the rules

### A1. Stance: what every app is for

1. **One job, said in one sentence with a contrast.** "Train on your own blunders. Your
   positions, not a puzzle book's." (HS front door). "Keep up with AI, a few minutes at a
   time." (UM join). "I get engineering and business to agree on something real." (HP).
   The hero states the job and what it is not.
2. **Built to survive you losing interest.** It has to become "a quiet routine", not
   "another thing to keep up with" (UM ARCHITECTURE). No maintenance a user has to do,
   no nagging. Notification budget: at most 2 a week, threshold-based (UM BACKLOG).
3. **No guilt.** "Never guilt nudges about progress or streaks", "streak loss is guilt by
   another name" (UM ARCHITECTURE, BACKLOG). News "never undoes your progress" (UM tour).
   See ⚑B2 for the conflict with hindsight.
4. **The person decides; the machine suggests.** "Clicking one applies that name - the
   user decides, nothing is named automatically from here" (LQ). commit: "Remove the two
   speaker-name features that read as guessing in testing".
5. **Say what's certain, hedge what isn't.** commit: "Write ambiguous speakers into the
   AI summary as a hedge, not a name" (LQ). commit: "Say which engine the app is using,
   instead of implying it" (HS).
6. **Mark machine-made content until a person has checked it.** UM's "unverified" label:
   "Written by the agents, not yet reviewed by a human". LQ keeps "Your notes" and the AI
   summary in separate boxes: "The AI never edits these."
7. **Never report success you haven't confirmed.** HS GOTCHAS §5: one dropped poll "closed
   the panel and toasted Done over a run that was still going". A done state comes from the
   thing being done, not from silence.
8. **Credit sources, never copy them.** Every source names its author; key points are
   paraphrased, and code drops any that copy 12+ words; videos play in YouTube's own
   player "so the view counts for the creator" (UM ARCHITECTURE, app.js).
9. **Private by default.** Guest mode that says exactly what a cookie means (UM join);
   "Let people reset their own password, so you never hold it" (HS commit); one error
   message for all three reset failures, because which one it was "is information about
   somebody" (HS web.py); voice profiles "kept on this computer" (LQ); no-cookie YouTube
   domain (UM); self-hosted fonts (DS).
10. **Show the cost before asking for it.** Time on every unit: "Start, 35 min", "About 35
    minutes", "3.5 h left" (UM). Long jobs say how long they are and that you can walk
    away (HS sync).

### A2. Layout: what gets the space

11. **The content is the hero; the chrome is the caption.** "The board is the content, the
    panel is the caption" - the board is sized from both window axes, the text panel takes
    what's left (HS). Applies to transcripts (LQ), modules (UM), charts.
12. **Survey views and work views are different places.** "The dashboard is somewhere you
    survey, the board is somewhere you work, and they are allowed to feel different" (HS).
    LQ's session view is "flat, full width, no cards". Cards belong on survey screens;
    work screens are flat.
13. **One hero, then the rest.** "Four full-width panels of equal weight read as a
    checklist: everything looks equally like the next thing to do. So: one hero naming the
    single habit worth fixing" (HS dashboard). UM's "Next up" does the same.
14. **Columns start level; siblings line up.** commit: "Lay the dashboard out in three
    columns that start level" (HS). UM join: "mirrored cards with buttons bottom left".
    The Building AI card misalignment you spotted is this rule broken (fixed in DS v1).
15. **Actions sit bottom-left of what they act on.** UM join cards, HS "drill button at the
    bottom-left of the one-thing card". Primary action first, on the left.
16. **No dead space.** commit: "Stop the one-thing card growing a dead band under the board"
    (HS). A lone section takes the full width (UM `cols()`, HS "whichever card is on its
    own gets the row").
17. **Show it only when it's something.** No "+0" on an equal position (HS); "Don't show a
    nameless 0% chip" (LQ commit); empty sections hidden (UM); the wipe-annotations button
    exists only while there are annotations (HS); prev/next only once there's a search term
    (LQ).
18. **Say it in the line, not in a legend.** commits: "Drop the band legend under the bars;
    each row's tooltip still names it", "Drop the cosine explainer under the bars; say it in
    the recognised line instead" (LQ). Direct chart labels in DS v1 follow this.
19. **Background goes last and closed.** Set-once display options "collapsed by default -
    they do not belong in the reading path of every single card"; the game history
    "collapsed by default and last in the panel" (HS).
20. **Controls keep their place.** "Equal thirds, one row: the control under the cursor keeps
    its position and size from card to card" (HS).
21. **Don't spoil the answer.** Motif tags come after the answer, "never beside the board.
    Reading 'Hung a piece' before you move tells you what to look for, which is the whole
    puzzle" (HS). UM BACKLOG: a failed test gives a guiding hint, not the answer.
22. **Long sequences are tables; short ones can be chips.** commit: "Give the move history a
    real move list instead of chip soup" (HS). "Six plies read fine as a run of chips;
    eighty do not."
23. **Wrap, don't truncate, what can't be guessed.** "A truncated motif is the one thing on
    this card you cannot work out from what's left" (HS).
24. **Reading has a measure; working has the window.** Prose capped, the board and the
    transcript get full width (HS, LQ, UM `main.narrow`).
25. **Hierarchy by meaning, not by habit.** The streak sits "at title weight rather than as
    13px grey text in the corner. It's the one number that's meant to feel like a score;
    the deck totals are reference material and can stay quiet" (HS).
26. **Housekeeping is visibly quieter.** "Housekeeping, not a thing you came here to do"
    (HS sync row).

### A3. Interaction

27. **Undo over "are you sure".** LQ toasts carry Undo for 12s; "exact undo" for voice
    samples. Confirm only before overwriting work you can't get back ("Confirms before
    overwriting an existing summary (your own notes are untouched)").
28. **A failure keeps the screen and says why.** "A failed call keeps the current screen and
    says why, instead of a dead button" (UM). commit: "Make a failed HQ re-transcribe say
    what happened, and leave a trace" (LQ).
29. **Try before you commit.** "Listen: play that speaker's line, then stop; again plays their
    next line - hear who it is before picking a name" (LQ). HS demo before sign-up.
30. **Don't punish curiosity.** commit: "Give the deck an exit, and stop punishing
    curiosity" (HS).
31. **Long jobs: the button is the progress, details one click away.** "A sync is minutes
    long and you are meant to walk away from it, so the button itself is the progress bar"
    (HS).
32. **Be honest when you don't know how long.** "A sliding sliver is honest about that; a bar
    stuck at 0% reads as wedged" (HS). A zero day "still gets a visible stub" (HS).
33. **Desktop apps behave like desktop apps.** Click, Ctrl and Shift selection "like Windows
    Explorer", right-click menu, Ctrl+K search, Ctrl +/-/0 zoom, Alt+drag, Esc closes, arrows
    move (LQ). Shortcuts appear where the action lives ("Next match (Enter)").
34. **Optimistic where it's safe.** Stop flips the panel immediately "so the Stop button can't
    linger if the backend's mode event is slow" (LQ).
35. **Phones are a real target.** commit: "Stop the dashboard scrolling sideways on a phone,
    and size the touch targets"; 44px boxes, the icon doesn't grow, "padding rather than a
    height" (HS).
36. **Own every control.** Native selects, confirms and scrollbars "wear someone else's
    theme" (HS); LQ's picker is "the app's own menu, not a native select". See ⚑B5.
37. **Selected and keyboard position look different.** "A tick rather than a highlight: the
    highlight means where the keyboard is, and the two must not look like each other" (HS).
38. **Reachable settings, gear not initials, tour once then "?".** commits: "Move the
    local/server switch into Settings, where the user can reach it" (HS), "Header: settings
    gear instead of the initial", "Guided tour of Home, from a ? button" (UM).
39. **Preferences are per device and survive missing storage.** UM `pref` and `storeGet`
    fall back when localStorage throws; HS board size; DS theme.
40. **The entry page is the same product.** "The front door opening onto a
    differently-coloured app reads as two products" (HS web.py).

### A4. Visual

41. **Same colour, same meaning, everywhere.** One colour per person across chips, picker,
    transcript (LQ). "The move you played is marked in the same red the app uses for a wrong
    answer everywhere else"; commit: "Put Your games beside The one thing, in the same red" (HS).
42. **The glyph carries the meaning; colour supports it.** "?? has to survive being skimmed"
    (HS). This is what makes the light-mode colour exception survivable: the word is always there.
43. **Tint by kind, full strength only as a marker.** "Every card is the same shape with a
    different tint, so the tint is the only thing that has to be said per card"; the swatch
    is the only undiluted use (HS dashboard).
44. **Three tiers beat a raw number.** commit: "Colour the similarity bars: match, possible,
    unlikely" (LQ); keep the number small beside it.
45. **Calm the chrome.** Scrollbars that would be "the lightest thing on the screen" pull the
    eye "to the one element that never has anything to say" (HS). Hover states acknowledge,
    they don't ask to be read.
46. **Identical on every platform.** Pieces and icons are SVG because glyph fonts "disagree
    differently on Windows than on Linux, which a packaged app cannot have" (HS). See ⚑B1.
47. **Your own marks, in currentColor.** UM chevrons with circuit nodes, HS pawn in a
    counter-clockwise arrow. Logos are stroked line drawings with round caps that take the
    text colour; brand yellow "in light mode too" (UM commit).
48. **Dark is the home ground, often with a greener working surface.** HS's dashboard is
    "deeper and greener than the rest of the app" - the same instinct as the DS green cards.

### A5. Words

49. **Commit-message voice in the UI.** Plain outcomes, full sentences, no jargon: "Say
    something when the machine is asleep, instead of error 1033". Your commit log is the
    best style guide you have.
50. **Labels talk; placeholders say what the field is for.** "Pick a username", "The email on
    your account"; placeholders "where a reset link would go", "whose games to analyse" (HS).
    See ⚑B9: this contradicts what I wrote in `GUIDELINES.md`.
51. **Features have names.** "Next up", "Waiting on you", "Test out", "The one thing", "Your
    games", "the front door", "HQ pass". Short, plain, used consistently in UI, docs and commits.
52. **Errors say what happened and what happens next.** "Couldn't save that: ... Try again in a
    moment." (UM). The asleep page says the machine is asleep, not 530 (HS).
53. **Playful words only where you wait.** claude-skins spinner words ("Brooding",
    "Conjuring") and done words; the dry joke lives in loading and empty moments, never in
    errors or actions.
54. **Ellipsis only for "in progress".** "Assessing…" (LQ). Placeholders currently use it too
    ("Find…"); see ⚑B10.

### A6. How you build it

55. **Vanilla, no build step, one file per concern.** All three apps; DS v1 kept this.
56. **Every non-obvious layout decision has a why-comment.** HS's CSS comments are the best
    design documentation in your repos; they name the bug, the measurement and the trade-off.
57. **UX rules become tests.** HS `test_a_silent_engine_is_not_blamed_on_the_cpu_build`, DS
    contrast tests. When a rule is checkable, it is checked.
58. **Every string through an escaper.** UM `esc()`, LQ `escHtml` "at every sink".

---

## Part B: inconsistencies ⚑

Ordered by how much they matter. Each has a recommendation; none is applied.

**⚑B1. Arrows and ticks render from a random system font.** Archivo has no `→ ↗ ← ✓`
(measured in the browser: the glyph width changes with the fallback font). HP, UM and DS
all use them as text; HS deliberately moved to SVG for exactly this. Worse:
`scripts/fetch-fonts.sh` downloads only the basic Latin subset, so even JetBrains Mono
would lose them once self-hosted.
*Recommend:* set `.arrow` and `.go` in JetBrains Mono (proposed element 01), and change
`fetch-fonts.sh` to fetch the full JetBrains Mono file, or the subset containing U+2190-21FF
and U+2713.

**⚑B2. Streaks: a score in hindsight, guilt in upgrade-me.** HS puts the streak "at title
weight", "meant to feel like a score", and a partial break ends it (commit: "make a partial
break the streak"). UM's docs rule streaks out: "streak loss is guilt by another name".
*Recommend:* one rule for all apps. My suggestion: show runs as a record ("best run: 12")
rather than something you can lose.

**⚑B3. Every app has its own accent.** HP and UM yellow; HS chess.com green `#81b64c` with
red for mistakes; LQ azure `#4a96da` on a cool blue-black. The family decision says yellow
everywhere.
*Recommend:* LQ moves fully (its blue becomes `--data-1`). HS is the real question: its
green is borrowed from chess.com so the board feels familiar. Keep the board colours as the
app's content palette, move the chrome to yellow.

**⚑B4. Tooltips: "nobody hovers" vs the place loquol keeps its explanations.** HS rejects
tooltips for anything that matters. LQ puts voice-match reasons and similarity bands in
tooltips, and its two dropped explainers moved into tooltips too.
*Recommend:* details on click (proposed element 19). Tooltips only name an icon.

**⚑B5. Native controls in some apps, custom in others.** HS and LQ replace native selects,
confirm dialogs and scrollbars; UM uses native `<details>` dropdowns and checkboxes; DS v1
ships a native `<select>`.
*Recommend:* proposed menu (03), dialog (04) and scrollbars (21) become the standard. Native
checkboxes stay, tinted with `accent-color`.

**⚑B6. Touch targets: 44 in hindsight, 40 in the system.** DS buttons, icon buttons and the
checklist all say 40px.
*Recommend:* proposed element 22: 44px under 760px wide, unchanged above.

**⚑B7. Em dashes in shipped UI, not just the mock.** Quoted with the dash written as
[em dash] so this file passes its own test. LQ: "Meeting ended [em dash] still recording.
Stop now?", "No sessions yet [em dash] start one with the "+" tab above.", "No notes yet [em dash] type to add
them.". HS `<title>`: "Hindsight [em dash] train on your own blunders". HP: 8. UM and LQ code
comments use them heavily (not user-facing).
*Recommend:* fix the user-facing ones when each app adopts the system; leave comments.

**⚑B8. Middle dots, which you dropped, are everywhere.** UM: "Next up · topic", "Start · 35
min", "rated confident · 2 modules to prove". LQ preview head: "date · status · duration ·
speakers". HS front door: "Request access · Have an invite code?". I slipped them into DS
twice today.
*Recommend:* decide what replaces them. In running text a comma or a new line; in metadata
rows, spacing (`gap`) between mono items, as the DS reference now does.

**⚑B9. My guideline on placeholders contradicts your practice.** `GUIDELINES.md` says
"placeholders are real examples, not instructions". HS does the opposite, and it reads well:
"where a reset link would go".
*Recommend:* change the guideline to yours: a placeholder says what the field is for, or
gives a real example when the format is the question (dates, codes).

**⚑B10. Three date formats and two duration formats.** LQ standardised on `DD/MM/YY` and
whole minutes ("32 min", "<1 min"); UM uses the browser locale ("Oct 13, 2026") and "3.5 h
left"; the DS reference shows `32:10` and "2d ago".
*Recommend:* one formats table: relative for recent ("2d ago"), `14 Oct` within the year,
`14 Oct 2025` beyond; durations as "32 min" for meetings and lessons, `mm:ss` only on a
timeline or player. All in `.meta`.

**⚑B11. Empty states.** UM "Nothing here yet" and "All caught up"; LQ "No sessions yet [em dash]
start one with the + tab above."; DS guideline says empty states invite and never say
"nothing here".
*Recommend:* UM's "All caught up / Nothing required left." is fine (it's a result, not an
apology); rewrite the other two.

**⚑B12. Fonts per app.** LQ Segoe UI Variable + Cascadia Code; HS system stack; HP and UM
Archivo + JetBrains Mono.
*Recommend:* Archivo everywhere except state pages (proposed 16), which stay on system fonts
by design (HS: no second request on the page with no second chance).

**⚑B13. Buttons.** DS pills; HS full-width 8px buttons on the front door; LQ 8px.
*Recommend:* pills everywhere; full width only in narrow single-column forms (proposed 17).

**⚑B14. The homepage moves more than the rules allow.** HP hijacks the mouse wheel to snap
between two screens, uses `scroll-snap: mandatory`, and the scroll cue nudges forever
(`animation: nudge infinite`). DS: "Nothing loops, bounces or pulses".
*Recommend:* drop the wheel handler and the loop; keep the snap as `proximity` at most.

**⚑B15. Toasts are a no-go in DS and a core tool in loquol.** DS lists "toasts for
everything" as a no-go; LQ uses them for Undo, background results and errors.
*Recommend:* both are right; write the line: toasts for Undo and for background results the
screen can't show, nothing else (proposed 05).

**⚑B16. Status dots.** HS severity is "one chip family with a coloured dot, not three
different coloured pills"; DS v1 dropped dots ("too much").
*Recommend:* keep v1 (no dots), and note HS's reason is satisfied: severity no longer looks
louder than a label.

**⚑B17. Progress shapes.** UM's banner uses donuts; DS v1 chose the 2px line; HS uses a ring
on the sync button.
*Recommend:* line for progress through content, ring only on a button that runs a long job
(proposed 10). Donuts go.

**⚑B18. Light mode.** UM and LQ have both themes; HP and HS are dark only.
*Recommend:* HP gets light for free with the system; HS keeps dark-only for the board view
if you want, but its dashboard and front door should follow the system.

**⚑B19. Feature names in capitals.** HS commits and comments write "Your games", "The one
thing" with capitals mid-sentence; UI headings are sentence case.
*Recommend:* names keep their capital only at the start of a heading; in running text,
quote or bold them instead.

**⚑B20. The light-mode colour exception needs words next to colour.** You chose exact
colours at about 2:1 on cream. That's only safe because status always has a word (A4.42).
*Recommend:* add to the rules: a status colour never appears in light mode without its word,
and never on body text.

**⚑B21. A generated file broke a committed test.** The repo-governance hook wrote
`docs/TOKEN_DRAIN.md` during the v1 commit; it contains em dashes, so `test_no_em_dashes`
fails on `b76e0c8`. The hook couldn't run pytest (not installed in the system Python), so
nothing caught it.
*Fixed in the working tree, not committed:* the test skips that generated file. Also worth
doing: install pytest where the hook finds it, so the gate runs on every commit.

**⚑B22. `fetch-fonts.sh` and the state page disagree.** Self-hosted fonts are right for apps;
HS's asleep page loads nothing on purpose. Not a bug, but the rule needs saying (see 16).

---

## Part C: what a complete system still lacks

Proposed today (Part D) covers most of the component gap. Still missing after that:

**Foundations**
- An SVG icon set in the round-cap line style: home, catalog, news, settings, help, search,
  sync, record, stop, play, pause, trim, export, close, chevrons, arrows. Today every app
  draws its own.
- Logo construction rules for the per-app marks (stroke weights, node circles, the 32-unit
  grid, how a mark sits next to its name), and favicons that follow the theme (UM does this).
- A formats table (⚑B10) and a `fmt.js` with the functions: relative date, date, duration,
  plural ("1 module" vs "2 modules", which UM already has).
- Breakpoints as named rules. The apps use 640, 760, 860, 940 and 960; pick three.
- Print styles for the things people will print (CV, summaries).

**Components not in today's proposal**
- Tabs for documents (LQ's session tabs with overflow arrows and a compact dropdown).
- Audio player and scrubber (LQ).
- Inline edit: click a title, Enter commits, Esc cancels (LQ).
- Context menu on right-click (same look as the menu; LQ).
- Outline / table of contents beside a stage, collapsible on a phone (UM topic player).
- Video embed with credit card (UM source cards).
- Selection bar for multi-select actions ("Merge shows at 2+, Delete at 1+", LQ).
- Window chrome for frameless desktop apps (LQ title bar, resize edges).

**Content**
- A microcopy library: error, empty, undo, confirm and offline strings in your voice, with
  bad and good examples like `about-me.md` has.
- Feature naming rules (⚑B19) and a list of the names in use.
- The placeholder rule rewritten (⚑B9).

**Behaviour**
- A keyboard map shared by all apps: Ctrl+K search, Esc close, arrows move, Enter open,
  Ctrl +/-/0 zoom, `?` help.
- Notification budget (2 a week, threshold-based) written as a system rule, not only in UM.
- Tour rules: runs once after onboarding, remembered per browser, reachable from `?`.
- Toast durations (proposed 05) and when not to toast.

**Engineering**
- Token export for non-web surfaces: HS's GNOME top-bar stylesheet, pywebview window colours,
  the favicon.
- A tested migration path per app (UM first: names already match).
- pytest available to the pre-commit hook (⚑B21).

---

## Part D: proposed reference elements

Live at `reference/proposed.html` (both themes checked). Code in `css/proposed.css` and
`js/proposed.js`; `scripts/sync.sh` does not ship them until you accept them.

| # | Element | Built from | Notes |
|---|---|---|---|
| 01 | Arrows in mono | HS SVG decision, ⚑B1 | Changes `.arrow` and `.go` |
| 02 | App bar | UM header | Brand hides its name on a phone |
| 03 | Menu | HS `.dd`, LQ picker | `popover` attribute, no JS to open; tick vs keyboard wash; arrow keys |
| 04 | Dialog | LQ confirm | Native `<dialog>`; only before overwriting work |
| 05 | Toast | LQ `toast()` | 4.2s / 12s with Undo / 10s errors, bottom-left |
| 06 | Segmented control | HS filters | For 2-4 options that change a view |
| 07 | Choice cards | UM `.pick`, `.level` | Checked gets the yellow ring |
| 08 | Stepper | UM onboarding | No labels, no numbers |
| 09 | Find bar and keys | LQ find, Ctrl+K | Prev/next hidden until there's a term |
| 10 | Job ring and unknown progress | HS sync | The button is the progress |
| 11 | Person chips | LQ speakers | One colour per person, share in mono |
| 12 | Pipeline | LQ readiness chips | Manual completion is dashed |
| 13 | Table | HS move list | Numbered column, mono figures |
| 14 | Week bars | HS progress | Zero day keeps a stub |
| 15 | Meter | LQ similarity | Match / possible / unlikely |
| 16 | State page | HS asleep page | System fonts in production |
| 17 | Front door | HS landing, UM join | Purpose placeholders |
| 18 | Settings rows | HS, UM settings | What it does, then the control |
| 19 | Details on click | HS sync details | Replaces explanatory tooltips |
| 20 | Coach mark | UM tour | Spotlight plus card |
| 21 | Scrollbars | HS | Thin, no track, no arrows |
| 22 | Touch targets | HS | 44px under 760px |

---

## Part E: decisions I need, in order

1. **⚑B1** arrows: mono, or SVG everywhere?
2. **⚑B3** hindsight: board keeps chess.com colours, chrome goes yellow?
3. **⚑B2** streaks: records instead of streaks in every app?
4. **⚑B10** one formats table, as recommended?
5. **⚑B9** placeholders: adopt your purpose style?
6. **⚑B8** what replaces middle dots in metadata rows?
7. Part D: which of the 22 elements go into `components.css`?
8. The proposed tests from `BACKLOG.md` (no raw hex outside tokens, light blocks identical,
   no emoji) plus two new candidates from this review: no `·` in shipped copy, and no
   glyph arrows outside `.arrow` / `.go`.

Uncommitted in the working tree: this file, `css/proposed.css`, `js/proposed.js`,
`reference/proposed.html`, and the one-line test fix for ⚑B21.

---

## Part F: review outcomes (2026-10-14, Valentin)

Verdicts on Part D, in his words where they set a rule. **New rule** marks something that
goes into `GUIDELINES.md`.

| # | Verdict | What changes |
|---|---|---|
| 01 | Accepted | Mono arrows. Answers ⚑B1. Still needed: real fonts fetched, `fetch-fonts.sh` keeps the arrow range |
| 02 | Accepted | None |
| 03 | Change | Menu stays. Sort becomes its own two-part control, see F1 |
| 04 | Accepted | None |
| 05 | Accepted | None (the text and the toasts both) |
| 06 | Accepted, extend | Build a gallery of filter elements, all at one height, see F1 |
| 07 | Keep, no rule | The component is fine; "a checkbox you can read" is too obvious to be a guideline |
| 08 | Change | Numbers are optional, not a sign the flow is too long. Visual steps stay |
| 09 | Change | Ctrl+F finds on screen; Ctrl+K searches the database. Find may offer exact match and replace |
| 10 | Change | The filling ring is the answer; the sliding sliver goes |
| 11 | Rethink | Challenges chips, see F3 |
| 12 | Change | Stages as icons, not text chips; done in `--good`; manual stays dashed |
| 13 | Change | Column widths and search/sort, see F4 |
| 14 | Reframe | Too obvious as a component rule. If kept, it is a principle: **brutally honest graphs, don't fake data** |
| 15 | Reframe | Tiers are right, but the guideline is about **making decisions and information easy**, not about "meters" |
| 16 | Elevate | See F5 |
| 17 | Redo | Two-column layout; access policy, see F6 |
| 18 | Extend | One example settings module showing every kind of setting, see F7 |
| 19 | Reverse | Tooltips on hover, used sparingly, see F8. Reverses ⚑B4's recommendation |
| 20 | Accepted, extend | The tour highlights one thing on the real app and dims or blurs the rest |
| 21 | Accepted | Custom scrollbars: dimmer, quieter, simpler than the browser's |
| 22 | Open | Not reviewed yet |

**F1. Filter and sort bars. New rule.**
- Filters are left-aligned. Sorting is right-aligned; if several controls sit on the right,
  sort is the leftmost of them.
- A sort is always two parts: a dropdown for the key, and a clickable icon on its left that
  reverses the order.
- The sort dropdown is a rounded rectangle, not a pill. Controls that open a list are not pills.
- Every control in one bar has the same height. A segmented control taller than the dropdown
  next to it is a defect. Candidate test: one control-height token used by all of them.
- Wanted: a gallery of the filter elements the apps can reuse.

**F2. Obvious things stay out.** Practices nobody would get wrong (a readable checkbox, a zero
day that still shows) are not design-system rules. The system records what makes an app his,
or what people really do get wrong.

**F3. Chips are for small amounts.** The 11 example doesn't need chips at all. What matters is
not "one colour per person" but **consistency** and **focus on what's important**: a speaker
with under 1% doesn't need to appear if showing them costs room or pushes other things around.

**F4. Tables.** Columns that don't need the width don't get it; a long-text column gets the
room instead of wrapping early. Every text column is searchable; every number or date
column is sortable.

**F5. Errors and offline. New rule.** Every app hosted through Cloudflare ships an offline
page (the homelab sleeps, so this is the normal case, not an edge case). Beyond that: handle
errors properly. Generic screens or unexpected behaviour look like something was forgotten.

**F6. Access. New rule.** Most apps don't lock people out: the default is open, or a demo.
Apps that can put real GPU or CPU load on the homelab warrant a login. The login screen is
two columns.

**F7. Settings module.** One reference module covering every kind of setting: a choice of
few (local/server as segments), a dropdown for many, free text, a toggle, a number, an
action button.

**F8. Tooltips. New rule.** Hover is right for a tooltip. The question is what deserves one:
only things where it adds real extra value. Conflicts with hindsight's "nobody hovers"
comment; hindsight's sync details (a long explanation) may stay a click panel, which is not
a tooltip.

**Built into `reference/proposed.html` after the review:** 03 sort control, 06b filter gallery
and two assembled bars (every control `--control-h`: 32px, 44px under 760px), 08, 09, 10,
12, 13, 14, 15, 18, 19, 20 as above. 11 and 17 are now three options each, waiting for a pick.

### Round 2 (same day)

| # | Verdict | Built |
|---|---|---|
| 03 | Reverse icon: no border, tight to its dropdown | Yes |
| 06b | Too squished; generous is on brand. List/grid as icons | `--control-h` 32 to 40px (the same as `.btn`); icon segments |
| 06c | New: pill or rectangle is not defined yet | Three options rendered, waiting for a pick |
| 08 | Count left-aligned, below the bars at the top of a page, above them at the bottom | Yes |
| 09 | Whole word: underlined "ab". Replace buttons are rectangles, like their neighbours | Yes |
| 10 | No text next to the ring; it repeats what the ring says | Yes |
| 11 | One line: option A. A bar: the reference chart. Leans to coloured names, like "new" and "updated" | A (coloured names), A2 (mark), B (chart) |
| 12 | The colour already says done; no tick. One icon per stage, as loquol does | Transcript, person, pen icons; tint for done, dashed for manual |
| 13 | Search on the column name: magnifier opens a narrow field on top; a funnel shows while filtered | Yes; the filter row is gone |
| 14 | Keep the stub, so it isn't "brutally" honest: renamed **Honest graphs**; the stub is grey, never the data colour | Yes |
| 15 | A general concept; the similarity tiers are one case of it | Text rewritten with other cases |
| 17 | Keep all three; C gets the form on the right, the reason as a side note | Yes |
| 18 | Number spinners squished: removed, steppers outside the box. Typed fields have no outline, a placeholder when empty, a text cursor | Yes; focus shows a thin yellow underline |
| 19 | All tooltips on hover, styled like the old click panel. **New rule: never ask a question and hide the answer.** "Why Markus?" removed | Yes |
| 20 | Blur too harsh | 2.5px to 1px, dim .3 to .4 |
| 22 | Unclear what a touch target is | Section rewritten with a desktop/phone demo |

### Round 3 (same day)

- **06c: B.** Rectangle for anything that holds a value and any button in a row with them;
  pill for an action standing on its own. Segments are now rectangles everywhere.
- **11: A**, coloured names. B (the chart) is the nicer design, but A is more coherent,
  simpler, smaller, and takes no attention where none is needed.
- **13:** the suggestions stand. Text columns search; columns with a few repeating values get
  a checkbox funnel; dates get a preset funnel ("Last 7 days"); numbers only sort.
- **22:** accepted. Accessibility matters; the light-mode colour exception stays as it is.
- **⚑B1 settled, and it was worse than flagged:** Google's JetBrains Mono drops → ↗ ← ✓ in
  every subset, not just the self-hosted one. `fetch-fonts.sh` now takes the full variable
  file from JetBrains' own repo, pinned to commit `02bb50b` (113 KB, has every glyph,
  checked with fontTools). The reference pages no longer load Google Fonts.

### Decisions on Part E (same day)

- **⚑B9 placeholders: A**, real examples of valid input. Search fields name what they search.
- **⚑B10 formats: B**, relative when recent, `14 Oct` this year, `14 Oct 2025` before,
  minutes for lengths, `32:10` only on a player. Table in `GUIDELINES.md` section 2.
- **⚑B8 separators:** leaning B (space between mono items); commas shown beside it in
  `reference/elements.html` 13b for a final look.
- **⚑B2 streaks: B**, a best run you can't lose.
- **⚑B3 colour: C**, one palette for every app, content included. Recorded exception:
  hindsight keeps its colours as they are.
- **Tests: yes.** C5 no raw hex outside tokens, C6 no middle dots, C7 arrows only in mono.
