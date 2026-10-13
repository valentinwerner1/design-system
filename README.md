# design-system

Warm near-black, one yellow, quiet by default. The shared look for valentinwerner.com
and the apps around it, as plain CSS with no build step.

## Use it in an app

```
scripts/sync.sh path/to/app/static/ds
```

```html
<script src="ds/theme.js"></script>          <!-- in <head>, no defer -->
<link rel="stylesheet" href="ds/ds.css">
<link rel="stylesheet" href="app.css">       <!-- app-specific styles, after -->
```

Then `toggleTheme()` switches light and dark, and `data-reveal` on an element gives it
the entrance motion.

## See it

```
python3 -m http.server 8765
```

Open http://localhost:8765/reference/.

Decisions and why: `docs/ARCHITECTURE.md`. Rules the tests enforce: `docs/PROJECT.md`.
