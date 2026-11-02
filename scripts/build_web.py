#!/usr/bin/env python3
"""Build standalone web pages from the artifact sources in docs/.

The artifact sources (docs/mockup-carta-pengganti.html, docs/swimlane-flow.html)
are written without <!doctype>/<head>/<body> because the Claude artifact viewer
adds them. This script wraps each source in a full HTML document so the pages
also work on any web server (for example GitHub Pages serving /docs):

  docs/index.html     landing page
  docs/portal.html    succession planning portal
  docs/swimlane.html  swimlane flow

Run from the repository root:  python3 scripts/build_web.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

BASE_CSS = (":root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
            "body{margin:0}img{max-width:100%}[hidden]{display:none!important}")


def wrap(src: str) -> str:
    """Move everything up to the first </style> into <head>, the rest into <body>."""
    cut = src.index("</style>") + len("</style>")
    head, body = src[:cut], src[cut:]
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
            f"<style>{BASE_CSS}</style>\n{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n")


INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Succession Planning Portal</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
:root { --bg: #f8fcf6; --surface: #fff; --sunken: #f0f9ec; --line: #e6e6e6; --fg: #2a2b2e; --muted: #6a6b6d; --accent: #0d6636; --accent2: #4a9437; --brand: #52de56; --tint: #e3f3da; --warn: #945800; --warn-bg: #fdf0dc; }
@media (prefers-color-scheme: dark) { :root { --bg: #1d1e20; --surface: #2a2b2e; --sunken: #232427; --line: #4d4d4d; --fg: #f4f4f5; --muted: #bfc0c0; --accent: #6ebe46; --accent2: #52de56; --tint: #1f3d2a; --warn: #f0a93b; --warn-bg: #3a2a10; color-scheme: dark; } }
* { box-sizing: border-box; }
body { margin: 0; border-top: 4px solid var(--brand); background: var(--bg); color: var(--fg); font: 14px/1.5 "IBM Plex Sans", system-ui, sans-serif;
  padding: 32px max(16px, env(safe-area-inset-right, 0px)) 48px max(16px, env(safe-area-inset-left, 0px)); }
.wrap { max-width: 900px; margin: 0 auto; display: grid; gap: 16px; }
h1 { font-size: 24px; margin: 0; } p { margin: 0; color: var(--muted); }
.tier { font-size: 11px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--accent); }
.cards { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
@media (max-width: 640px) { .cards { grid-template-columns: 1fr; } }
a.card { display: grid; gap: 6px; padding: 18px; border: 1px solid var(--line); border-top: 3px solid var(--accent); border-radius: 10px; background: var(--surface); color: inherit; text-decoration: none; }
a.card:nth-child(2) { border-top-color: var(--accent2); }
a.card:hover { background: var(--sunken); }
a.card:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
a.card b { font-size: 17px; } a.card span.go { color: var(--accent); font-weight: 600; font-size: 13px; }
.note { background: var(--warn-bg); color: var(--warn); border-radius: 8px; padding: 10px 12px; font-size: 13px; }
.bm { font-style: italic; }
</style>
</head>
<body>
<div class="wrap">
  <div class="tier">Talent, Succession &amp; Leadership Pipeline</div>
  <h1>Succession Planning Portal</h1>
  <p>MCP · OCP · Readiness Validation &amp; IDP · 2026 cycle</p>
  <p class="bm">Portal Succession Planning · MCP · OCP · Readiness Validation &amp; IDP · Kitaran 2026</p>
  <div class="cards">
    <a class="card" href="portal.html"><b>Portal</b><p>Overview, dashboard, summary (PDF / PowerPoint), succession chart, readiness validation, IDP and employee card.</p><p class="bm">Gambaran, dashboard, ringkasan, carta pengganti, readiness validation, IDP dan kad pekerja.</p><span class="go">Open portal →</span></a>
    <a class="card" href="swimlane.html"><b>Swimlane flow</b><p>The six-stage process by role, criteria and scoring.</p><p class="bm">Proses enam peringkat ikut peranan, kriteria dan skor.</p><span class="go">Open swimlane →</span></a>
  </div>
  <div class="note">The portal opens with fictional sample data. To see the real list, load the MCP/OCP Masterlist inside the portal: the file is read in your browser only and is not uploaded.<br><span class="bm">Portal dibuka dengan data contoh rekaan. Muatkan Masterlist MCP/OCP di dalam portal untuk senarai sebenar: fail dibaca dalam pelayar anda sahaja dan tidak dimuat naik.</span></div>
</div>
</body>
</html>
"""


def main() -> None:
    (DOCS / "portal.html").write_text(wrap((DOCS / "mockup-carta-pengganti.html").read_text(encoding="utf-8")), encoding="utf-8")
    (DOCS / "swimlane.html").write_text(wrap((DOCS / "swimlane-flow.html").read_text(encoding="utf-8")), encoding="utf-8")
    (DOCS / "index.html").write_text(INDEX, encoding="utf-8")
    print("Built docs/index.html, docs/portal.html, docs/swimlane.html")


if __name__ == "__main__":
    main()
