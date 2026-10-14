# design-system

Warm near-black, one yellow, quiet by default. The shared look for valentinwerner.com
and the apps around it, as plain CSS with no build step.

**How to design with it: [`GUIDELINES.md`](GUIDELINES.md).** The CSS makes a screen look
right; the guidelines decide what goes on it. Read them before building UI, human or agent.

## Use it in an app

```
scripts/sync.sh path/to/app/static/ds
```

```html
<script src="ds/theme.js"></script>          <!-- in <head>, no defer -->
<link rel="stylesheet" href="ds/ds.css">
<link rel="stylesheet" href="app.css">       <!-- app-specific styles, after -->
<script src="ds/components.js"></script>     <!-- end of <body>: toasts, menus, tables -->
```

Then `toggleTheme()` switches light and dark, and `data-reveal` on an element gives it
the entrance motion.

## See it

```
python3 -m http.server 8765
```

Open http://localhost:8765/reference/ for the foundations and patterns, and
http://localhost:8765/reference/elements.html for every component with its reasoning.

Decisions and why: `docs/ARCHITECTURE.md`. Rules the tests enforce: `docs/PROJECT.md`.
