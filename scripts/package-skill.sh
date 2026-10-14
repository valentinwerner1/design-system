#!/usr/bin/env bash
# Package the design system as a self-contained Claude skill.
#
#   scripts/package-skill.sh <dest-dir> [zip]   e.g. scripts/package-skill.sh ../skillset/skills/design-system
#
# Writes <dest>/SKILL.md (from skill/SKILL.md), GUIDELINES.md, VERSION, references/ (the
# reference pages, pointed at the bundle) and assets/ds/ (what scripts/sync.sh writes into
# an app). <dest> is rebuilt from scratch, so a file removed here disappears there too.
# With a second argument, also writes a zip of the skill for upload to claude.ai.
# CI runs this on every push to main and commits the result to the skillset repo.
set -euo pipefail

here="$(cd "$(dirname "$0")/.." && pwd)"
dest="${1:?usage: scripts/package-skill.sh <dest-dir> [zip]}"
zip="${2:-}"

if [ -n "$(git -C "$here" status --porcelain -- css js fonts reference skill GUIDELINES.md)" ]; then
  echo "design-system has uncommitted changes; commit first so VERSION means something" >&2
  exit 1
fi
# Rebuilding deletes <dest>; only ever delete a folder this script wrote.
if [ -e "$dest" ] && [ ! -f "$dest/VERSION" ] && [ -n "$(ls -A "$dest")" ]; then
  echo "$dest exists and wasn't written by this script (no VERSION); refusing to replace it" >&2
  exit 1
fi

version="$(git -C "$here" rev-parse --short HEAD) $(git -C "$here" log -1 --format=%cs)"
rm -rf "$dest"
mkdir -p "$dest/references"

"$here/scripts/sync.sh" "$dest/assets/ds" > /dev/null
cp "$here/skill/SKILL.md" "$here/GUIDELINES.md" "$dest/"
echo "design-system $version. Packaged by scripts/package-skill.sh: do not edit here." > "$dest/VERSION"

# The pages load the four stylesheets and the scripts from ../css and ../js; in the
# skill they sit in assets/ds as one ds.css. "./" listed the folder when served; here
# it has to name the page.
for page in "$here"/reference/*.html; do
  sed -e '\#href="\.\./css/\(tokens\|base\|components\)\.css"#d' \
      -e 's#\.\./css/fonts\.css#../assets/ds/ds.css#' \
      -e 's#\.\./js/#../assets/ds/#g' \
      -e 's#href="\./"#href="index.html"#g' \
      "$page" > "$dest/references/$(basename "$page")"
done

if [ -n "$zip" ]; then
  zip="$(cd "$(dirname "$zip")" && pwd)/$(basename "$zip")"
  rm -f "$zip"
  (cd "$(dirname "$dest")" && zip -qr "$zip" "$(basename "$dest")")
  echo "zipped -> $zip"
fi

echo "packaged design-system $version -> $dest"
