# What Devices Hear and Send

This is the chapter that makes everything else make sense. We'll walk through
each of the four device types and answer two honest questions: **what can it
hear?** and **what does it send out of your home?** No scare tactics — most of
this is ordinary and manageable — but it's better to know than to guess.

## The four senses, in one table

| Device | What it can hear | What it sends (typically) |
| --- | --- | --- |
| Smart speaker | Sound in the room — voice, TV, music. A hot word (e.g. "Alexa", "Hey Google", "Siri") usually wakes it; most recent models also wake on a wake sound or button press | Voice clips *after* the wake word (if cloud voice is on), app activity, music habits, usage stats |
| Smart plug | Nothing. No microphone at all | Power-on schedules, on/off state, sometimes energy readings, to its cloud (unless it's a local-control plug) |
| Smart thermostat | Nothing audible (a few premium models have voice/sound features you can skip) | Temperature, humidity, occupancy (motion or "someone's home" signals), schedules, heating/cooling runtimes |
| Home camera | Nothing audible unless it has a speaker/mic feature (most have both — more below) | What the lens sees — clips or a live stream — plus motion alerts, and usually audio if enabled |

A good mental model: **speakers and cameras have ears/eyes and want your
words and images; plugs and thermostats are mute devices that want your
*habits* — when things turn on, and when your home is occupied.**

## Smart speakers, plainly

- The microphone is *always* powered — that's how it hears the wake word.
  This is normal and expected, not a fault.
- What matters is what triggers a **recording**: the wake word, a wake sound
  (some models have this, check your settings), or you pressing the button.
- If your speaker's companion app shows a "Voice History" or "Recordings"
  page, that is where any saved clip lives — and usually where you can
  delete them and turn saving off. See the
  [Privacy Settings Table](12-privacy-settings-table.md).
- The mute button on the device (or the physical switch, on most models) cuts
  the microphone at the hardware level. When muted, most devices show a red
  light, an orange dot, or a crosshatch on the light ring. There is no
  cloud pause that beats a physical mute.

## Smart plugs, plainly

- No microphone, no camera. The humblest device here.
- What it knows is on/off state and (on some models) how much energy it
  passes through. Where that goes depends on the brand's design: cloud-only
  plugs send it to the maker's servers; **local-control plugs** keep the
  schedule and status inside your house, handled by your hub or the plug
  itself and shown to you by a local app.
- If plug data leaving your home would bother you, this is exactly the case
  where [Local Control First](07-local-control-first.md) pays off.

## Smart thermostats, plainly

- It does not listen, but it *does* watch patterns: when the house warms,
  when it cools, when someone seems home.
- Thermostats are the one device most families are *happy* to connect — the
  automation genuinely helps. Comfortable middle ground: keep it connected,
  but review the schedule and occupancy settings so its "smart" matches your
  life rather than rediscovering it slowly.
- Occupancy features ("sensors noticed somebody") can usually be turned off
  later if the house becomes predictable.

## Cameras, plainly

- Cameras are the one device type where **placement is a privacy decision**.
  Lenses pointed at your own front door: normal. Lenses into a living room,
  a bedroom, or a neighbor's windows: worth reconsidering.
- Most cameras include a **microphone** as well, because two-way talk is a
  selling feature. If you never use two-way talk, look for a setting named
  "audio recording" or "microphone" and switch it off.
- Where your clips land matters: cloud subscriptions keep footage on the
  company's servers; **local storage** (a microSD card in the camera, or a
  hub/NVR in your closet) keeps it in your house. See
  [Home Cameras](06-home-cameras.md) for a plain walk-through.
- If seeing strangers' property bothers your conscience the same way seeing
  yours bothers them — that instinct is right. Aim inside your own property
  line.

## The three questions to ask about any gadget

Before (or after) inviting any device into your home, you can ask just three
things:

1. **What are its senses?** Microphone, camera, presence, power meter?
2. **Where do its memories go?** Straight to a company's cloud, to a hub
   inside your house, or to a memory card in the device itself?
3. **Can it do its job if the internet is out?** If yes, you've found a
   *local-capable* device — the quiet hero of this manual.

You don't need the perfect answer to question three — "the lights still turn
off at bedtime when the internet is down" is a very achievable bar.

## Calm summary

- Speakers: ears always on, recordings only after being called.
- Plugs and thermostats: no ears, but they remember routines.
- Cameras: eyes (and ears) — placement and storage settings are your privacy
  levers.
- Everything above has an off switch, a mute switch, or a settings page, and
  the coming chapters show you all of them.
