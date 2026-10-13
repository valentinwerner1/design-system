#!/usr/bin/env bash
# Download the variable woff2 files (latin subset) into fonts/, once.
# Both fonts are SIL Open Font License, so self-hosting and committing them is fine.
# Source is Google's font CDN via its CSS API; the file URLs change between releases,
# so they're read from the CSS rather than hard-coded.
set -euo pipefail

here="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$here/fonts"
# A modern user agent, or the API serves TTF instead of woff2.
ua="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

fetch() {  # fetch <css2 family query> <output file>
  local css url
  css="$(curl -fsSL -A "$ua" "https://fonts.googleapis.com/css2?family=$1&display=swap")"
  # The latin block is the last one in the response.
  url="$(printf '%s\n' "$css" | grep -o 'https://fonts.gstatic.com/[^)]*\.woff2' | tail -1)"
  curl -fsSL "$url" -o "$here/fonts/$2"
  echo "fonts/$2  $(wc -c < "$here/fonts/$2") bytes"
}

fetch "Archivo:wdth,wght@62..125,100..900" archivo-latin-var.woff2
fetch "JetBrains+Mono:wght@100..800" jetbrains-mono-latin-var.woff2
