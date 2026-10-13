# Architecture

Design and rationale, agreed over the design sessions on 2026-10-13. Built from the
valentinwerner.com homepage mock and the upgrade-me redesign (`cffafb7` there), after a
pass over loquol, hindsight and cache-tax, then refined in eight rounds of side-by-side
comparisons (`docs/archive/explore-rounds.html`). How to use it: `GUIDELINES.md`. What
the tests enforce: `PROJECT.md`.

## Principles

1. **Quiet, nothing that nags.** Every element competes for attention; take the quieter
   option and remove before adding.
2. **Yellow is the signature.** `#FFC500` marks action, progress and selection in every app,
   so it has to stay rare to keep meaning anything.
3. **Warm page, never pure.** Near-black `#100f0e` and cream `#faf7f2`, never `#000` or `#fff`.
4. **Individual, but quiet.** Character comes from mono data labels, the green cards, the
   lit selection and the arrows, not from decoration.
5. **Plain words.** No em dashes. Buttons are verbs. Errors say what happened, then what to do.

## Decisions

| Area | Decision | Why |
|---|---|---|
| Typeface | Archivo (variable, 100-900) + JetBrains Mono | Already the homepage and upgrade-me. Manrope, Roboto Flex and Plus Jakarta Sans were compared on the real hero and not taken. Variable loading fixes the 650/620/550 weights upgrade-me asked for and never got |
| Reading face | Sans only | One family. upgrade-me's system serif rendered differently per OS |
| Theme | Dark-first, light supported, follows the system unless the user picked one | |
| Dark page | `#100f0e` | Lighter pages blurred the step to the cards |
| Dark cards | Deep green graphite `#1c201c`, no edge, no shadow | The warm greys read brown ("grandpa"); the green against the warm page has the most character. Faint grey lifted to `#9b9488` to stay at 4.5:1 on it |
| Light page | Cream `#faf7f2`, cards `#fffcf6` with a soft small shadow, no edge | Lighter than the mock's `#f6f2ea` so colours pop; blue and green tints were tried and lost to cream. The shadow is 3-12px, not the broad one |
| Feature panels | Light: grey `#ebe4d6`; the "next up" banner fades yellow to grey (`.feature.lit`). Dark: the card surface | Banner and call to action pair up as one kind of surface. Green and peach gradient ends were too much |
| Colours | One set for both themes: info `#6ea8ff`, good `#5cc48a`, warn `#f0a060`, bad `#ff7a6b`; data adds violet `#c79bff` and pink `#ff8fb0` | The dark-mode set was preferred over every light-mode variant. Status and data share hues on purpose (info = data 1, good = data 2, warn = data 5); near-but-not-equal pairs looked awkward |
| Light-mode colour contrast | **Exception:** status and data colours stay exact in light mode, about 2:1 on cream, bold | Chosen over darker shades, underlines and tints ("good enough"). The test allows these roles in light mode down to a floor of 1.6:1 and still enforces 4.5:1 for every grey and link |
| Status | Mono caps in the status colour, bold, no pill, no dot | The tinted pill was the most generic element in the system; dots on top were "too much" |
| Notices | Hairline plus a mono status title, no box | |
| Active tab | Yellow line | A dot was tried and read as noise next to status text |
| Icon nav | Active icon gets a small yellow dot (from upgrade-me) | |
| Selected row | A soft radial fill, and an outline whose yellow glows mid top and bottom and fades to the sides (ellipse 35%) | Edge gradients at 100-135° looked scuffed where square row corners met the rounded list |
| Row hover | Faint wash, no arrow | The arrow added movement without information |
| Clickable cards | ↗ circle top right, yellow on hover, 2px lift | From the homepage cards |
| Card footers | `.foot` pins progress and counts to the bottom | Sibling cards with different description lengths were misaligned |
| Progress | 2px line with a mono percentage | Ticks and rings were compared |
| Charts | Direct labels over the top bar; `.chart-key` as fallback when labels would collide; hover any series element to fade the others | The dot legend was a turn-off |
| Section numbers | Not used | "There is no need for that number" |
| Buttons | Pills | Rectangles and a site/app split were compared in full screens |
| Radius | Sharp: 4 fields, 6 inner blocks, 8 cards and lists | |
| Density | One scale, 15px base | |
| Motion | Settle: 120ms colour, 180ms 2px lift, 320ms 8px entrance, one easing | |
| Greys | Text, soft, muted, faint | The mock had seven near-identical greys |
| Light links | Ink text, 2px yellow underline | Yellow text on cream is 1.4:1 |
| Selection | Yellow fill behind selected text; no yellow highlight blocks in content | |
| Delivery | Vanilla CSS vendored into each app by `scripts/sync.sh` | Every app is vanilla JS with no build step |
| Fonts | Self-hosted woff2 | No visitor IP to Google (GDPR, LG Munich 2022); offline apps get the real faces |

## Signatures

| Rule (everywhere) | Option (reach for when it fits) | Dropped |
|---|---|---|
| Tight headlines | Mono label above a headline (`.eyebrow`) | Middle dots as separators |
| No edges in dark: green surfaces carry depth | One yellow phrase per page (`.mark`) | Section numbers |
| Arrow characters in links and buttons | Numbered labels (`.num`) | Hover arrows on rows |
| Tabular numbers, data in mono | Round-cap line icons with node circles | Tinted status pills |
| Pill buttons | Photo fading into the page | |

## Token layers

`css/tokens.css` holds semantic roles (`--muted`, `--accent-ink`, `--feature`) set per
theme; components read only those. Names match upgrade-me's so it adopts the file
without renames. There is no separate primitive layer: with one brand and two themes, a
raw palette would be a second list of the same hex values.
