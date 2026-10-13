#!/usr/bin/env bash
# Copy the design system into an app as one vendored folder.
#
#   scripts/sync.sh <dest-dir>      e.g. scripts/sync.sh ../upgrade-me/upgrade_me/web/static/ds
#
# Writes <dest>/ds.css (fonts + tokens + base + components, in that order),
# <dest>/theme.js and <dest>/fonts/. The header in ds.css names the commit it came
# from, so an app always knows which version it runs. Apps never edit these files;
# app-specific CSS goes in the app's own stylesheet, loaded after ds.css.
set -euo pipefail

here="$(cd "$(dirname "$0")/.." && pwd)"
dest="${1:?usage: scripts/sync.sh <dest-dir>}"

if [ -n "$(git -C "$here" status --porcelain -- css js fonts)" ]; then
  echo "design-system has uncommitted changes in css/, js/ or fonts/; commit first so the header means something" >&2
  exit 1
fi

version="$(git -C "$here" rev-parse --short HEAD) $(git -C "$here" log -1 --format=%cs)"
mkdir -p "$dest/fonts"

{
  echo "/* design-system $version. Vendored by scripts/sync.sh: do not edit here. */"
  # fonts.css points at ../fonts from css/; in the vendored folder they sit beside ds.css.
  sed 's#\.\./fonts/#fonts/#g' "$here/css/fonts.css"
  cat "$here/css/tokens.css" "$here/css/base.css" "$here/css/components.css"
} > "$dest/ds.css"

cp "$here/js/theme.js" "$dest/theme.js"
if compgen -G "$here/fonts/*.woff2" > /dev/null; then
  cp "$here"/fonts/*.woff2 "$dest/fonts/"
else
  echo "warning: no fonts in $here/fonts yet (run scripts/fetch-fonts.sh); falling back to system fonts" >&2
fi

echo "synced design-system $version -> $dest"
