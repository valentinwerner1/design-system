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

## 2. Alignment and consistent formatting

- Siblings line up. Repeated cards put their footers in `.foot` so progress, counts and
  status sit at the same height regardless of how long the description is.
- The same kind of data looks the same everywhere: durations `32:10`, relative dates
  `2d ago`, counts `5 of 12`, percentages `42%`, all in `.meta` (mono).
- Everything snaps to the 4px grid (`--space-*`). No one-off margins.
- Numbers are tabular (set on `body`), so columns of figures line up.
- Text never wider than `--width-prose` (68ch). Body text is left-aligned, never centred.

## 3. Symbols over text, where they are unambiguous

- Navigation uses icons (`.icon-nav`), each with `aria-label` and `title`.
- Arrows carry direction: `→` continue or go, `↗` opens a destination, `←` `→` page.
- Use a word when a symbol could mean two things. A tooltip is never the only way to learn
  what something does.
- Icons are round-cap line drawings, 1.8 to 2px stroke, `currentColor`, 24px grid.

## 4. Colour

- Yellow means action, selection, progress or "this one". Never decoration.
- Status colours only for status, data colours only for data the app owns. They share hues
  (info = data 1, good = data 2, warn = data 5), so never put a status and a series of the
  same hue next to each other with different meanings.
- Status is mono caps text in its colour (`.badge`), never a tinted pill.
- Body text is never coloured. Colour sits in labels, marks and links.
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
- Placeholders are real examples ("Weekly sync"), not instructions.

## 7. Charts

- Label series directly on the chart (`.chart .labels`). Use `.chart-key` only when direct
  labels would collide.
- Every series element carries `data-s`; hovering any of them fades the others.
- Values in mono next to the bar, not inside it.
- The right chart for the question: stacked bar for parts of a whole per item, line for
  change over time, a single number when there is one number.

## 8. No-gos

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
| Mixing pill and square buttons, ad-hoc radii | `--radius-button` and the 4 / 6 / 8 scale |
| Title Case, "Welcome back, User!", "Unlock", "Seamless", "Supercharge" | Sentence case, plain words |
| Toasts for everything; modals to confirm non-destructive actions | Inline confirmation; undo instead of "are you sure?" |
| Spinners for every load | Keep the layout, show what's ready, mark what isn't |
| Disabled buttons with no reason | Keep it enabled and explain on use |
| Fake metrics, lorem ipsum, stock testimonials in shipped UI | Real data, or leave the space out |
| Legends made of coloured dots under a chart | Direct labels |
| House-shaped diagrams, decorative illustrations | Diagrams that show the real mechanism, or none |

## 9. Before you ship

- [ ] Squint test: the most important thing stands out, nothing else competes.
- [ ] One primary button, one lit element.
- [ ] Sibling cards and rows align; data formats match across the screen.
- [ ] Both themes checked; reduced motion checked.
- [ ] Keyboard: every action reachable, focus ring visible.
- [ ] 320px wide: nothing scrolls sideways, touch targets at least 40px.
- [ ] Empty, loading and error states exist and follow section 6.
- [ ] `uvx --from pytest pytest -q tests` passes in this repo after any token change.
