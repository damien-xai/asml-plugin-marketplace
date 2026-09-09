---
name: asml-motion-safety
description: >
  Watchdogs, interlocks, and fail-safe actuator commands for ASML scanner motion control.
  Use when adding a new actuator, changing travel limits, handling faults, or reviewing
  safety-related C++ on the wafer stage, reticle stage, or wafer handler. Triggers:
  "asml safety", "interlock", "watchdog", "estop", "fail-safe", "travel limit".
---

# ASML motion safety

Mock skill. These are coding rules for fail-safe motion, not a certified safety case.

## Envelope

Every `write()` of a setpoint goes through a clamp:

1. **Travel limits** — software stops inside the hardware hard-stops, with a margin the module declares in `init()`.
2. **Velocity / acceleration** — reject commands that the plant cannot physically follow in one cycle.
3. **Interlock mask** — if any bit in the module's interlock word is set, output the **safe state**, not the controller's request.

Safe state is defined per actuator at `init()` (usually hold last-good position or remove force). Never invent "zero everything" as a default — zero force on a gravity-loaded axis is a drop.

## Watchdog

The cycle function increments a counter the safety supervisor samples. If two consecutive machine cycles are missed, the supervisor commands safe state. New modules must:

- Export `heartbeat()` from the same translation unit as the cycle.
- Not reset the counter from a diagnostics thread.

## Faults are sticky

A limit violation, driver error, or missed heartbeat sets a sticky fault. Only a supervisory `reset()` after the plant is verified idle may clear it. Do not auto-clear inside the servo.

## What not to do

- Do not catch-and-continue on a driver error in `actuate()`.
- Do not raise travel limits to "make the test pass".
- Do not put the interlock check behind an `#ifdef NDEBUG`.
