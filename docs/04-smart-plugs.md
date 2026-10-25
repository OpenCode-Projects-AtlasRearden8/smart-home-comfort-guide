# Smart Plugs

A smart plug is a small adapter that fits between the wall outlet and
something else's plug, and lets you switch that thing on or off by app,
schedule, voice, or rule. It is the gentlest possible entry to home
automation: no electrician, no app big enough to frighten anyone, and it is
one of the easiest devices to get working **locally** — a nice thing, given
this guide's leanings.

## What plugs are wonderful for

- **Lamps** — the classic warm win. "The hallway light already off" is a
  comfort you stop noticing because it always works.
- **Coffee makers and kettles** — morning routines that start themselves.
- **Fans** — a bedroom fan that winds down with a schedule instead of with
  you.
- **Christmas lights**, aquarium lights, humidifiers — anything whose switch
  would otherwise need an actual human.

## What never goes in a smart plug

Keep these off smart plugs entirely, for safety reasons, with no exceptions:
space heaters, electric blankets, air conditioners above the plug's rating,
 Anything medically necessary (oxygen concentrators, CPAP and similar).
Also anything life-safety critical, like a sump pump or deep freezer. The
reason is simple: software and routines occasionally miss a beat, and those
specific appliances should not be part of any missed beat.

## Picking a plug: the traits that matter

Instead of a shopping list, here are the four traits worth checking, in
order, next time you're at the Plug Wall:

1. **Does it work locally?** Look for words like "local control," "works
   with Home Assistant," "Zigbee," "Thread," "Matter," or "no cloud
   required." A plug that keeps its own schedule or pairs with a hub inside
   your house is the [Local Control First](07-local-control-first.md) ideal.
2. **Does the schedule live on the plug or on a server?** If the app is the
   only place the schedule exists, an internet outage makes the plug stupid.
   If the schedule lives on the plug or hub, it survives the outage.
3. **Energy metering?** (nice to have) Small metering shows you what a
   device is really doing — "did the dehumidifier even turn on?"
4. **Safety listings** (UL/ETL equivalents in your region) — check the
   fine print on the box; it's one line and it matters.

## First ten minutes, once

1. Plug it in, pair it by the app's instructions, and **name it
   something you'll say aloud** — "Hallway Lamp," not "TP-Link HS103-4F2A."
2. Set its one schedule (on at 6:45 pm, off at 11:30 pm) *and* check whether
   an "Away mode" or "Randomize" option exists for when you travel.
3. Test with your voice assistant if you have one: "turn off the Hallway
   Lamp" should cause a click you can hear from the couch.

## Two patterns worth having

- **The Bedtime Plug**: one lamp, one schedule, one voice command. Complete.
- **The Away Mode**: before a trip, turn off everything non-essential and
  let a couple of plugs run an on/off-random pattern. It costs nothing and
  is old-fashioned-effective.

## Calm summary

- Plugs are the cheapest, most forgiving win in home automation.
- They're mute — nothing to hear, just habits to check.
- One schedule + a name you'll actually say + local control if you can find
  it = done well.
