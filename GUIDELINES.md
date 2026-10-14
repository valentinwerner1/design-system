# Guidelines

How to use the system well. Tokens and components make a screen look right; these rules
decide what goes on it. Written for people and for AI agents building UI: the no-go list
at the end is mostly the things generated UI gets wrong by default.

## 1. Attention budget

Every element competes with every other one. Before adding anything, list what is already
asking for attention on the screen and decide what wins.

- One primary action per view. One filled yellow button; everything else is ghost or quiet.
- One lit element per page: the `.feature.lit` banner, a `.mark` phrase, or the selected row.
  Never all three in the same viewport.
- Remove before adding. If a section is empty, hide it; don't show "nothing here".
- No badge, count or status unless the user would act differently because of it.
- Squint test: blur your eyes at the screen. What stands out should be what matters most.
- Make the decision easy. Do the reading for the person: name the one thing to do next
  instead of listing ten ("Next up", "The one thing"), sort a raw number into a few named
  tiers (match, possible, unlikely), preselect the sensible default. The detail stays
  reachable, quietly, and the person still decides.
- Show only what earns its room. A speaker under 1% folds into "+2" when showing them would
  cost space or push other things around.
- Chips only in small numbers. A list of people, stages or moves is a line, icons or a table.
- Nothing to lose. No streak that resets: show a run as a record ("best run: 12 days") next
  to what happened this week. Progress never goes backwards because you took a break.

## 2. Alignment and consistent formatting

- Siblings line up. Repeated cards put their footers in `.foot` so progress, counts and
  status sit at the same height regardless of how long the description is.
- The same kind of data looks the same everywhere, always in `.meta` (mono):

  | Kind | Format |
  |---|---|
  | Date, last 7 days | relative: `2h ago`, `2d ago` |
  | Date, this year | `14 Oct` |
  | Date, before this year | `14 Oct 2025` |
  | Time of day | 24-hour: `06:58` |
  | Length of a meeting, lesson, job | minutes: `32 min`, `1 h 10 min`, `<1 min` |
  | Position in a recording | `32:10`, only on a player or timeline |
  | Count | `5 of 12` |
  | Share | `42%` |

  Never the browser's locale format.
- Items in a metadata row are one `.meta` line separated by commas: "9 Oct, 58 min,
  5 speakers". No middle dots, no bullets.
- Everything snaps to the 4px grid (`--space-*`). No one-off margins.
- Numbers are tabular (set on `body`), so columns of figures line up.
- Text never wider than `--width-prose` (68ch). Body text is left-aligned, never centred.
- Every control in a bar is exactly `--control-h` tall (40px, 44px on a phone): dropdowns,
  segments, fields, toggles, sort, and the buttons beside them. A selector standing taller
  than the dropdown next to it is a defect. Controls are generous, never squished.
- Filters line up on the left. Sort sits on the right, the leftmost of whatever else is
  there, and is always two parts: a reverse-order icon (no border) right against the
  dropdown for the key.
- Tables: a column that doesn't need width doesn't get it (`.fit`), so long text gets the
  room instead of wrapping early.

## 3. Symbols over text, where they are unambiguous

- Navigation uses icons (`.icon-nav`), each with `aria-label` and `title`.
- Arrows carry direction: `→` continue or go, `↗` opens a destination, `←` `→` page.
- Use a word when a symbol could mean two things.
- Arrows and ticks are set in JetBrains Mono (`.arrow`, `.go`, menu ticks): Archivo has none,
  and a fallback font draws them differently on every OS.
- When the colour already says the state, there is no tick as well. A stage that is done is
  its own icon in `--good`, not a check mark.
- Tooltips open on hover, styled as a small panel. They are for what people care about but
  don't need on screen all the time: the name of an icon, its shortcut, what a number
  measures. Never the answer to a question the screen asks: if it's worth asking, the
  answer is on screen. No "?" buttons that hide an explanation.
- Icons are round-cap line drawings, 1.8 to 2px stroke, `currentColor`, 24px grid.

**Shape: rectangle or pill, by where it sits.** A rectangle (`--radius-md`) is anything
that holds a value (a field, a dropdown, segments, an on/off toggle) and any button in a row
with them. A pill is an action that stands on its own: the primary button, a form's submit,
a card's action, "Start tour".

## 4. Colour

- Yellow means action, selection, progress or "this one". Never decoration.
- One palette for every app, content included (boards, charts): no per-app accent colour.
  Recorded exception: hindsight keeps its own colours as they are.
- Status colours only for status, data colours only for data the app owns. They share hues
  (info = data 1, good = data 2, warn = data 5), so never put a status and a series of the
  same hue next to each other with different meanings.
- Status is mono caps text in its colour (`.badge`), never a tinted pill.
- Body text is never coloured. Colour sits in labels, marks and links.
- A person keeps one colour (`--data-*`) everywhere they appear, and their name carries it,
  the way a status word does. No chip, no dot.
- No gradients except `.feature.lit` and the selected-row glow.
- Known exception: in light mode the status and data colours are the dark-mode ones, about
  2:1 on cream (decided, see `ARCHITECTURE.md`). Keep them to short bold labels and
  marks; never use them for sentences.

## 5. Motion

- Settle timings only: 120ms for colour, 180ms for a 2px lift, 320ms for an 8px entrance.
- Nothing loops, bounces or pulses. Motion answers an action; it never asks for attention.
- Hover is a faint wash on rows and a 2px lift on cards. No arrows sliding in.
- Everything still works with reduced motion on (base.css switches it off).

## 6. Words

- No em dashes. Hyphens, colons, or a new sentence.
- Sentence case for everything, including buttons and headings.
- Buttons are verbs, one to three words: "Save", "Clear search", "Say hello".
- Errors say what happened, then what to do: "Couldn't reach the server. Your notes are
  kept locally. Try again in a minute."
- Empty states invite: name the space and offer the next step with an arrow link.
- No "successfully", "please", exclamation marks, or "simply / just / easy".
- Never ask a question and hide its answer.
- Placeholders are real examples of valid input ("Weekly sync", "magnuscarlsen"), not
  instructions. Search fields are the exception: they name what they search ("Find in
  transcript"), because an example query would read as a typed one.
- Text written by an AI or a person (summaries, notes, module content) is markdown, and it
  is always rendered, never shown raw. Render GitHub-flavoured: tables, task lists,
  strikethrough and fenced code on, raw HTML off. Put the result in `.md`, which styles
  everything the renderer can emit. CommonMark alone has no tables; that is why they
  arrived as pipes. In Python:

  ```python
  from markdown_it import MarkdownIt  # markdown-it-py
  from mdit_py_plugins.tasklists import tasklists_plugin  # mdit-py-plugins

  md = (
      MarkdownIt("commonmark", {"html": False})
      .enable(["table", "strikethrough"])
      .use(tasklists_plugin)
  )
  ```

## 7. Charts

- Label series directly on the chart (`.chart .labels`). Use `.chart-key` only when direct
  labels would collide.
- Every series element carries `data-s`; hovering any of them fades the others.
- Values in mono next to the bar, not inside it.
- The right chart for the question: stacked bar for parts of a whole per item, line for
  change over time, a single number when there is one number.
- Honest graphs: don't fake data. A zero day keeps a grey stub so the chart doesn't look
  broken, never in the data colour, so it can't pass for a small value. An axis doesn't
  start where it flatters; a number you don't have is missing, not estimated.

## 8. Interaction

Each of these is built in `reference/elements.html`, with its reason beside it.

- Undo over "are you sure". A dialog (`.dialog`) only before overwriting work that can't
  come back, like regenerating an AI summary.
- Toasts only for Undo and for background results the screen can't show. Bottom left;
  4 seconds, 12 with an action, 10 for errors.
- Our own controls, never the platform's: `.menu` for every dropdown, our scrollbars
  (thin, dim, no arrows). Native checkboxes stay, tinted.
- Keys: <kbd>Ctrl</kbd> <kbd>F</kbd> finds in what's on screen; <kbd>Ctrl</kbd> <kbd>K</kbd>
  searches everything the app holds. Esc closes, arrows move. The shortcut is shown where
  the action lives.
- Long jobs: the button that started it is the progress, a ring filling around it. No text
  beside it, no sliding sliver.
- Tables: number and date columns sort from their header. Text columns search from their
  header (a narrow field opens over it). Columns with a few repeating values get a funnel
  with checkboxes; dates get a funnel only for presets that answer a real question ("Last
  7 days"). While a column filters, its icon is a yellow funnel.
- Settings: what it does on the left, the control on the right. The control follows the
  choice: segments for two to four options, a dropdown for more, a field for text or a
  number, a switch for on and off, a button for a one-off action. Fields you type into have
  no box: a placeholder when empty, a text cursor on hover, a thin yellow line on focus.
  Numbers that get nudged have - and + outside the field. Destructive actions go last, in
  their own group.
- Steppers: the bars carry it. A count is optional, left-aligned, below the bars at the top
  of a page and above them at the bottom.
- The tour runs once after onboarding, then from "?". It points at one real thing at a time
  and blurs and dims the rest, gently.

## 9. Errors, offline and access

- Every app hosted through Cloudflare ships an offline page (`.state-page`). The homelab
  sleeps, so offline is the normal case, not an edge case. It says what's going on and
  what happens next, in system fonts, with no script.
- No generic screens. An error says what happened and what happens next; a failure keeps
  the screen and says why. A generic or unexpected screen reads as something forgotten.
- Most apps don't lock anyone out: open, or a demo. A login is only for apps that can put
  real GPU or CPU load on the homelab OR something that needs to be protected.
  It is two columns, the form on the right (`.door-split`).

## 10. No-gos

The tells of generic, AI-made UI. If a design has one of these, it needs a reason.

| Don't | Do instead |
|---|---|
| Purple/blue gradients, glass, glow, neon, gradient blobs behind the hero | Flat warm page; one `.feature.lit` panel |
| Emoji or sparkle icons (✨) for "AI" features | Line icons, or just say what it does |
| Tinted pill badges on everything | Mono caps status text, only where it changes a decision |
| Every section in a card; cards inside cards | Rows inside one surface; whitespace as the container |
| Three equal feature cards with an icon in a circle and "Fast. Secure. Simple." | Specific claims with real numbers, or nothing |
| Centred hero with a headline, two buttons and nothing true in it | A plain statement that's actually about the person or product |
| Rounded cards with a thick coloured left border as callouts | `.notice`: a hairline and a status title |
| Dashed boxes for empty states | One sentence and an arrow link |
| Shadows in dark mode; heavy, wide shadows in light | Green surfaces in dark, the soft small shadow in light |
| Pure `#000` / `#fff`, default Tailwind greys and `blue-500` | The tokens |
| Random font weights, Inter or Roboto by default | Archivo at the token weights |
| Pills and rectangles by mood, ad-hoc radii | The shape rule (section 3) and the 4 / 6 / 8 scale |
| Title Case, "Welcome back, User!", "Unlock", "Seamless", "Supercharge" | Sentence case, plain words |
| Toasts for everything; modals to confirm non-destructive actions | Inline confirmation; undo instead of "are you sure?" |
| Spinners for every load | Keep the layout, show what's ready, mark what isn't |
| Disabled buttons with no reason | Keep it enabled and explain on use |
| Fake metrics, lorem ipsum, stock testimonials in shipped UI | Real data, or leave the space out |
| Legends made of coloured dots under a chart | Direct labels |
| Native selects, confirm boxes and scrollbars | `.menu`, `.dialog`, the system's scrollbars |
| Chips for every person, stage or tag | A line, an icon per stage, or a table |
| A "?" that hides the explanation of what's on screen | Say it on screen; tooltips only name and measure |
| Controls of different heights in one bar | `--control-h` for all of them |
| House-shaped diagrams, decorative illustrations | Diagrams that show the real mechanism, or none |

## 11. Before you ship

- [ ] Squint test: the most important thing stands out, nothing else competes.
- [ ] One primary button, one lit element.
- [ ] Sibling cards and rows align; data formats match across the screen.
- [ ] Both themes checked; reduced motion checked.
- [ ] Keyboard: every action reachable, focus ring visible.
- [ ] 320px wide: nothing scrolls sideways, touch targets 44px.
- [ ] Every bar of controls is one height.
- [ ] Empty, loading, error and offline states exist and follow sections 6 and 9.
- [ ] Every text written by an AI or a person renders as markdown in `.md`, tables included.
- [ ] `uvx --from pytest pytest -q tests` passes in this repo after any token change.
