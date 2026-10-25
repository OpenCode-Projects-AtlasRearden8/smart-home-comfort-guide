#!/usr/bin/env python3
"""Tests for the Smart Home Comfort Guide builder.

Run with:  python3 test_build.py   (stdlib unittest — no dependencies)
"""

from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

import build


class InlineTests(unittest.TestCase):
    def test_escapes_html(self):
        self.assertIn("&amp;", build.md_inline("a & b < c > d"))

    def test_bold(self):
        self.assertEqual("<strong>comfort</strong>", build.md_inline("**comfort**"))

    def test_bold_spans_asterisk_pair(self):
        out = build.md_inline("**one *two* three**")
        self.assertIn("<strong>one <em>two</em> three</strong>", out)

    def test_italic(self):
        self.assertEqual("<em>calm</em>", build.md_inline("*calm*"))

    def test_code_protects_markdown(self):
        out = build.md_inline("`**not bold**`")
        self.assertIn("<code>**not bold**</code>", out)

    def test_link(self):
        out = build.md_inline("[Kitchen](04-smart-plugs.md)")
        self.assertEqual('<a href="04-smart-plugs.md">Kitchen</a>', out)

    def test_fix_links_rewrites_md_to_html(self):
        out = build.fix_links('<a href="04-smart-plugs.md">Kitchen</a>')
        self.assertIn('href="04-smart-plugs.html"', out)

    def test_fix_links_keeps_anchors(self):
        out = build.fix_links('<a href="13-glossary.md#thread">t</a>')
        self.assertIn('href="13-glossary.html#thread"', out)


class BlockTests(unittest.TestCase):
    def test_heading_gets_slug_id(self):
        out = build.md_to_html("## Guest Networks, Plain English")
        self.assertIn('<h2 id="guest-networks-plain-english">', out)

    def test_duplicate_heading_slugs_get_counter(self):
        out = build.md_to_html("## Room\n\n## Room")
        self.assertIn('id="room"', out)
        self.assertIn('id="room-1"', out)

    def test_paragraph(self):
        out = build.md_to_html("Hello there.")
        self.assertEqual("<p>Hello there.</p>", out)

    def test_wrapped_paragraph_joins_lines(self):
        out = build.md_to_html("one\nwrapped")
        self.assertEqual("<p>one wrapped</p>", out)

    def test_unordered_list(self):
        out = build.md_to_html("- a\n- b")
        self.assertEqual("<ul><li>a</li><li>b</li></ul>", out)

    def test_ordered_list_keeps_order(self):
        out = build.md_to_html("1. a\n2. b\n10. c")
        self.assertEqual("<ol><li>a</li><li>b</li><li>c</li></ol>", out)

    def test_nested_list(self):
        out = build.md_to_html("- a\n  - nested")
        self.assertEqual("<ul><li>a<ul><li>nested</li></ul></li></ul>", out)

    def test_continuation_line_joins_item(self):
        out = build.md_to_html("- first part\n  second part")
        self.assertEqual("<ul><li>first part second part</li></ul>", out)

    def test_checklist_unchecked(self):
        out = build.md_to_html("- [ ] wash the dishes")
        self.assertIn('class="check"', out)
        self.assertIn('type="checkbox">', out)
        self.assertIn("wash the dishes", out)

    def test_checklist_checked(self):
        out = build.md_to_html("- [x] done already")
        self.assertIn(' checked=""', out)

    def test_table(self):
        md = "| a | b |\n| --- | --- |\n| 1 | 2 |"
        out = build.md_to_html(md)
        self.assertIn("<th>a</th>", out)
        self.assertIn("<td>1</td>", out)

    def test_hr(self):
        self.assertIn("<hr>", build.md_to_html("---"))

    def test_blockquote(self):
        out = build.md_to_html("> quiet wisdom")
        self.assertIn("<blockquote><p>quiet wisdom</p></blockquote>", out)

    def test_code_block_escapes(self):
        out = build.md_to_html("```\n<a>&\n```")
        self.assertIn("<pre><code>&lt;a&gt;&amp;</code></pre>", out)

    def test_blank_line_separators(self):
        out = build.md_to_html("A\n\nB")
        self.assertEqual("<p>A</p>\n<p>B</p>", out)


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name)
        build.build_into(self.out)

    def test_all_doc_pages_written(self):
        for slug, _ in build.DOCS:
            self.assertTrue((self.out / f"{slug}.html").is_file(), slug)

    def test_index_and_css_written(self):
        self.assertTrue((self.out / "index.html").is_file())
        self.assertTrue((self.out / "style.css").is_file())

    def test_every_page_has_html_document_structure(self):
        for path in self.out.glob("*.html"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("<!DOCTYPE html>", text, path.name)
            self.assertIn('lang="en"', text, path.name)
            self.assertIn("</html>", text, path.name)

    def test_license_line_appears_on_every_page(self):
        for path in self.out.glob("*.html"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("© 2026 Asdale Dynamics, LLC", text, path.name)

    def test_home_links_to_every_doc(self):
        text = (self.out / "index.html").read_text(encoding="utf-8")
        for slug, _ in build.DOCS:
            self.assertIn(f"{slug}.html", text)

    def test_pagers_link_neighbors(self):
        text = (self.out / "02-what-devices-hear-and-send.html").read_text(encoding="utf-8")
        self.assertIn("01-getting-started.html", text)
        self.assertIn("03-smart-speakers.html", text)

    def test_no_broken_doc_links_in_output(self):
        pages = {f"{slug}.html" for slug, _ in build.DOCS} | {"index.html", "style.css"}
        heading_ids = {
            path: set(re.findall(r'<h[1-6] id="([^"]+)"', path.read_text(encoding="utf-8")))
            for path in self.out.glob("*.html")
        }
        for path in self.out.glob("*.html"):
            text = path.read_text(encoding="utf-8")
            for match in re.finditer(r'href="([^"]*)"', text):
                page, _, anchor = match.group(1).partition("#")
                self.assertTrue(page == "" or page in pages, f"{path.name}: {page}")
                if anchor:
                    target = path if not page else self.out / page
                    self.assertIn(
                        anchor,
                        heading_ids.get(target, set()),
                        f"{path.name}: anchor {page}#{anchor}",
                    )

    def test_no_local_network_urls_in_output(self):
        for path in self.out.glob("*.html"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("http://", text.replace("http://", "http://", 1), path.name)
            for bad in ("http://", "https://fonts", "//cdn.", "google-analytics"):
                self.assertNotIn(bad, text, f"{path.name}: {bad}")

    def test_checklists_use_real_checkboxes(self):
        text = (self.out / "11-room-by-room-checklist.html").read_text(encoding="utf-8")
        self.assertGreater(text.count('type="checkbox"'), 10)

    def test_tables_render_with_headers(self):
        text = (self.out / "12-privacy-settings-table.html").read_text(encoding="utf-8")
        self.assertGreater(text.count("<thead>"), 4)

    def test_docs_source_links_resolve(self):
        self.assertEqual([], build.verify_links())


class IntegrityTests(unittest.TestCase):
    def test_docs_dir_has_all_sources(self):
        for slug, _ in build.DOCS:
            self.assertTrue((build.DOCS_DIR / f"{slug}.md").is_file(), slug)

    def test_output_is_deterministic(self):
        with tempfile.TemporaryDirectory() as a:
            build.build_into(Path(a))
            first = {p.name: p.read_bytes() for p in Path(a).glob("*")}
        with tempfile.TemporaryDirectory() as b:
            build.build_into(Path(b))
            second = {p.name: p.read_bytes() for p in Path(b).glob("*")}
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main(verbosity=2)
