---
name: asml-test-diagnostics
description: >
  Calibration, diagnostics, and HIL/SIL test automation for ASML scanners.
  Use when planning hardware-in-the-loop tests, writing diagnostic playbooks, or
  turning a field abort/drift symptom into a reproducible test. Triggers:
  /asml-hil-plan, "asml diagnostics", "asml hil", "asml sil", "scanner abort",
  "asml test automation".
---

# ASML test and diagnostics

Mock skill. HIL means a local fake plant, not a Veldhoven scanner.

## Choose SIL vs HIL

| Level | Plant | Use |
|---|---|---|
| SIL | Pure software fake of the module | Logic, fault flags, recipe handling |
| HIL | Fake plant + the real control binary (or a hardware-in-the-loop rig) | Timing, drivers, watchdogs |

Default SIL. Promote to HIL only when the user names cycle time, drivers, or a hardware rig.

## Test plan shape

Write a markdown plan (or the repo's existing test-plan format) with:

1. **Module** and cycle budget (from `asml-embedded-control` if it is a control module).
2. **Stimulus** — one table of inputs (setpoints, faults injected).
3. **Expect** — numeric tolerances in the same units as production (`nm`, `µs`).
4. **Abort cases** — missed heartbeat, travel-limit, driver error. Each must end in the documented safe state.
5. **Collect** — traces: `t_ns`, command, estimate, output, fault word.

Do not add a "run on tool" step. The last step is `pytest` (or the repo runner) against the fake plant.

## Diagnostic playbook

When the user pastes a symptom (overlay drift, focus excursion, unexpected ABORT):

1. Name the subsystem (stage / optics / handler / source) from the symptom — say if you are guessing.
2. List the **off-cycle** signals to dump (heartbeat counters, last sticky fault, last recipe hash).
3. Give a SIL test that reproduces the abort without hardware.
4. Point at `asml-calibration` if the likely fix is a calibration update rather than a code change.

## Coding rules for tests

- Tests may allocate. Production control code under test still must not, on the cycle.
- Time is simulated (`t_ns += cycle_ns`). Do not `sleep()` to wait for a 1 ms cycle.
- Seeds are fixed. Traces land next to the test, not on stdout only.
