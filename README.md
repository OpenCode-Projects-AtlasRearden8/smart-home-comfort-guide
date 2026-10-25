# Smart Home Comfort Guide

A calm, plain-English beginner manual for smart speakers, smart plugs, smart
thermostats, and home cameras — written privacy-first, with a local-control
mindset. No fear, no hype, no product pushing. Just clear steps that help you
and your family enjoy the comfort of a smart home *and* keep your privacy.

This project is maintained by **Asdale Dynamics, LLC** as part of its
beginner-friendly technology education series, in the same spirit as Dylan
Asdale's *The Massive AI Manual*: explained like a friend would, step by step,
never condescending.

## Who this is for

- Anyone setting up their first smart speaker, plug, thermostat, or camera.
- Families who want the comfort, not the complexity.
- People who care about privacy and want devices that work **without** the
  cloud when possible.
- Less-techy household members who just want things to *work* — there are
  print-ready presets and a room-by-room checklist.

## What's inside (`docs/`)

| Doc | What it covers |
| --- | --- |
| [Getting Started](docs/01-getting-started.md) | How to read this manual, and a gentle first path |
| [What Devices Hear and Send](docs/02-what-devices-hear-and-send.md) | The honest, calm tour of each device type's senses and data flow |
| [Smart Speakers](docs/03-smart-speakers.md) | Choosing, placing, muting, and living with a speaker |
| [Smart Plugs](docs/04-smart-plugs.md) | The easiest win in home automation |
| [Smart Thermostats](docs/05-smart-thermostats.md) | Comfort and savings without surprises |
| [Home Cameras](docs/06-home-cameras.md) | Watching over your home while caring about privacy |
| [Local Control First](docs/07-local-control-first.md) | What "local" means, why it's the privacy-friendly default, and starter picks |
| [Guest Networks, Plain English](docs/08-guest-networks.md) | A second lane on your Wi-Fi, explained like a friend would |
| [Muting and Factory Reset](docs/09-muting-and-factory-reset.md) | Turning things off, and starting over cleanly |
| [Family Presets](docs/10-family-presets.md) | Print-friendly "if this, do that" cards for less-techy family members |
| [Room-by-Room Checklist](docs/11-room-by-room-checklist.md) | Walk each room once and finish with a sensible setup |
| [Privacy Settings Table](docs/12-privacy-settings-table.md) | One table you can screenshot: what to check, where |
| [Glossary](docs/13-glossary.md) | Every jargon word, explained in everyday language |

## Build the site

The manual builds into a small static HTML site (no JavaScript required, no
network requests) with one command:

```bash
python3 build.py
```

Then open `site/index.html` in any browser. The site is self-contained:
styles live in `site/style.css`, links are relative, and nothing phones home.

`python3 build.py --check` verifies the output without overwriting timestamps
expectations — useful in scripts.

## Tests

```bash
python3 test_build.py
```

Runs the standard-library test suite covering the Markdown converter, link
generation, and build integrity.

## Requirements

- Python 3.8+ (standard library only — no packages to install)
- Any operating system

## Privacy of this project itself

This repository contains no secrets, API keys, or personal data. The generated
site makes no network requests and uses no analytics, fonts, or scripts from
the internet.

## Credits and license

- Guide and code by **Asdale Dynamics, LLC** — beginner-friendly AI and
  technology education, books, and practical tools.
- Learn more at Dylan Asdale's hub, `dylanasdale.github.io`.
- Released under the MIT License — see [LICENSE](LICENSE).
  © 2026 Asdale Dynamics, LLC.
