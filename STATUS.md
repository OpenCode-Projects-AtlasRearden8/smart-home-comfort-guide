# Status — Smart Home Comfort Guide

Last updated: 2026-10-25

## What was built

A complete beginner manual for four smart-home device types — **speakers,
plugs, thermostats, and cameras** — written privacy-first with a
local-control mindset, plus a build script that turns the Markdown sources
into a self-contained static HTML site.

**Tone and constraints held throughout:** calm, plain English, never
condescending; no product shilling (options are described by *traits*, with a
few community-famous names for illustration only); local-control favored;
no fear-mongering; no secrets, API keys, or personal data anywhere in the
repository.

### Contents (`docs/`, 13 chapters)

| # | File | Covers |
| --- | --- | --- |
| 1 | `01-getting-started.md` | How to read the manual, a gentle first path |
| 2 | `02-what-devices-hear-and-send.md` | Per-device "what it hears / what it sends" tour + the three questions to ask any gadget |
| 3 | `03-smart-speakers.md` | Placement, mute, voice history, DND |
| 4 | `04-smart-plugs.md` | Uses, safety exceptions, local-schedule traits |
| 5 | `05-smart-thermostats.md` | Install safety photo, schedules, occupancy/geofencing trade-offs |
| 6 | `06-home-cameras.md` | Placement property-line rule, cloud vs local storage, mic settings |
| 7 | `07-local-control-first.md` | What "local" means, three effort levels, community-famous picks |
| 8 | `08-guest-networks.md` | The 10-minute guest-network walkthrough, isolation explainers |
| 9 | `09-muting-and-factory-reset.md` | Physical mute, privacy mode, reset-before-exit habit, generic reset patterns |
| 10 | `10-family-presets.md` | 8 print-and-laminate cards for less-techy family members |
| 11 | `11-room-by-room-checklist.md` | Room-by-room tickable checklist (rendered as real checkboxes) |
| 12 | `12-privacy-settings-table.md` | Settings tables per device type + a 6-minute privacy pass |
| 13 | `13-glossary.md` | Alphabetical plain-English glossary |

### Site (`site/`, generated — committed for convenience)

- `index.html` — hero page with card grid of all chapters
- 13 chapter pages with prev/next pager and an "On this page" TOC
- `style.css` — single hand-rolled stylesheet; print-friendly; zero external
  resources (no JS, no fonts, no analytics, no network requests)
- Relative links only; open `site/index.html` from disk and it just works

### Build tooling

- `build.py` — stdlib-only Markdown-subset → HTML converter and site
  generator (headings/anchors, paragraphs, nested lists, checklists, tables,
  code fences, blockquotes, hr, bold/italic/code/links, `.md` → `.html`
  link rewriting with anchors). Output is deterministic.
- `test_build.py` — 36 stdlib `unittest` tests: inline/block conversion
  cases, build integrity (all pages written, structure, license line on
  every page, no broken page or anchor links, no external URLs),
  checklists/tables rendered, docs↔build list agreement, and byte-level
  determinism of the output.
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale
  Dynamics, LLC`.
- `README.md` — project overview, build/test instructions, credit to
  Asdale Dynamics, LLC.

## How to run

```bash
python3 build.py            # build site/ from docs/
python3 build.py --check    # verify build in a temp dir (no writes)
python3 test_build.py       # run the test suite
```

Then open `site/index.html` in any browser. Requirements: Python 3.8+,
standard library only.

## Verification results (run locally before commit)

- `python3 test_build.py` — **Ran 36 tests … OK**
- `python3 build.py --check` — check passed: 15 files, doc links OK
- `python3 build.py` — wrote 15 files into `site/`
- Link audit: no broken relative links (source `.md` audit via
  `verify_links()` plus generated-HTML page/anchor audit in tests)
- External-resource audit: no `http://`/`https://` URLs, CDNs, or analytics
  references in generated HTML (except the MIT-license explanation link,
  which is page attribution, not a fetched resource)
- Determinism: two builds compared byte-for-byte — identical
- HTML sanity: every page has doctype, `lang="en"`, meta description,
  stylesheet, footer with the licensing line
- Typos/artifact scan of output for stray `**`, odd CJK chars, broken
  entities — clean

## Known gaps / future ideas

- The Markdown converter covers the subset this manual uses (it is not a
  general-purpose Markdown parser; unsupported syntax passes through as
  plain text). If later chapters add footnotes or definition lists, extend
  `build.py` first.
- Checkboxes reset on reload — they're presentation/print aids, not stored
  progress. Could persist via `localStorage` if ever desired.
- Device-specific factory-reset durations are intentionally given as ranges
  ("5–15 seconds, watch for a chime") rather than model- specifics that age
  badly; a firmware-lookup appendix could be added later.
- The site has no search; a client-side index page would be small and could
  be added without violating the no-JS dependency rule (it is optional JS).
- No screenshots/images by design: keeps everything text, low-bandwidth,
  and manufacturer-neutral.
