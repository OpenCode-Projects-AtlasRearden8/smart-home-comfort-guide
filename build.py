#!/usr/bin/env python3
"""Build the Smart Home Comfort Guide static site from docs/*.md into site/.

Standard library only — no packages to install.

Usage:
    python3 build.py            build the site into ./site/
    python3 build.py --check    verify the build in a temporary directory

Output is deterministic: rebuilding produces byte-identical files.

Copyright (c) 2026 Asdale Dynamics, LLC
Licensed under the MIT License (see LICENSE).
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "docs"
SITE_DIR = ROOT / "site"

SITE_TITLE = "Smart Home Comfort Guide"
SITE_TAGLINE = (
    "A calm, privacy-first beginner manual for smart speakers, "
    "plugs, thermostats, and cameras."
)

# Reading order. (slug, short description used for the home page cards)
DOCS = [
    ("01-getting-started", "How to read this manual, and a gentle first path that avoids overwhelm."),
    ("02-what-devices-hear-and-send", "The honest, calm tour of what each device hears and what it sends out of your home."),
    ("03-smart-speakers", "Choosing, placing, muting, and living comfortably with a smart speaker."),
    ("04-smart-plugs", "The easiest win in home automation, plus the safety exceptions."),
    ("05-smart-thermostats", "Comfort and savings without surprises — plus the one wire worth photographing."),
    ("06-home-cameras", "Watching over your home while keeping placement and storage decisions yours."),
    ("07-local-control-first", "What “local control” means, why it is the privacy-friendly default, and starter picks."),
    ("08-guest-networks", "A second lane on your Wi-Fi, explained like a friend would, in ten minutes."),
    ("09-muting-and-factory-reset", "The “shh” switch you use often, and the clean-slate move you use rarely."),
    ("10-family-presets", "Print-friendly cards for less-techy family members: if this, do that."),
    ("11-room-by-room-checklist", "Walk each room once and finish with a sensible, ticked-off setup."),
    ("12-privacy-settings-table", "One table to check against your devices — then stop worrying about it."),
    ("13-glossary", "Every jargon word in this manual, explained in everyday language."),
]


# --------------------------------------------------------------------------
# Markdown conversion (a small, purpose-built subset: enough for this manual)
# --------------------------------------------------------------------------

LIST_RE = re.compile(r"^(\s*)[-*]\s+(.*)$")
ORD_RE = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
HR_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
TABLE_SEP_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$"
)


def slugify(text: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s_]+", "-", slug.strip())
    return re.sub(r"-+", "-", slug).strip("-") or "s"


def md_escape(text: str) -> str:
    return html.escape(text, quote=False)


def md_inline(text: str) -> str:
    """Convert inline markdown (bold, italic, code, links) to HTML."""
    s = md_escape(text)
    codes: list[str] = []

    def stash(match: re.Match) -> str:
        codes.append(match.group(1))
        return f"\x00C{len(codes) - 1}\x00"

    s = re.sub(r"`([^`]+)`", stash, s)
    s = re.sub(r"\[([^\]]+)\]\(([^()\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s, flags=re.DOTALL)
    s = re.sub(r"(?<!\*)\*([^*\s][^*]*)\*(?!\*)", r"<em>\1</em>", s)
    for i, code in enumerate(codes):
        s = s.replace(f"\x00C{i}\x00", f"<code>{code}</code>")
    return s


def fix_links(fragment: str) -> str:
    """Rewrite relative .md hrefs to .html."""

    def rewrite(match: re.Match) -> str:
        href = match.group(1).removesuffix(".md") + ".html" + (match.group(2) or "")
        return f'href="{html.escape(href, quote=True)}"'

    return re.sub(r'href="([^"]+\.md)(#[^"]*)?"', rewrite, fragment)


def checklist_li(content: str) -> str:
    m = re.match(r"^\[( |x|X)\]\s+(.*)$", content)
    if m:
        checked = ' checked=""' if m.group(1).lower() == "x" else ""
        return (
            f'<li class="check"><label><input type="checkbox"{checked}> '
            f"{md_inline(m.group(2))}</label></li>"
        )
    return f"<li>{md_inline(content)}</li>"


def render_table(rows: list[tuple[list[str], bool]]) -> str:
    head, body_rows = "", []
    for cells, is_header in rows:
        row = ("<th>%s</th>" if is_header else "<td>%s</td>") * len(cells)
        rendered = "".join(
            (f"<th>{md_inline(c)}</th>" if is_header else f"<td>{md_inline(c)}</td>")
            for c in cells
        )
        if is_header:
            head = f"<thead><tr>{rendered}</tr></thead>"
        else:
            body_rows.append(f"<tr>{rendered}</tr>")
    body = "<tbody>" + "".join(body_rows) + "</tbody>" if body_rows else "<tbody></tbody>"
    return f"<table>{head}{body}</table>"


def parse_table_row(line: str) -> list[str]:
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def md_to_html(text: str) -> str:
    """Parse the Markdown subset used by this manual into an HTML fragment."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: list[str] = []
    used_slugs: dict[str, int] = {}

    def flush_paragraph(buf: list[str]) -> None:
        if buf:
            out.append("<p>" + md_inline(" ".join(buf)) + "</p>")
            buf.clear()

    def close_table() -> None:
        if table_state["rows"]:
            out.append(render_table(table_state["rows"]))
            table_state["rows"] = []
            table_state["open"] = False

    # mutable state shared by helpers
    table_state: dict = {"rows": [], "open": False}

    def parse_list(start: int) -> tuple[str, int]:
        """Parse a run of list lines; supports one nesting level."""
        items: list[tuple[int, bool, str]] = []  # (indent, ordered, content)
        i, n = start, len(lines)
        while i < n:
            line = lines[i]
            if not line.strip():
                # blank line: continue only if the next non-blank is a list line
                j = i + 1
                while j < n and not lines[j].strip():
                    j += 1
                if j < n and (LIST_RE.match(lines[j]) or ORD_RE.match(lines[j])):
                    i = j
                    continue
                break
            indent = len(line) - len(line.lstrip(" "))
            mo, mo2 = LIST_RE.match(line), ORD_RE.match(line)
            if indent == 0 and not (mo or mo2):
                break
            if mo:
                items.append((indent, False, mo.group(2)))
            elif mo2:
                items.append((indent, True, mo2.group(3)))
            elif items and indent >= 2:
                # continuation line: fold into the previous item
                ind, ordered, content = items[-1]
                items[-1] = (ind, ordered, (content + " " + line.strip()).strip())
            else:
                break
            i += 1

        def render(list_items: list[tuple[int, bool, str]], fallback_ordered: bool) -> str:
            tag = "ol" if (list_items[0][1] if list_items else fallback_ordered) else "ul"
            pieces = [f"<{tag}>"]
            k = 0
            while k < len(list_items):
                _, _, content = list_items[k]
                nested = []
                j = k + 1
                while j < len(list_items) and list_items[j][0] > 0:
                    nested.append(list_items[j])
                    j += 1
                li = checklist_li(content)
                if nested:
                    li = li.replace("</li>", render(nested, tag == "ol") + "</li>", 1)
                pieces.append(li)
                k = j
            return "".join(pieces) + f"</{tag}>"

        return render(items, items[0][1] if items else False), i

    para: list[str] = []
    in_code = False
    code_buf: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if in_code:
            if stripped.startswith("```"):
                out.append("<pre><code>" + md_escape("\n".join(code_buf)) + "</code></pre>")
                code_buf, in_code = [], False
            else:
                code_buf.append(line)
            i += 1
            continue

        if not stripped:
            flush_paragraph(para)
            close_table()
            i += 1
            continue

        if stripped.startswith("```"):
            flush_paragraph(para)
            close_table()
            in_code = True
            i += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if heading:
            flush_paragraph(para)
            close_table()
            level, htext = len(heading.group(1)), heading.group(2)
            slug = slugify(htext)
            count = used_slugs.get(slug, 0)
            used_slugs[slug] = count + 1
            if count:
                slug = f"{slug}-{count}"
            out.append(f'<h{level} id="{slug}">{md_inline(htext)}</h{level}>')
            i += 1
            continue

        if HR_RE.match(line):
            flush_paragraph(para)
            out.append("<hr>")
            i += 1
            continue

        if (
            not table_state["open"]
            and stripped.startswith("|")
            and i + 1 < n
            and TABLE_SEP_RE.match(lines[i + 1])
        ):
            flush_paragraph(para)
            table_state["rows"] = [(parse_table_row(line), True)]
            table_state["open"] = True
            i += 2
            continue

        if table_state["open"] and stripped.startswith("|") and not HR_RE.match(line):
            table_state["rows"].append((parse_table_row(line), False))
            i += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph(para)
            close_table()
            quote: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>" + md_to_html("\n".join(quote)) + "</blockquote>")
            continue

        if LIST_RE.match(line) or ORD_RE.match(line):
            flush_paragraph(para)
            close_table()
            frag, i = parse_list(i)
            out.append(frag)
            continue

        para.append(stripped)
        i += 1

    flush_paragraph(para)
    close_table()
    if in_code:
        out.append("<pre><code>" + md_escape("\n".join(code_buf)) + "</code></pre>")

    return fix_links("\n".join(p for p in out if p))


# --------------------------------------------------------------------------
# Page assembly
# --------------------------------------------------------------------------

def doc_title(slug: str) -> str:
    md_text = (DOCS_DIR / f"{slug}.md").read_text(encoding="utf-8")
    match = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
    return match.group(1).strip() if match else slug


PAGE_CSS = """:root{--ink:#253331;--muted:#5b6a67;--bg:#fbfaf7;--card:#ffffff;--accent:#0f766e;--accent-soft:#e3f0ee;--line:#e4e1d8;--warn-bg:#fdf3e3;--code-bg:#f2f1ec}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:2px}a:hover{color:#0b5d57}
.wrap{max-width:52rem;margin:0 auto;padding:0 1.25rem}
header.site{background:var(--card);border-bottom:1px solid var(--line);padding:.9rem 0}
header.site .wrap{display:flex;align-items:baseline;justify-content:space-between;gap:1rem;flex-wrap:wrap}
.site-title{font-weight:700;font-size:1.05rem;color:var(--ink);text-decoration:none}
.site-title span{color:var(--accent)}
.site-tagline{color:var(--muted);font-size:.85rem;display:none}
main{padding:2.25rem 0 3rem}article{max-width:46rem}
h1{font-size:1.9rem;line-height:1.25;margin:0 0 1rem}
.lede{font-size:1.08rem;color:var(--muted)}
h2{font-size:1.3rem;margin:2.2rem 0 .7rem;padding-top:.35rem;border-top:1px solid var(--line)}
h3{font-size:1.08rem;margin:1.6rem 0 .5rem}
table{width:100%;border-collapse:collapse;margin:1.2rem 0;font-size:.92rem;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden}
th,td{text-align:left;padding:.55rem .7rem;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td,tr:last-child th{border-bottom:none}
blockquote{margin:1.2rem 0;padding:.8rem 1.1rem;background:var(--warn-bg);border-left:4px solid #e0a34a;border-radius:0 8px 8px 0}
blockquote p{margin:.35rem 0}
code{background:var(--code-bg);padding:.1rem .35rem;border-radius:4px;font-size:.9em;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
pre{background:var(--code-bg);border:1px solid var(--line);border-radius:8px;padding:.9rem 1rem;overflow-x:auto}pre code{background:none;padding:0}
ul,ol{padding-left:1.4rem}li{margin:.3rem 0}
li.check{list-style:none;margin-left:-1.4rem}
li.check label{display:flex;gap:.55rem;align-items:flex-start}
li.check input{margin-top:.32rem}
hr{border:none;border-top:1px solid var(--line);margin:2rem 0}
.pager{display:flex;justify-content:space-between;gap:1rem;margin-top:3rem;padding-top:1rem;border-top:1px solid var(--line);font-size:.92rem}
.pager span{color:var(--muted)}
footer.site{border-top:1px solid var(--line);background:var(--card);color:var(--muted);font-size:.85rem;padding:1.4rem 0}
footer.site p{margin:.3rem 0}
.btn{display:inline-block;background:var(--accent);color:#fff;border-radius:8px;padding:.55rem 1.1rem;text-decoration:none;font-weight:600}.btn:hover{background:#0b5d57;color:#fff}
.btn.ghost{background:transparent;color:var(--accent);border:1px solid var(--accent)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));gap:1rem;margin:1.5rem 0}
.cards .card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem;display:block;text-decoration:none;color:var(--ink)}
.cards .card:hover{border-color:var(--accent)}
.cards .card b{color:var(--accent)}
.cards .card p{margin:.35rem 0 0;font-size:.88rem;color:var(--muted)}
.toc{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem 1.25rem;margin:1.5rem 0;font-size:.92rem}
.toc ul{margin:.3rem 0;padding-left:1.1rem}
.hero{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1.75rem 1.5rem;margin-bottom:2rem}
.hero h1{margin-bottom:.5rem}
.hero .btns{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1.1rem}
.credit{color:var(--muted)}
@media print{header.site,footer.site,.pager,.toc{display:none}body{background:#fff}a{color:inherit}" """.strip() + "\n::-webkit-scrollbar{height:8px}\n"


def page_html(title: str, description: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(description, quote=True)}">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site"><div class="wrap">
<a class="site-title" href="index.html">Smart Home <span>Comfort Guide</span></a>
<span class="site-tagline">privacy-first, in plain English</span>
</div></header>
<main class="wrap">
<article>
{body}
</article>
</main>
<footer class="site"><div class="wrap">
<p>© 2026 Asdale Dynamics, LLC · MIT License · {html.escape(SITE_TAGLINE)}</p>
</div></footer>
</body>
</html>
"""


def dieta(body: str) -> str:  # small helper kept for readability of pager below
    return body


def doc_page(slug: str, prev_doc, next_doc) -> str:
    md_text = (DOCS_DIR / f"{slug}.md").read_text(encoding="utf-8")
    title = doc_title(slug)
    body_md = re.sub(r"^#\s+.+\n", "", md_text, count=1)
    body = md_to_html(body_md)

    headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    toc = ""
    if len(headings) >= 3:
        items = "".join(
            f'<li><a href="#{hid}">{html.escape(re.sub(r"<[^>]+>", "", text))}</a></li>'
            for hid, text in headings
        )
        toc = f'<nav class="toc"><strong>On this page</strong><ul>{items}</ul></nav>'

    pager = '<nav class="pager">'
    if prev_doc:
        prev_slug, prev_title = prev_doc
        pager += (
            f'<span>← Previous: <a href="{prev_slug}.html">{prev_title}</a></span>'
        )
    if next_doc:
        next_slug, next_title = next_doc
        pager += (
            f'<span>Next: <a href="{next_slug}.html">{html.escape(next_title)}</a> →</span>'
        )
    pager += "</nav>"

    first_paragraph = re.search(r"<p>(.*?)</p>", body, re.DOTALL)
    if first_paragraph:
        description = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", first_paragraph.group(1))).strip()[:160]
    else:
        description = SITE_TAGLINE

    return page_html(f"{title} — {SITE_TITLE}", description, toc + body + pager)


HOME_BODY = """<section class="hero">
<h1>Smart Home Comfort Guide</h1>
<p class="lede">A calm, plain-English manual for smart speakers, plugs, thermostats, and
cameras — written privacy-first, with a local-control mindset. No fear, no hype,
no product pushing. Just clear steps for a home that is comfortable
<em>and</em> kind to your privacy.</p>
<div class="btns">
<a class="btn" href="01-getting-started.html">Start reading</a>
<a class="btn ghost" href="11-room-by-room-checklist.html">Room-by-room checklist</a>
</div>
</section>

<section>
<h2>Why this guide</h2>
<p>Smart devices are tools: they listen, switch, warm, and watch, in service of
small everyday comforts. Each one has senses and habits worth knowing about,
which is exactly what this manual explains — calmly, once, and in order. When
you are ready to act, the <a href="11-room-by-room-checklist.html">room-by-room
checklist</a> and the <a href="12-privacy-settings-table.html">privacy settings
table</a> turn the reading into twenty tidy minutes.</p>
<p class="credit">Published by <strong>Asdale Dynamics, LLC</strong>. This site is
self-contained: no JavaScript, no analytics, no network requests.</p>
</section>

<section>
<h2>The manual</h2>
<div class="cards">
{cards}
</div>
</section>"""


def home_page() -> str:
    cards = [
        f'<a class="card" href="{slug}.html"><b>{html.escape(doc_title(slug))}</b>'
        f"<p>{html.escape(desc)}</p></a>"
        for slug, desc in DOCS
    ]
    body = HOME_BODY.format(cards="\n".join(cards))
    return page_html(SITE_TITLE, SITE_TAGLINE, body)


def build_into(site_dir: Path) -> list[Path]:
    """Build the site into `site_dir`. Returns the list of files written."""
    site_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    titles = [doc_title(slug) for slug, _ in DOCS]
    for idx, (slug, _) in enumerate(DOCS):
        prev_doc = (DOCS[idx - 1][0], titles[idx - 1]) if idx > 0 else None
        next_doc = (DOCS[idx + 1][0], titles[idx + 1]) if idx + 1 < len(DOCS) else None
        out = site_dir / f"{slug}.html"
        out.write_text(doc_page(slug, prev_doc, next_doc), encoding="utf-8")
        written.append(out)

    home = site_dir / "index.html"
    home.write_text(home_page(), encoding="utf-8")
    written.append(home)

    css = site_dir / "style.css"
    css.write_text(PAGE_CSS, encoding="utf-8")
    written.append(css)

    return written


def verify_links() -> list[str]:
    """Every relative .md link in docs must point at a real doc file."""
    problems: list[str] = []
    slugs = {f.stem for f in DOCS_DIR.glob("*.md")}
    for doc_file in sorted(DOCS_DIR.glob("*.md")):
        for match in re.finditer(r"\]\(([^#)]+\.md)(#[^)]*)?\)", doc_file.read_text(encoding="utf-8")):
            if match.group(1).removesuffix(".md") not in slugs:
                problems.append(f"{doc_file.name}: broken link to {match.group(1)}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Smart Home Comfort Guide site.")
    parser.add_argument("--check", action="store_true", help="build into a temp dir and verify instead of writing site/")
    args = parser.parse_args(argv)

    broken = verify_links()
    if broken:
        for problem in broken:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1

    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            files = build_into(Path(tmp))
        print(f"check passed: {len(files)} files, doc links OK")
        return 0

    for path in build_into(SITE_DIR):
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
