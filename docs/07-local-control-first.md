# Local Control First

"Local control" is the quiet backbone of this manual. Here it is in one
sentence: **a local device does its job inside your house, on your network,
without needing a company's distant servers to think for it.** This chapter
explains why that idea is worth caring about, what it gets you, and how to
find it without becoming an engineer.

## Why "local" is the privacy-friendly default

Every byte a device sends to a company's servers is a byte about your life
that lives on somebody else's disk — subject to their retention policy,
their breach history, and their future acquisitions. A device that works
locally mostly can't leak what it never sends. Local control also has
honest, non-privacy benefits:

- **It works when the internet is out.** The schedule lives on the plug, not
  a server in another state.
- **It's faster.** A "turn off the lamp" that doesn't detour to the cloud
  responds in a fraction of the time.
- **It outlives the company.** Cloud-only gadgets become paperweights when
  the maker loses interest. Local devices keep working.

## The nickname: "cloud-tethered"

Most beginner-oriented devices are cloud-tethered: they work through an app
that goes out to the internet, reaches the maker's servers, and comes back.
It's the easiest path (that's why makers choose it), and it's fine for many
people. The point of this chapter is not to shame cloud devices — it's to
show that a **local-first subset** exists and is often no harder.

## How to spot local-capable devices (no engineering degree required)

On the product page or box, look for these words — they're the plain-English
signals:

- **"Works with Home Assistant"** — Home Assistant is free, open-source
  software that runs on a small box in your closet and becomes your home's
  measuring stick and remote.
- **Matter, or Thread** — modern standards designed, in part, for local
  control across brands.
- **Zigbee or Z-Wave** — older radio standards that pair with a hub that
  lives in your house.
- **"No cloud required" / "local API" / "on-device schedules."**
- **HomeKit compatibility** — Apple's stack keeps most control and history
  local to your home hub.

If a product page mentions none of these and only says "download our app,"
it's cloud-tethered: not forbidden, just not the local-first pick.

## The three common local-first setups (ranked by effort)

### Level 1: A local-friendly hub

Buy nothing extra beyond what you'd buy anyway; pick devices that pair with
a hub (Zigbee/Z-Wave/Thread) rather than Wi-Fi gadgets. The hub sits in a
closet, keeps schedules and rules inside your home, and serves an app that
works on your network. HomeKit homes and hub-based starter kits both
qualify. Effort: low — the "local" happens because of the shape of the gear,
not because of your skills.

### Level 2: Home Assistant on a small computer (the community favorite)

Home Assistant is free, open-source home-control software. People run it on
a Raspberry Pi-style single-board computer or a mini PC, or in a ready-made
"Home Assistant Yellow/Green" style box. Its skill curve is real but
gentle: start with plugs and lights, and let it grow at your pace. Its
community documentation is famously patient with beginners. Effort:
medium — one evening to start, then as many evenings as you enjoy.

### Level 3: The tinkerer's shelf

ESPHome and DIY microcontroller gadgets, home-grown dashboards, scripts that
tie everything together. Honestly, past Level 2 most people are having the
fun for its own sake — and that's fine, this is a guide, not a rulebook.

## A few genuinely local-friendly picks (named because they're famous, not because anyone paid)

- **Home Assistant** — free, open source; the community standard for local
  hubs.
- **Hubitat Elevation** — a purpose-built local-control hub (Zigbee/Z-Wave).
- **Apple HomeKit**, via HomeKit-compatible devices or a hub — most control
  flows locally by design.
- **Shelly** brand plugs/relays — many models expose local control with
  "local API."
- **Aqara / Zigbee sensors and plugs** with a local hub (see again Level 1).
- **Lutron Caséta** — lighting with a well-liked local hub integration in
  Home Assistant.

The general shape to remember: **hubs first (Level 1) covers most people.
Level 2 is worth one nice weekend. Level 3 is optional joy.**

## What local control does *not* mean

It doesn't mean zero internet ever: apps get updates, firmware downloads,
and voice-cloud devices still use the cloud. It means **when the internet
goes down, the important stuff — lights, schedules, locks, heating — keeps
working**, and your day-to-day logs mostly stay home.
