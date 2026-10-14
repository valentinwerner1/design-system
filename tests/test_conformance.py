# tests/test_conformance.py
"""Executable form of the constraints in docs/PROJECT.md § Constraints.

Every project-specific test here maps to exactly one row of that table, by name. If
you change a constraint, change both. A constraint that cannot be expressed as a test
must be tagged `[unverifiable]` in PROJECT.md with a reason, not quietly dropped.

Design rules for tests in this file:

- **Static only.** Parse the source, don't import it. These must run with nothing but
  pytest installed — no project dependencies, no hardware, no network. That is what
  lets them run in CI and in a pre-commit hook on a machine that only holds the
  checkout.
- **Assertion messages carry the why.** They are read at the moment someone is being
  blocked, which is the only moment the reasoning matters.

The checks below the divider are generic and apply to any repo. Add project-specific
ones above it.
"""

from __future__ import annotations

import ast
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _py_files(d: Path) -> list[Path]:
    return sorted(p for p in d.rglob("*.py") if "__pycache__" not in p.parts)


def _parse(p: Path) -> ast.Module:
    return ast.parse(p.read_text(encoding="utf-8"), filename=str(p))


def _imported_names(tree: ast.Module) -> set[str]:
    """Top-level module name of every import, including function-local ones."""
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            out.add(node.module.split(".")[0])
    return out


def _tracked(pattern: str) -> list[str]:
    """Files matching a pathspec that git is tracking."""
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--", pattern],
        capture_output=True,
        text=True,
    )
    return [ln for ln in out.stdout.splitlines() if ln.strip()]


# =============================================================================
# Project-specific constraints — one test per PROJECT.md row.
# =============================================================================

TOKENS = ROOT / "css" / "tokens.css"
EM_DASH = "—"


def _block(css: str, selector: str) -> str:
    """Body of the first rule whose selector is exactly `selector` (no nesting inside)."""
    m = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", css)
    assert m, f"{selector} block missing from css/tokens.css"
    return m.group(1)


def _decls(body: str) -> dict[str, str]:
    body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)
    return {k: v.strip() for k, v in re.findall(r"--([\w-]+)\s*:\s*([^;]+);", body)}


def _resolve(t: dict[str, str]) -> dict[str, str]:
    """Follow var(--x) references (e.g. --data-1: var(--info)) to a literal."""
    out = {}
    for k, v in t.items():
        seen = 0
        while (m := re.fullmatch(r"var\(--([\w-]+)\)", v)) and seen < 10:
            v, seen = t[m.group(1)], seen + 1
        out[k] = v
    return out


def _themes() -> dict[str, dict[str, str]]:
    css = TOKENS.read_text(encoding="utf-8")
    dark = _decls(_block(css, ":root"))
    # Light only overrides what differs; everything else (accent, status, data) carries over.
    light = {**dark, **_decls(_block(css, ':root[data-theme="light"]'))}
    return {"dark": _resolve(dark), "light": _resolve(light)}


def _rgba(value: str) -> tuple[float, float, float, float]:
    value = value.strip().lower()
    if value.startswith("#"):
        h = value[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    m = re.match(r"rgba?\(([^)]*)\)", value)
    assert m, f"unparseable colour {value!r}"
    parts = [p.strip() for p in m.group(1).split(",")]
    return (
        float(parts[0]),
        float(parts[1]),
        float(parts[2]),
        float(parts[3]) if len(parts) > 3 else 1.0,
    )


def _over(fg: str, bg: str) -> tuple[float, float, float]:
    """Composite a possibly translucent colour over an opaque one."""
    r, g, b, a = _rgba(fg)
    br, bgc, bb, _ = _rgba(bg)
    return (r * a + br * (1 - a), g * a + bgc * (1 - a), b * a + bb * (1 - a))


def _lum(rgb: tuple[float, float, float]) -> float:
    def ch(c: float) -> float:
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _ratio(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    hi, lo = sorted((_lum(a), _lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


SURFACES = ("bg", "surface", "surface-2", "feature")
TEXT_ROLES = ("text", "soft", "muted", "faint", "accent-ink")
STATUS = ("good", "warn", "bad", "info")
DATA = ("data-1", "data-2", "data-3", "data-4", "data-5")

# Deliberate exception, decided 2026-10-13 (docs/ARCHITECTURE.md): light mode uses the
# dark-mode status and data colours unchanged ("exact colour, bold"). They sit around
# 2:1 on cream. The floor stops them from quietly getting even fainter.
LIGHT_COLOUR_FLOOR = 1.6


def test_colour_pairs_meet_wcag_aa():
    """C2. Every text role is readable on every surface, in both themes.

    Text needs 4.5:1 (WCAG AA); status colours are text too. Data colours are marks,
    not text, so they need 3:1. The mock failed this at 10-11px with greys that
    looked fine on a bright monitor; numbers don't depend on the monitor.
    The one exception is status and data colours in light mode, see LIGHT_COLOUR_FLOOR.
    """
    failures = []
    for theme, t in _themes().items():
        for s in SURFACES:
            base = _over(t[s], "#000000")
            for role in TEXT_ROLES:
                r = _ratio(_over(t[role], t[s]), base)
                if r < 4.5:
                    failures.append(f"{theme}: --{role} on --{s} is {r:.2f}:1, needs 4.5")
            for role, need in [*((x, 4.5) for x in STATUS), *((d, 3.0) for d in DATA)]:
                r = _ratio(_over(t[role], t[s]), base)
                if theme == "light":
                    need = LIGHT_COLOUR_FLOOR
                if r < need:
                    failures.append(f"{theme}: --{role} on --{s} is {r:.2f}:1, needs {need}")
        r = _ratio(_over(t["on-accent"], "#000000"), _over(t["accent"], "#000000"))
        if r < 4.5:
            failures.append(f"{theme}: --on-accent on --accent is {r:.2f}:1, needs 4.5")
    assert not failures, (
        "Colour pairs below WCAG AA:\n  " + "\n  ".join(failures) + "\nAdjust the token in "
        "css/tokens.css (nudge lightness, keep the hue) rather than adding an exception."
    )


def test_no_em_dashes():
    """C1. No em dashes in anything the system ships or documents.

    It's a deliberate signature (hyphens, colons, or a new sentence instead) and an
    em dash is one of the most recognisable tells of generated text. CLAUDE.md is the
    shared template and tests/ is tooling, so both are out of scope.
    """
    offenders = []
    paths = [ROOT / "README.md", *(ROOT / d for d in ("css", "js", "reference", "docs", "scripts"))]
    for base in paths:
        files = (
            [base]
            if base.is_file()
            else sorted(p for p in base.rglob("*") if p.is_file())
            if base.exists()
            else []
        )
        for p in files:
            if p.suffix in {".woff2", ".png", ".jpg", ".ico"}:
                continue
            # Generated by the repo-governance hook, not written here.
            if p.name == "TOKEN_DRAIN.md":
                continue
            for i, line in enumerate(
                p.read_text(encoding="utf-8", errors="replace").splitlines(), 1
            ):
                if EM_DASH in line:
                    offenders.append(f"{p.relative_to(ROOT)}:{i}")
    assert not offenders, (
        f"em dash found at {offenders}. Use a hyphen, a colon, or split the sentence."
    )


def _weight_range(css: str, family: str) -> tuple[int, int] | None:
    for face in re.findall(r"@font-face\s*\{([^}]*)\}", css):
        if re.search(rf'font-family:\s*"{re.escape(family)}"', face):
            m = re.search(r"font-weight:\s*(\d+)\s+(\d+)\s*;", face)
            return (int(m.group(1)), int(m.group(2))) if m else None
    return None


def test_font_weights_render_as_written():
    """C3. Every font-weight in the CSS must exist in the loaded font.

    upgrade-me asked for 650, 620 and 550 while loading only static 400-700, so the
    browser silently rounded them to 700 and 600. Archivo is declared as a variable
    range in css/fonts.css; this checks the range is there and every weight fits it.
    """
    fonts = (ROOT / "css" / "fonts.css").read_text(encoding="utf-8")
    rng = _weight_range(fonts, "Archivo")
    assert rng, (
        'css/fonts.css must declare Archivo with a weight range ("font-weight: 100 900"). '
        "A single weight means static files, and in-between weights get rounded."
    )
    weights_var = {k: v for k, v in _themes()["dark"].items() if k.startswith("weight-")}
    used: list[tuple[str, int]] = []
    for p in sorted((ROOT / "css").glob("*.css")):
        if p.name == "fonts.css":
            continue
        text = re.sub(r"/\*.*?\*/", "", p.read_text(encoding="utf-8"), flags=re.S)
        for val in re.findall(r"font-weight:\s*([^;]+);", text) + re.findall(
            r"(?<![\w-])font:\s*(var\(--weight-[\w-]+\)|\d{3})\s", text
        ):
            val = val.strip()
            m = re.fullmatch(r"var\(--([\w-]+)\)", val)
            if m:
                val = weights_var.get(m.group(1), "")
            if val.isdigit():
                used.append((p.name, int(val)))
    bad = [f"{f}: {w}" for f, w in used if not rng[0] <= w <= rng[1]]
    assert used, "found no font-weight declarations; the parser is probably broken"
    assert not bad, f"weights outside Archivo's loaded range {rng}: {bad}"


# =============================================================================
# Generic — these apply to every repo. Keep them.
# =============================================================================

SECRET_PATHSPECS = [
    ".env",
    "*.pem",
    "*.key",
    "*.p12",
    "*.pfx",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "*credentials*.json",
    "client_secret*.json",
    "service-account*.json",
    "*.keystore",
    "*.jks",
]


def test_no_secret_files_tracked():
    """Credentials must never be committed, even to a private remote.

    Git history is effectively permanent — removing the file later does not remove
    it from every clone and every cached copy. The only cheap moment is before the
    first commit.
    """
    found = {spec: hits for spec in SECRET_PATHSPECS if (hits := _tracked(spec))}
    assert not found, (
        f"credential-shaped file(s) tracked by git: {found}. Untrack them "
        f"(git rm --cached), add them to .gitignore, and rotate anything exposed."
    )


def test_no_tls_verification_disabled():
    """Disabled TLS verification defeats the point of TLS.

    It is usually added to work around a corporate proxy whose CA isn't in certifi.
    The correct fix is the OS trust store (e.g. `truststore.inject_into_ssl()`),
    which keeps the proxy working while still rejecting an actual interceptor.
    """
    offenders: list[str] = []
    for p in _py_files(ROOT):
        # Skip every conformance file, not just the running one: this function holds
        # the literals it searches for, so any copy of it -- a vendored template, a
        # sibling package's suite -- would match itself.
        if p.name == "test_conformance.py":
            continue
        if any(part in {".venv", "node_modules", "build", "dist"} for part in p.parts):
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            code = line.split("#", 1)[0].replace(" ", "")
            if "verify=False" in code or "CERT_NONE" in code:
                offenders.append(f"{p.relative_to(ROOT)}:{i}")
    assert not offenders, (
        f"TLS verification disabled at {offenders}. Use the OS trust store instead of "
        f"turning verification off."
    )


def test_claude_md_matches_canonical():
    """CLAUDE.md is identical in every repo — that sameness is what makes it trustable.

    Per-repo edits belong in docs/PROJECT.md. Skipped when the skill isn't installed on
    this machine (e.g. a CI runner), since there is nothing to compare against.
    """
    canonical = Path.home() / ".claude/skills/repo-governance/assets/CLAUDE.md"
    local = ROOT / "CLAUDE.md"
    if not canonical.exists():
        pytest.skip("repo-governance skill not installed here")
    if not local.exists():
        pytest.skip("no CLAUDE.md in this repo yet")
    assert local.read_text(encoding="utf-8") == canonical.read_text(encoding="utf-8"), (
        "CLAUDE.md has drifted from the canonical template. Project-specific rules go "
        "in PROJECT.md; if the rule is genuinely universal, change the template and "
        "propagate it to every repo."
    )


def _project_md() -> Path | None:
    """docs/PROJECT.md by convention. A root PROJECT.md is still accepted so repos
    bootstrapped before the move to docs/ keep being checked rather than skipped."""
    for p in (ROOT / "docs" / "PROJECT.md", ROOT / "PROJECT.md"):
        if p.exists():
            return p
    return None


def test_project_md_paths_exist():
    """Catch the quiet failure: a doc that is only *slightly* behind the code.

    A stale path is trusted more than a search result, so it does damage without ever
    looking wrong. Paths in PROJECT.md are relative to the repo root, wherever the
    file itself lives.
    """
    project = _project_md()
    if project is None:
        pytest.skip("no docs/PROJECT.md yet")
    missing = []
    for token in re.findall(r"`([^`\s]+)`", project.read_text(encoding="utf-8")):
        # Only things that clearly denote a path in this repo.
        # "~" and "$" denote paths outside the repo; "<" marks a placeholder.
        if "/" not in token or token.startswith(("http", "<", "-", "~", "$", "/")):
            continue
        if "*" in token:
            continue
        candidate = token.rstrip(".,;:").split("#")[0]
        if not candidate.endswith(
            (".py", ".md", ".js", ".ts", ".json", ".yaml", ".yml", ".toml", ".sh", ".cfg")
        ) and not candidate.endswith("/"):
            continue
        if not (ROOT / candidate).exists():
            missing.append(candidate)
    assert not missing, (
        f"PROJECT.md references path(s) that no longer exist: {sorted(set(missing))}. "
        f"Update the doc in the same change that moved the code."
    )


def test_project_md_constraints_all_have_tests():
    """PROJECT.md promises a test per constraint. This checks the promise itself.

    Without it, the table can claim coverage that does not exist — which is exactly
    the failure this whole arrangement is meant to prevent.
    """
    project = _project_md()
    if project is None:
        pytest.skip("no docs/PROJECT.md yet")
    defined = {
        n.name
        for n in ast.walk(ast.parse(Path(__file__).read_text(encoding="utf-8")))
        if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
    }
    named, missing = set(), []
    for line in project.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| C") or "[unverifiable]" in line:
            continue
        for token in line.replace("`", " ").split():
            if token.startswith("test_"):
                named.add(token)
                if token not in defined:
                    missing.append(token)
    assert not missing, (
        f"PROJECT.md names test(s) that do not exist: {missing}. An untested, untagged "
        f"constraint is a bug in PROJECT.md — either write the test or tag it "
        f"[unverifiable] with a reason."
    )
