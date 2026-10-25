# Smart Thermostats

A thermostat that connects to the Wi-Fi can be adjusted from anywhere, keeps
a weekly schedule without a human re-programming it, and quietly saves energy
by not heating an empty house. Of the four devices in this guide it is the
one most people end up genuinely glad they connected — and for good reason:
the savings and comfort are real, and it has a sensible personality (a
thermostat's interest is in your home's temperature, not your conversations).

## What a smart thermostat is good at

- **A schedule that survives life.** Nobody re-programs the thermostat after
  the kids' piano lessons move.
- **Remote touch.** "Warm the guest room before Grandma arrives" from your
  phone, without walking upstairs.
- **Not heating an empty house.** Presence features and schedules both serve
  this; the savings are usually visible in your first winter bill.
- **Small, useful reports.** Runtime and history pages tell you if something
  changed ("the furnace ran 40% more this week — did a filter get dirty?").

## Before you install (safety check, gently)

Thermostats control HVAC wiring, which is low voltage but *not*
idiot-of-the-wires-proof:

- Turn the breaker off before removing the old unit.
- **Take a photo of the existing wires first.** The photo is the most useful
  tool in the box.
- Note whether a **C-wire** (a "common" wire) exists. Many smart thermostats
  want one; if the photo shows one, good; if not, look for a brand that
  explicitly supports no-C-wire homes. If this paragraph felt like static,
  it's a genuine "worth a plumber" moment — a one-hour HVAC tech visit is
  cheap insurance and very normal.
- Never use an old thermostat's backplate as a shelf. (Do not ask how we
  know.)

## First ten minutes, once

1. Connect it to Wi-Fi and the companion app, following its steps.
2. Set a simple schedule first — wake/go-out/evening/night — matching your
   real life, not an idealized version. One degree of honesty here is worth
   five settings later.
3. Walk through the app's **Privacy** or **Data** page once. Note things
   like occupancy sensing, cloud analytics, and ad/partner choices, if any.
4. If it proposes "auto-schedule learning," decide consciously whether you
   want a thermostat that's *learning your patterns* (it is) or one doing
   exactly what a schedule says. Both are fine; knowing which you have will
   save you confusion later.

## Settings worth finding

- **Occupancy / "someone's home" sensing:** genuinely useful in some homes;
  free to turn off later if yours never varies.
- **Geofencing** ("heat the house when my phone enters the county"): handy,
  but it makes your phone's location part of the system. Skip it if that
  bugs you — a schedule gets you 80% of the win.
- **Cloud vs local hits:** some thermostats offer a local API or a direct
  integration with local-control hubs. If keeping its data at home matters
  to you, pick models supporting hubs like Home Assistant or HomeKit — see
  [Local Control First](07-local-control-first.md).

## One comfort trap to avoid

If your house has a single furnace, don't try to make the thermostat argue
rooms into comfort: the thermostat sets what the *house* does, and room
comfort comes from ceiling fans, throws, closed doors, and one more blanket.
Raising the whole house two degrees to warm one cold bedroom is the oldest
mistake in the manual.

## Calm summary

- The thermostat is the device most worth connecting to the cloud, if any
  is.
- A photo of the wires before you start; a real schedule during setup; a
  quiet tour of the privacy page at the end.
- Everything else — occupancy, geofencing, learning — is opt-in seasoning.
