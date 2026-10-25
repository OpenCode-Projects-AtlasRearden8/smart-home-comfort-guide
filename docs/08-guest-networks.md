# Guest Networks, Plain English

A guest network is a second lane of the same road. Your family's phones,
speakers, and cameras ride one lane; guests' phones ride the other. Same
house, same address (the same router), but the lanes don't mix. That's the
whole idea. This chapter gets you from "sounds nice" to "done in ten
minutes."

## Why bother, plainly

Three reasons in growing order of importance:

1. **Politeness, automated.** Guests get Wi-Fi without you reading out a
   forty-character password over zooming crickets.
2. **Safety-in-depth.** A visitor's laptop with an old, unpatched flaw can't
   sniff around your printer's settings or poke at your thermostat from the
   guest lane.
3. **Privacy furniture.** Your smart devices live on the family lane. Things
   that don't need to *talk to* your devices simply can't. Neighbors still
   borrow sugar; they don't need to borrow your camera feed.

## What it protects against (and what it doesn't)

It protects the *shape* of your network: family and guest clients can't
address each other directly. It does **not** fix bad password hygiene, an
outdated router, or a camera you plugged into the TV-lane by accident. It's
one good lock, not the whole door.

## The 10-minute walkthrough (most routers)

Exact wording varies by router brand, but the shape is always the same. Look
in your router's web settings (often `192.168.0.1` or `192.168.1.1` in a
browser) or its phone app, and find:

1. **Wireless → Guest network** (or "Guest Wi-Fi," "Visitor access," "2.4G
   Guest.")
2. Turn it **on**.
3. Name it something friendly: `SureHills-Guest`. (Anything except your real
   family network's name.)
4. Give it a **separate password** — shorter than a novel is fine; guests
   type it on phone keyboards.
5. Find the toggle called **"Allow guests to see each other"** — make sure
   it's **off**.
6. Same style of toggle for **"Allow access to local network / intranet"** —
   **off**. This is the real lock; the rest is presentation.
7. Optional but nice: a **speed cap** ("limit bandwidth") so one guest's
   game patch doesn't slow your family speaker.
8. Save, then connect with a phone you brought as a guest and test: you
   *should* get internet and *should not* be able to reach your printer or
   camera.

## The two settings that matter most

If you remember only two words: **isolation** and **no local access.** Every
guest-network feature is some version of "keep the guest lane from touching
the family lane." Skip the fancy portal pages and bandwidth limits if they
frustrate you; isolation is the part with teeth.

## Where do smart devices live, then?

- **Family lane**: speakers, plugs, thermostat, cameras, computers, phones —
  everything that is *your* stuff.
- **Guest lane**: visitors' phones, the babysitter's tablet, the in-laws'
  laptop, your kid's school friends. Possibly also the doorbell camera if
  it's cloud-heavy and you want it extra-segregated — with the caveat that
  if you use a local-control hub, it must be on the family lane to be
  reachable.

One practical note for IoT-tinkerers: some routers let you make a third
lane (an "IoT network") for gadgets alone. That's genuinely tidy, not
required — the guest lane is the 90% win.

## When guests ask for the password

Have a story-free answer. A card by the front door (see
[Family Presets](10-family-presets.md)) with the guest Wi-Fi name and
password, laminated, is both charming and practical. If you update the
password once a quarter, make re-printing the card part of that ritual.

## Calm summary

- Two lanes, one road.
- The toggle to hunt for is **"no access to local network."**
- Everything that's *your stuff* rides the family lane; guests ride the
  other.
- Ten minutes, one router settings visit, engraved forever.
